from pydantic import BaseModel
from typing import List, Dict, Optional

class LinkItem(BaseModel):
    title: str
    url: str
    icon: Optional[str] = None

class LinkInBioCreate(BaseModel):
    slug: str
    title: str
    bio: Optional[str] = None
    links: List[LinkItem] = []
    theme_config: Optional[Dict] = {}

class LinkInBioUpdate(BaseModel):
    title: Optional[str] = None
    bio: Optional[str] = None
    links: Optional[List[LinkItem]] = None
    theme_config: Optional[Dict] = None
    is_active: Optional[bool] = None

class LinkInBioResponse(BaseModel):
    id: str
    slug: str
    title: str
    bio: Optional[str]
    links: List[Dict]
    theme_config: Dict
    is_active: bool
    
    class Config:
        from_attributes = True