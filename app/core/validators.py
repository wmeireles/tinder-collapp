from pydantic import validator
import re
from typing import Any

class ValidationMixin:
    @validator('email', pre=True)
    def validate_email(cls, v):
        if not v:
            return v
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        return v.lower()
    
    @validator('password', pre=True)
    def validate_password(cls, v):
        if not v:
            return v
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain number')
        return v
    
    @validator('slug', pre=True)
    def validate_slug(cls, v):
        if not v:
            return v
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('Slug can only contain lowercase letters, numbers, and hyphens')
        if len(v) < 3 or len(v) > 50:
            raise ValueError('Slug must be between 3 and 50 characters')
        return v
    
    @validator('phone', pre=True)
    def validate_phone(cls, v):
        if not v:
            return v
        phone_regex = r'^\+?1?\d{9,15}$'
        if not re.match(phone_regex, v):
            raise ValueError('Invalid phone number format')
        return v

def sanitize_html(text: str) -> str:
    """Remove HTML tags from text"""
    if not text:
        return text
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def validate_file_size(file_size: int, max_size: int = 5 * 1024 * 1024) -> bool:
    """Validate file size (default 5MB)"""
    return file_size <= max_size

def validate_file_type(filename: str, allowed_types: list = None) -> bool:
    """Validate file type"""
    if not allowed_types:
        allowed_types = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx']
    
    extension = filename.lower().split('.')[-1]
    return extension in allowed_types