from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserAdmin(BaseModel):
    id: str
    email: str
    name: Optional[str]
    plan: str
    is_active: bool
    created_at: datetime

class PlatformMetrics(BaseModel):
    total_users: int
    active_users: int
    total_matches: int
    total_collaborations: int