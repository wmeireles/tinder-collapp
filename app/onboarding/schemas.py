from pydantic import BaseModel
from typing import List, Optional

class OnboardingStep1(BaseModel):
    name: str
    bio: str
    profile_photo: Optional[str] = None

class OnboardingStep2(BaseModel):
    social_media: dict  # {"instagram": "@user", "youtube": "channel"}
    content_types: List[str]  # ["videos", "photos", "stories"]
    niches: List[str]  # ["travel", "lifestyle", "tech"]

class OnboardingStep3(BaseModel):
    target_audience: str
    location: str
    collaboration_goals: str

class CompleteOnboarding(BaseModel):
    step1: OnboardingStep1
    step2: OnboardingStep2
    step3: OnboardingStep3