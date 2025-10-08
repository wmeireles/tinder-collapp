"""
Security Management Router
Endpoints for security monitoring and management
"""
import time
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.db.database import get_db
from app.auth.security_enhanced import get_current_user_secure
from app.core.security_config import security_validator, security_settings
from app.core.audit import audit, SecurityEventType
from app.core.security_enhanced import security_manager
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/security", tags=["security"])

@router.get("/health")
async def security_health_check():
    """Public security health check"""
    return {
        "status": "secure",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0"
    }

@router.post("/password/validate")
async def validate_password_strength(
    password_data: dict,
    current_user = Depends(get_current_user_secure)
):
    """Validate password strength"""
    password = password_data.get("password", "")
    
    if not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required"
        )
    
    validation_result = security_manager.validate_password_strength(password)
    
    audit.log_security_event(
        SecurityEventType.DATA_ACCESS,
        user_id=str(current_user.id),
        details={"resource": "password_validation", "strength": validation_result["strength"]}
    )
    
    return validation_result

@router.get("/settings")
async def get_security_settings(
    current_user = Depends(get_current_user_secure)
):
    """Get current security settings (non-sensitive)"""
    
    return {
        "password_policy": {
            "min_length": security_settings.MIN_PASSWORD_LENGTH,
            "require_uppercase": security_settings.REQUIRE_UPPERCASE,
            "require_lowercase": security_settings.REQUIRE_LOWERCASE,
            "require_numbers": security_settings.REQUIRE_NUMBERS,
            "require_special_chars": security_settings.REQUIRE_SPECIAL_CHARS
        },
        "session_policy": {
            "timeout_minutes": security_settings.SESSION_TIMEOUT_MINUTES,
            "max_concurrent_sessions": security_settings.CONCURRENT_SESSIONS_LIMIT
        },
        "file_upload": {
            "max_size_mb": security_settings.MAX_FILE_SIZE_MB,
            "allowed_types": security_settings.ALLOWED_FILE_TYPES
        }
    }