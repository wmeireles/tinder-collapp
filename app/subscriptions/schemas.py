from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubscriptionCreate(BaseModel):
    plan: str  # free, pro, enterprise
    stripe_subscription_id: Optional[str] = None

class SubscriptionResponse(BaseModel):
    id: str
    user_id: str
    plan: str
    status: str
    current_period_start: Optional[datetime]
    current_period_end: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class PlanFeatures(BaseModel):
    name: str
    price: float
    features: list
    limits: dict