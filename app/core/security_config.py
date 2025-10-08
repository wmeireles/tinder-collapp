"""
Security Configuration for Collapp
Centralized security settings and validation
"""
import os
from typing import List, Dict, Any
from pydantic import validator
from pydantic_settings import BaseSettings

class SecuritySettings(BaseSettings):
    """Security configuration settings"""
    
    # Password Policy
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_UPPERCASE: bool = True
    REQUIRE_LOWERCASE: bool = True
    REQUIRE_NUMBERS: bool = True
    REQUIRE_SPECIAL_CHARS: bool = True
    PASSWORD_HISTORY_COUNT: int = 5
    
    # Account Lockout
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 100
    
    # Session Management
    SESSION_TIMEOUT_MINUTES: int = 30
    ABSOLUTE_SESSION_TIMEOUT_HOURS: int = 8
    CONCURRENT_SESSIONS_LIMIT: int = 3
    
    # Token Security
    JWT_SECRET_ROTATION_DAYS: int = 30
    REFRESH_TOKEN_ROTATION: bool = True
    TOKEN_BLACKLIST_ENABLED: bool = True
    
    # Data Protection
    ENCRYPT_PII: bool = True
    DATA_RETENTION_DAYS: int = 365
    AUDIT_LOG_RETENTION_DAYS: int = 2555  # 7 years
    
    # API Security
    API_KEY_REQUIRED: bool = False
    API_RATE_LIMIT_PER_KEY: int = 1000
    CORS_ALLOWED_ORIGINS: List[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "https://collapp.com"
    ]
    
    # File Upload Security
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: List[str] = [
        "image/jpeg", "image/png", "image/gif", "image/webp",
        "application/pdf", "text/plain"
    ]
    SCAN_UPLOADS_FOR_MALWARE: bool = True
    
    # Database Security
    DB_CONNECTION_ENCRYPTION: bool = True
    DB_QUERY_LOGGING: bool = False  # Only in development
    
    # Monitoring and Alerting
    SECURITY_MONITORING_ENABLED: bool = True
    ALERT_ON_SUSPICIOUS_ACTIVITY: bool = True
    ALERT_EMAIL: str = "security@collapp.com"
    
    # Compliance
    GDPR_COMPLIANCE: bool = True
    LGPD_COMPLIANCE: bool = True
    DATA_ANONYMIZATION: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from environment
    
    @validator('CORS_ALLOWED_ORIGINS', pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @validator('ALLOWED_FILE_TYPES', pre=True)
    def parse_file_types(cls, v):
        if isinstance(v, str):
            return [file_type.strip() for file_type in v.split(',')]
        return v

class SecurityValidator:
    """Validate security configurations and requirements"""
    
    def __init__(self, settings: SecuritySettings):
        self.settings = settings
    
    def validate_environment(self) -> Dict[str, Any]:
        """Validate security environment setup"""
        issues = []
        recommendations = []
        
        # Check if running in production
        env = os.getenv("ENVIRONMENT", "development")
        if env == "production":
            # Production-specific checks
            if not os.getenv("SECRET_KEY") or len(os.getenv("SECRET_KEY", "")) < 32:
                issues.append("SECRET_KEY must be at least 32 characters in production")
            
            if not self.settings.DB_CONNECTION_ENCRYPTION:
                issues.append("Database connection encryption should be enabled in production")
            
            if self.settings.DB_QUERY_LOGGING:
                recommendations.append("Disable database query logging in production")
        
        # Check SSL/TLS
        if not os.getenv("SSL_CERT_PATH"):
            recommendations.append("Configure SSL/TLS certificates for HTTPS")
        
        # Check monitoring
        if not self.settings.SECURITY_MONITORING_ENABLED:
            recommendations.append("Enable security monitoring")
        
        return {
            "environment": env,
            "issues": issues,
            "recommendations": recommendations,
            "security_score": self._calculate_security_score(issues, recommendations)
        }
    
    def _calculate_security_score(self, issues: List[str], recommendations: List[str]) -> int:
        """Calculate security score (0-100)"""
        base_score = 100
        base_score -= len(issues) * 20  # Critical issues
        base_score -= len(recommendations) * 5  # Recommendations
        return max(0, base_score)
    
    def get_security_headers(self) -> Dict[str, str]:
        """Get recommended security headers"""
        return {
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' https:; "
                "connect-src 'self' https:; "
                "frame-ancestors 'none';"
            ),
            "Permissions-Policy": (
                "geolocation=(), microphone=(), camera=(), "
                "payment=(), usb=(), magnetometer=(), gyroscope=()"
            )
        }

# Global security settings
security_settings = SecuritySettings()
security_validator = SecurityValidator(security_settings)