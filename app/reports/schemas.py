from pydantic import BaseModel
from typing import List

class EngagementReport(BaseModel):
    likes_received: int
    matches_count: int
    messages_sent: int
    collaborations_completed: int
    profile_views: int

class NetworkingReport(BaseModel):
    connections_made: int
    top_niches: List[str]
    compatibility_score: float
    growth_rate: float