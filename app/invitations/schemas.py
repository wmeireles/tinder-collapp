from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class InvitationCreate(BaseModel):
    email: Optional[EmailStr] = None
    message: Optional[str] = None

class InvitationResponse(BaseModel):
    id: str
    invite_code: str
    email: Optional[str]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class InvitationUse(BaseModel):
    invite_code: str