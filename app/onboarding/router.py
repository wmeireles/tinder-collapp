from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, UserProfile
from app.onboarding.schemas import OnboardingStep1, OnboardingStep2, OnboardingStep3, CompleteOnboarding
from app.auth.dependencies import get_current_user
import json

router = APIRouter(prefix="/onboarding", tags=["onboarding"])

@router.post("/step1")
def complete_step1(data: OnboardingStep1, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.name = data.name
    current_user.bio = data.bio
    if data.profile_photo:
        current_user.profile_photo = data.profile_photo
    db.commit()
    return {"message": "Step 1 completed"}

@router.post("/step2")
def complete_step2(data: OnboardingStep2, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
    
    profile.social_platforms = data.social_media
    profile.content_types = data.content_types
    profile.niches = data.niches
    db.commit()
    return {"message": "Step 2 completed"}

@router.post("/step3")
def complete_step3(data: OnboardingStep3, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Complete step 2 first")
    
    profile.city = data.location
    profile.collaboration_goals = data.collaboration_goals
    db.commit()
    return {"message": "Step 3 completed"}

@router.post("/complete")
def complete_onboarding(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.onboarding_completed = True
    db.commit()
    return {"message": "Onboarding completed successfully"}

@router.get("/status")
def get_onboarding_status(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    return {
        "onboarding_completed": current_user.onboarding_completed,
        "has_profile": profile is not None,
        "has_basic_info": bool(current_user.name and current_user.bio)
    }