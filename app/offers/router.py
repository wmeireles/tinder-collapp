from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, Offer, OfferAcceptance
from app.offers.schemas import OfferCreate, OfferUpdate, OfferResponse, OfferAcceptanceCreate, OfferAcceptanceResponse
from app.auth.dependencies import get_current_user
from typing import List
import json

router = APIRouter(prefix="/offers", tags=["offers"])

@router.post("/create", response_model=OfferResponse)
def create_offer(
    offer: OfferCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_offer = Offer(
        creator_id=current_user.id,
        title=offer.title,
        description=offer.description,
        package_details=json.dumps(offer.package_details),
        price=offer.price,
        currency=offer.currency,
        delivery_time=offer.delivery_time,
        status="active"
    )
    
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    
    return db_offer

@router.get("/my-offers", response_model=List[OfferResponse])
def get_my_offers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    offers = db.query(Offer).filter(Offer.creator_id == current_user.id).all()
    return offers

@router.get("/browse", response_model=List[OfferResponse])
def browse_offers(
    db: Session = Depends(get_db),
    limit: int = 20,
    skip: int = 0
):
    offers = db.query(Offer).filter(
        Offer.status == "active"
    ).offset(skip).limit(limit).all()
    
    return offers

@router.get("/{offer_id}", response_model=OfferResponse)
def get_offer(offer_id: str, db: Session = Depends(get_db)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )
    
    return offer

@router.put("/{offer_id}")
def update_offer(
    offer_id: str,
    update_data: OfferUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    offer = db.query(Offer).filter(
        Offer.id == offer_id,
        Offer.creator_id == current_user.id
    ).first()
    
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )
    
    for field, value in update_data.dict(exclude_unset=True).items():
        if field == "package_details" and value:
            setattr(offer, field, json.dumps(value))
        else:
            setattr(offer, field, value)
    
    db.commit()
    return {"message": "Offer updated successfully"}

@router.post("/{offer_id}/accept", response_model=OfferAcceptanceResponse)
def accept_offer(
    offer_id: str,
    acceptance: OfferAcceptanceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.db.models import Chat, Message
    from datetime import datetime
    import uuid
    
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )
    
    if offer.creator_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot accept your own offer"
        )
    
    db_acceptance = OfferAcceptance(
        offer_id=offer_id,
        accepter_id=current_user.id,
        message=acceptance.message,
        status="pending"
    )
    
    db.add(db_acceptance)
    db.flush()
    
    # Create chat for offer discussion
    chat = Chat(
        id=str(uuid.uuid4()),
        created_at=datetime.utcnow()
    )
    db.add(chat)
    db.flush()
    
    # Add initial message
    initial_message = Message(
        id=str(uuid.uuid4()),
        chat_id=chat.id,
        sender_id=current_user.id,
        content=f"💼 Aceitei sua oferta: {offer.title}. {acceptance.message}",
        message_type="offer_acceptance",
        created_at=datetime.utcnow()
    )
    db.add(initial_message)
    
    db.commit()
    db.refresh(db_acceptance)
    
    return db_acceptance