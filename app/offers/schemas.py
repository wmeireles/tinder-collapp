from pydantic import BaseModel, field_validator
from typing import Dict, Optional, Union
from datetime import datetime
import json
import uuid

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
    
    @field_validator('creator_id', mode='before')
    @classmethod
    def convert_uuid_to_str(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    @field_validator('package_details', mode='before')
    @classmethod
    def parse_package_details(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return {}
        return v or {}
    
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
    
    @field_validator('accepter_id', mode='before')
    @classmethod
    def convert_uuid_to_str(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True