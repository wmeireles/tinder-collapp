from pydantic import BaseModel, validator, field_serializer
from typing import Optional, Union
from datetime import datetime
import uuid
import re

class UserCreate(BaseModel):
    email: str
    password: str

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email must contain @')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 3:  # Muito relaxado para teste
            raise ValueError('Password must be at least 3 characters long')
        return v

class UserResponse(BaseModel):
    id: Union[str, uuid.UUID]
    email: str
    name: Optional[str] = None
    plan: Optional[str] = None
    created_at: Optional[datetime] = None

    @field_serializer('id')
    def serialize_id(self, value):
        return str(value)
    
    @field_serializer('created_at')
    def serialize_created_at(self, value):
        return value.isoformat() if value else None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

class PasswordResetRequest(BaseModel):
    email: str

class PasswordReset(BaseModel):
    token: str
    new_password: str