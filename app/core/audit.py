"""
Security Audit and Logging Module
Tracks security events and user actions
"""
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
from sqlalchemy.orm import Session
from app.db.database import get_db

# Configure security logger
security_logger = logging.getLogger("security")
security_handler = logging.FileHandler("logs/security.log")
security_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
security_handler.setFormatter(security_formatter)
security_logger.addHandler(security_handler)
security_logger.setLevel(logging.INFO)

class SecurityEventType(Enum):
    """Security event types"""
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    PASSWORD_CHANGE = "password_change"
    ACCOUNT_LOCKED = "account_locked"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    PERMISSION_DENIED = "permission_denied"
    API_KEY_USED = "api_key_used"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"

class SecurityAudit:
    """Security audit and logging system"""
    
    @staticmethod
    def log_security_event(
        event_type: SecurityEventType,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """Log security event"""
        event_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type.value,
            "user_id": user_id,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "details": details or {}
        }
        
        security_logger.info(json.dumps(event_data))
    
    @staticmethod
    def log_login_attempt(
        email: str,
        success: bool,
        ip_address: str,
        user_agent: str,
        failure_reason: Optional[str] = None
    ):
        """Log login attempt"""
        event_type = SecurityEventType.LOGIN_SUCCESS if success else SecurityEventType.LOGIN_FAILED
        details = {"email": email}
        if failure_reason:
            details["failure_reason"] = failure_reason
            
        SecurityAudit.log_security_event(
            event_type=event_type,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
    
    @staticmethod
    def log_data_access(
        user_id: str,
        resource: str,
        action: str,
        ip_address: str,
        success: bool = True
    ):
        """Log data access"""
        event_type = SecurityEventType.DATA_ACCESS if success else SecurityEventType.PERMISSION_DENIED
        details = {
            "resource": resource,
            "action": action,
            "success": success
        }
        
        SecurityAudit.log_security_event(
            event_type=event_type,
            user_id=user_id,
            ip_address=ip_address,
            details=details
        )
    
    @staticmethod
    def log_suspicious_activity(
        description: str,
        ip_address: str,
        user_id: Optional[str] = None,
        severity: str = "medium"
    ):
        """Log suspicious activity"""
        details = {
            "description": description,
            "severity": severity
        }
        
        SecurityAudit.log_security_event(
            event_type=SecurityEventType.SUSPICIOUS_ACTIVITY,
            user_id=user_id,
            ip_address=ip_address,
            details=details
        )

# Global audit instance
audit = SecurityAudit()