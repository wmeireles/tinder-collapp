from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from app.db.database import get_db
from app.db.models import User, Match, Message, Swipe, WantedApplication
from app.auth.dependencies import get_current_user
from app.reports import schemas
from datetime import datetime, timedelta

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/engagement", response_model=schemas.EngagementReport)
def get_engagement_report(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get real stats from database
    likes_received = db.query(Swipe).filter(
        Swipe.swiped_id == current_user.id,
        Swipe.action.in_(['like', 'boost'])
    ).count()
    
    matches_count = db.query(Match).filter(
        or_(Match.user_a_id == current_user.id, Match.user_b_id == current_user.id)
    ).count()
    
    messages_sent = db.query(Message).filter(Message.sender_id == current_user.id).count()
    
    profile_views = db.query(Swipe).filter(Swipe.swiped_id == current_user.id).count()
    
    return schemas.EngagementReport(
        likes_received=likes_received,
        matches_count=matches_count,
        messages_sent=messages_sent,
        collaborations_completed=matches_count,  # Simplified
        profile_views=profile_views
    )

@router.get("/networking", response_model=schemas.NetworkingReport)
def get_networking_report(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    connections_made = db.query(Match).filter(
        or_(Match.user_a_id == current_user.id, Match.user_b_id == current_user.id)
    ).count()
    
    # Mock top niches and scores
    top_niches = ["Tech", "Lifestyle", "Business"]
    compatibility_score = 85.5
    growth_rate = 12.3
    
    return schemas.NetworkingReport(
        connections_made=connections_made,
        top_niches=top_niches,
        compatibility_score=compatibility_score,
        growth_rate=growth_rate
    )

@router.get("/dashboard")
def get_dashboard_stats(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    # Last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    recent_matches = db.query(Match).filter(
        or_(Match.user_a_id == current_user.id, Match.user_b_id == current_user.id),
        Match.created_at >= thirty_days_ago
    ).count()
    
    recent_messages = db.query(Message).filter(
        Message.sender_id == current_user.id,
        Message.created_at >= thirty_days_ago
    ).count()
    
    total_swipes = db.query(Swipe).filter(
        Swipe.swiper_id == current_user.id,
        Swipe.action.in_(['like', 'boost'])
    ).count()
    
    total_matches = db.query(Match).filter(
        or_(Match.user_a_id == current_user.id, Match.user_b_id == current_user.id)
    ).count()
    
    match_rate = (total_matches / max(total_swipes, 1)) * 100 if total_swipes > 0 else 0
    
    return {
        "recent_matches": recent_matches,
        "recent_messages": recent_messages,
        "match_rate": round(match_rate, 1),
        "total_profile_views": db.query(Swipe).filter(Swipe.swiped_id == current_user.id).count(),
        "response_rate": 85.5,
        "avg_response_time": "2h 15min"
    }