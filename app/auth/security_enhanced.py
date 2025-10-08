"""
Enhanced Authentication with Security Features
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.security_enhanced import security_manager
from app.core.audit import audit, SecurityEventType
from app.db.database import get_db
from app.auth.crud import get_user_by_email
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()

class EnhancedAuthService:
    """Enhanced authentication service with security features"""
    
    def __init__(self):
        self.max_login_attempts = 5
        self.lockout_duration = 30  # minutes
        self.failed_attempts = {}
        self.locked_accounts = {}
    
    def authenticate_user(
        self, 
        email: str, 
        password: str, 
        ip_address: str,
        user_agent: str,
        db: Session
    ):
        """Authenticate user with enhanced security"""
        
        # Check if account is locked
        if self._is_account_locked(email):
            audit.log_login_attempt(email, False, ip_address, user_agent, "account_locked")
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Account temporarily locked due to multiple failed attempts"
            )
        
        # Check rate limiting
        if not security_manager.check_rate_limit(ip_address):
            audit.log_security_event(
                SecurityEventType.RATE_LIMIT_EXCEEDED,
                ip_address=ip_address,
                details={"email": email}
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later."
            )
        
        # Get user
        user = get_user_by_email(db, email)
        if not user:
            self._record_failed_attempt(email)
            audit.log_login_attempt(email, False, ip_address, user_agent, "user_not_found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verify password
        if not security_manager.verify_password(password, user.hashed_password):
            self._record_failed_attempt(email)
            audit.log_login_attempt(email, False, ip_address, user_agent, "invalid_password")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Check if user is active
        if not user.is_active:
            audit.log_login_attempt(email, False, ip_address, user_agent, "account_disabled")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account disabled"
            )
        
        # Success - clear failed attempts
        self._clear_failed_attempts(email)
        audit.log_login_attempt(email, True, ip_address, user_agent)
        
        return user
    
    def create_tokens(self, user_id: str) -> dict:
        """Create access and refresh tokens"""
        access_token = security_manager.create_access_token(
            data={"sub": str(user_id), "type": "access"}
        )
        refresh_token = security_manager.create_access_token(
            data={"sub": str(user_id), "type": "refresh"},
            expires_delta=7 * 24 * 60 * 60  # 7 days
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    def validate_password_strength(self, password: str) -> dict:
        """Validate password strength"""
        return security_manager.validate_password_strength(password)
    
    def _record_failed_attempt(self, email: str):
        """Record failed login attempt"""
        now = datetime.utcnow()
        if email not in self.failed_attempts:
            self.failed_attempts[email] = []
        
        self.failed_attempts[email].append(now)
        
        # Clean old attempts (older than 1 hour)
        hour_ago = now - timedelta(hours=1)
        self.failed_attempts[email] = [
            attempt for attempt in self.failed_attempts[email]
            if attempt > hour_ago
        ]
        
        # Lock account if too many attempts
        if len(self.failed_attempts[email]) >= self.max_login_attempts:
            self.locked_accounts[email] = now + timedelta(minutes=self.lockout_duration)
            audit.log_security_event(
                SecurityEventType.ACCOUNT_LOCKED,
                details={"email": email, "attempts": len(self.failed_attempts[email])}
            )
    
    def _clear_failed_attempts(self, email: str):
        """Clear failed attempts for user"""
        if email in self.failed_attempts:
            del self.failed_attempts[email]
        if email in self.locked_accounts:
            del self.locked_accounts[email]
    
    def _is_account_locked(self, email: str) -> bool:
        """Check if account is locked"""
        if email not in self.locked_accounts:
            return False
        
        unlock_time = self.locked_accounts[email]
        if datetime.utcnow() > unlock_time:
            del self.locked_accounts[email]
            return False
        
        return True

# Global auth service
auth_service = EnhancedAuthService()

async def get_current_user_secure(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current user with enhanced security validation"""
    
    # Extract IP and user agent
    ip_address = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    # Verify token
    payload = security_manager.verify_token(credentials.credentials)
    if not payload:
        audit.log_security_event(
            SecurityEventType.PERMISSION_DENIED,
            ip_address=ip_address,
            details={"reason": "invalid_token"}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    # Check token type
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Get user from database
    from app.auth.crud import get_user
    user = get_user(db, user_id)
    if not user or not user.is_active:
        audit.log_security_event(
            SecurityEventType.PERMISSION_DENIED,
            user_id=user_id,
            ip_address=ip_address,
            details={"reason": "user_not_found_or_inactive"}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Log data access
    audit.log_data_access(
        user_id=str(user.id),
        resource="user_profile",
        action="read",
        ip_address=ip_address
    )
    
    return user