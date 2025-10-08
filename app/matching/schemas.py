from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SwipeAction(BaseModel):
    swiped_user_id: str
    action: str  # "like", "dislike", "boost"

class CreatorCard(BaseModel):
    id: str
    name: str
    bio: str
    profile_photo: Optional[str]
    niches: List[str]
    social_media: dict
    match_percentage: Optional[int]
    ai_analysis: Optional[str]

class MatchResponse(BaseModel):
    id: str
    user_a: dict
    user_b: dict
    match_percent: Optional[int]
    created_at: datetime
    status: str