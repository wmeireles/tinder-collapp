from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from app.db.database import get_db
from app.db.models import User, Match, Message, Swipe, WantedPost
from app.auth.dependencies import get_current_user, get_admin_user
from app.admin import schemas
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin", tags=["admin"])

def check_admin(current_user):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Admin access required")

@router.get("/users")
def get_all_users(db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    
    users = db.query(User).order_by(User.created_at.desc()).limit(100).all()
    result = []
    
    for user in users:
        matches_count = db.query(Match).filter(
            or_(Match.user_a_id == user.id, Match.user_b_id == user.id)
        ).count()
        
        messages_count = db.query(Message).filter(Message.sender_id == user.id).count()
        
        result.append({
            "id": str(user.id),
            "name": user.name or "Usuário",
            "email": user.email,
            "plan": user.plan.value if user.plan else "FREE",
            "is_admin": user.is_admin,
            "is_active": user.is_active,
            "onboarding_completed": user.onboarding_completed,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "matches_count": matches_count,
            "messages_count": messages_count,
            "avatar": "/placeholder-avatar.svg",
            "handle": user.email.split('@')[0]
        })
    
    return result

@router.get("/metrics", response_model=schemas.PlatformMetrics)
def get_platform_metrics(db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    
    total_users = db.query(User).count()
    
    # Active users (created in last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    active_users = db.query(User).filter(User.created_at >= thirty_days_ago).count()
    
    total_matches = db.query(Match).count()
    total_collaborations = db.query(WantedPost).count()
    
    return schemas.PlatformMetrics(
        total_users=total_users,
        active_users=active_users,
        total_matches=total_matches,
        total_collaborations=total_collaborations
    )

@router.post("/moderate/user/{user_id}")
def moderate_user(user_id: str, action: str, db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if action == "suspend":
        user.is_active = False
    elif action == "activate":
        user.is_active = True
    
    db.commit()
    return {"success": True, "message": f"User {action}d successfully"}

@router.post("/feature/user/{user_id}")
def feature_user(user_id: str, db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    return {"success": True, "message": f"User {user_id} featured"}

@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db), admin_user = Depends(get_admin_user)):
    
    today = datetime.utcnow().date()
    today_start = datetime.combine(today, datetime.min.time())
    
    new_users_today = db.query(User).filter(User.created_at >= today_start).count()
    new_matches_today = db.query(Match).filter(Match.created_at >= today_start).count()
    
    return {
        "new_users_today": new_users_today,
        "new_matches_today": new_matches_today,
        "total_users": db.query(User).count(),
        "total_matches": db.query(Match).count(),
        "total_messages": db.query(Message).count()
    }