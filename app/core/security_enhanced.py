"""
Enhanced Security Module for Collapp
Implements enterprise-grade security measures
"""
import secrets
import hashlib
import hmac
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.hash import argon2
import bcrypt
from app.core.config import settings

# Enhanced password context with Argon2
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"], 
    deprecated="auto",
    argon2__memory_cost=65536,  # 64MB
    argon2__time_cost=3,        # 3 iterations
    argon2__parallelism=1       # 1 thread
)

class SecurityManager:
    """Enhanced security manager with multiple layers of protection"""
    
    def __init__(self):
        self.failed_attempts = {}  # Rate limiting
        self.blocked_ips = set()   # IP blocking
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password with timing attack protection"""
        try:
            # Add constant time delay to prevent timing attacks
            time.sleep(0.1)
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False
    
    def get_password_hash(self, password: str) -> str:
        """Generate secure password hash with salt"""
        return pwd_context.hash(password)
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Validate password strength"""
        errors = []
        score = 0
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters")
        else:
            score += 1
            
        if len(password) >= 12:
            score += 1
            
        if any(c.isupper() for c in password):
            score += 1
        else:
            errors.append("Password must contain uppercase letters")
            
        if any(c.islower() for c in password):
            score += 1
        else:
            errors.append("Password must contain lowercase letters")
            
        if any(c.isdigit() for c in password):
            score += 1
        else:
            errors.append("Password must contain numbers")
            
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        else:
            errors.append("Password must contain special characters")
            
        # Check for common passwords
        common_passwords = ["password", "123456", "qwerty", "admin", "letmein"]
        if password.lower() in common_passwords:
            errors.append("Password is too common")
            score = 0
            
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "score": score,
            "strength": self._get_strength_label(score)
        }
    
    def _get_strength_label(self, score: int) -> str:
        """Get password strength label"""
        if score <= 2:
            return "Weak"
        elif score <= 4:
            return "Medium"
        else:
            return "Strong"
    
    def create_access_token(self, data: dict, expires_delta: Optional[int] = None) -> str:
        """Create secure JWT token with additional claims"""
        to_encode = data.copy()
        now = datetime.utcnow()
        
        if expires_delta:
            expire = now + timedelta(seconds=expires_delta)
        else:
            expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            
        # Add security claims
        to_encode.update({
            "exp": expire,
            "iat": now,
            "nbf": now,
            "jti": secrets.token_urlsafe(32),  # JWT ID for revocation
            "iss": "collapp-api",              # Issuer
            "aud": "collapp-client"            # Audience
        })
        
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token with enhanced validation"""
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM],
                audience="collapp-client",
                issuer="collapp-api"
            )
            return payload
        except JWTError:
            return None
    
    def check_rate_limit(self, identifier: str, max_attempts: int = 5, window_minutes: int = 15) -> bool:
        """Check if identifier is rate limited"""
        now = time.time()
        window_start = now - (window_minutes * 60)
        
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = []
            
        # Clean old attempts
        self.failed_attempts[identifier] = [
            attempt for attempt in self.failed_attempts[identifier] 
            if attempt > window_start
        ]
        
        return len(self.failed_attempts[identifier]) < max_attempts
    
    def record_failed_attempt(self, identifier: str):
        """Record a failed login attempt"""
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = []
        self.failed_attempts[identifier].append(time.time())
    
    def generate_csrf_token(self) -> str:
        """Generate CSRF token"""
        return secrets.token_urlsafe(32)
    
    def verify_csrf_token(self, token: str, expected: str) -> bool:
        """Verify CSRF token"""
        return hmac.compare_digest(token, expected)
    
    def sanitize_input(self, data: str) -> str:
        """Sanitize user input"""
        if not isinstance(data, str):
            return str(data)
            
        # Remove potential XSS vectors
        dangerous_chars = ['<', '>', '"', "'", '&', 'javascript:', 'data:', 'vbscript:']
        for char in dangerous_chars:
            data = data.replace(char, '')
            
        return data.strip()
    
    def generate_api_key(self) -> str:
        """Generate secure API key"""
        return f"ck_{secrets.token_urlsafe(32)}"
    
    def hash_api_key(self, api_key: str) -> str:
        """Hash API key for storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()

# Global security manager instance
security_manager = SecurityManager()