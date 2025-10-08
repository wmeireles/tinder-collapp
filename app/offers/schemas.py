from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class OfferCreate(BaseModel):
    title: str
    description: str
    package_details: Dict = {}
    price: Optional[float] = None
    currency: str = "USD"
    delivery_time: int  # days

class OfferUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    package_details: Optional[Dict] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    delivery_time: Optional[int] = None
    status: Optional[str] = None

class OfferResponse(BaseModel):
    id: str
    creator_id: str
    title: str
    description: str
    package_details: Dict
    price: Optional[float]
    currency: str
    delivery_time: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class OfferAcceptanceCreate(BaseModel):
    offer_id: str
    message: Optional[str] = None

class OfferAcceptanceResponse(BaseModel):
    id: str
    offer_id: str
    accepter_id: str
    message: Optional[str]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True