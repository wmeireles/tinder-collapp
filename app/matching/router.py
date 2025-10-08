from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.db.database import get_db
from app.db.models import User, UserProfile, Swipe, Match, Chat
from app.matching.schemas import SwipeAction, CreatorCard, MatchResponse
from app.auth.dependencies import get_current_user
from typing import List
import json
import random

router = APIRouter(prefix="/matching", tags=["matching"])

@router.get("/discover", response_model=List[CreatorCard])
def discover_creators(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get users already swiped
    swiped_users = db.query(Swipe.swiped_id).filter(Swipe.swiper_id == current_user.id).subquery()
    
    # Get potential matches (exclude self and already swiped)
    potential_matches = db.query(User, UserProfile).join(UserProfile).filter(
        and_(
            User.id != current_user.id,
            User.onboarding_completed == True,
            ~User.id.in_(swiped_users)
        )
    ).limit(10).all()
    
    cards = []
    for user, profile in potential_matches:
        cards.append(CreatorCard(
            id=str(user.id),
            name=user.name or "Creator",
            bio=user.bio or "",
            profile_photo=user.profile_photo,
            niches=profile.niches or [],
            social_media=profile.social_platforms or {},
            match_percentage=random.randint(60, 95),  # Mock AI calculation
            ai_analysis=f"Great potential for collaboration in {profile.niches[0] if profile.niches else 'content creation'}"
        ))
    
    return cards

@router.post("/swipe")
def swipe_user(swipe: SwipeAction, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from app.db.models import Message
    from datetime import datetime
    import uuid
    
    # Check if already swiped
    existing = db.query(Swipe).filter(
        Swipe.swiper_id == current_user.id,
        Swipe.swiped_id == swipe.swiped_user_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already swiped")
    
    # Record swipe
    new_swipe = Swipe(
        swiper_id=current_user.id,
        swiped_id=swipe.swiped_user_id,
        action=swipe.action
    )
    db.add(new_swipe)
    
    # Check for match if it's a like or boost
    if swipe.action in ["like", "boost"]:
        mutual_like = db.query(Swipe).filter(
            and_(
                Swipe.swiper_id == swipe.swiped_user_id,
                Swipe.swiped_id == current_user.id,
                Swipe.action.in_(["like", "boost"])
            )
        ).first()
        
        if mutual_like:
            # Create match
            match = Match(
                user_a_id=current_user.id,
                user_b_id=swipe.swiped_user_id,
                match_percent=random.randint(70, 95)
            )
            db.add(match)
            db.flush()
            
            # Create chat
            chat = Chat(match_id=match.id)
            db.add(chat)
            db.flush()
            
            # Add boost message if applicable
            if swipe.action == "boost":
                boost_msg = Message(
                    id=str(uuid.uuid4()),
                    chat_id=chat.id,
                    sender_id=current_user.id,
                    content=f"✨ {current_user.name} enviou um Super! Vamos colaborar?",
                    message_type="boost",
                    created_at=datetime.utcnow()
                )
                db.add(boost_msg)
            
            db.commit()
            return {"match": True, "match_id": match.id, "chat_id": chat.id}
    
    db.commit()
    return {"match": False}

@router.get("/matches", response_model=List[MatchResponse])
def get_matches(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    matches = db.query(Match).filter(
        or_(
            Match.user_a_id == current_user.id,
            Match.user_b_id == current_user.id
        )
    ).all()
    
    result = []
    for match in matches:
        other_user_id = match.user_b_id if match.user_a_id == current_user.id else match.user_a_id
        other_user = db.query(User).filter(User.id == other_user_id).first()
        
        result.append(MatchResponse(
            id=str(match.id),
            user_a={"id": str(current_user.id), "name": current_user.name},
            user_b={"id": str(other_user.id), "name": other_user.name},
            match_percent=match.match_percent,
            created_at=match.created_at,
            status=match.status
        ))
    
    return result