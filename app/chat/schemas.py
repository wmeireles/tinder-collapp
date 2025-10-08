from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageCreate(BaseModel):
    chat_id: str
    content: str
    message_type: str = "text"

class MessageResponse(BaseModel):
    id: str
    chat_id: str
    sender: dict
    content: str
    message_type: str
    created_at: datetime

class ChatResponse(BaseModel):
    id: str
    match_id: Optional[str]
    wanted_id: Optional[str]
    participants: List[dict]
    last_message: Optional[MessageResponse]
    created_at: datetime