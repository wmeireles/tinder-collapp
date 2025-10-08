from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, UserProfile
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/me")
def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "bio": current_user.bio,
        "profile_photo": current_user.profile_photo,
        "created_at": current_user.created_at,
        "onboarding_completed": current_user.onboarding_completed,
        "profile": {
            "social_platforms": profile.social_platforms if profile else {},
            "content_types": profile.content_types if profile else [],
            "niches": profile.niches if profile else [],
            "city": profile.city if profile else None,
            "collaboration_goals": profile.collaboration_goals if profile else None
        } if profile else None
    }

@router.get("/{user_id}")
def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    
    return {
        "id": user.id,
        "name": user.name,
        "bio": user.bio,
        "profile_photo": user.profile_photo,
        "created_at": user.created_at,
        "profile": {
            "social_platforms": profile.social_platforms if profile else {},
            "content_types": profile.content_types if profile else [],
            "niches": profile.niches if profile else [],
            "city": profile.city if profile else None
        } if profile else None
    }