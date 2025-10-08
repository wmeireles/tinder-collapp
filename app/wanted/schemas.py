from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class WantedPostCreate(BaseModel):
    title: str
    description: str
    collaboration_type: str
    requirements: Optional[str] = None
    deadline: Optional[datetime] = None
    niches: Optional[List[str]] = []
    platforms: Optional[List[str]] = []
    sizes: Optional[List[str]] = []
    budget: Optional[str] = None
    location: Optional[str] = None

class WantedPostResponse(BaseModel):
    id: str
    title: str
    description: str
    collaboration_type: str
    requirements: Optional[str]
    deadline: Optional[datetime]
    status: str
    author: dict
    created_at: datetime
    niches: Optional[List[str]] = []
    platforms: Optional[List[str]] = []
    sizes: Optional[List[str]] = []
    budget: Optional[str] = None
    location: Optional[str] = None

class WantedApplicationCreate(BaseModel):
    wanted_post_id: str
    message: Optional[str] = None
    
    class Config:
        str_strip_whitespace = True

class WantedApplicationResponse(BaseModel):
    id: str
    wanted_post_id: str
    applicant: dict
    message: Optional[str]
    status: str
    created_at: datetime