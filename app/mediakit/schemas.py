from pydantic import BaseModel
from typing import Dict, List, Optional

class MediaKitCreate(BaseModel):
    content: str
    statistics: Dict = {}
    brand_partnerships: List[str] = []
    case_studies: List[Dict] = []
    is_public: bool = True

class MediaKitUpdate(BaseModel):
    content: Optional[str] = None
    statistics: Optional[Dict] = None
    brand_partnerships: Optional[List[str]] = None
    case_studies: Optional[List[Dict]] = None
    is_public: Optional[bool] = None

class MediaKitResponse(BaseModel):
    id: str
    user_id: str
    content: str
    statistics: str  # JSON string
    brand_partnerships: str  # JSON string
    case_studies: str  # JSON string
    is_public: bool
    
    class Config:
        from_attributes = True