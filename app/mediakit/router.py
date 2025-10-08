from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, MediaKit
from app.mediakit.schemas import MediaKitCreate, MediaKitUpdate, MediaKitResponse
from app.auth.dependencies import get_current_user
import json

router = APIRouter(prefix="/mediakit", tags=["mediakit"])

@router.post("/create")
def create_media_kit(
    media_kit: MediaKitCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if user already has a media kit
    existing = db.query(MediaKit).filter(MediaKit.user_id == current_user.id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Media kit already exists. Use update endpoint."
        )
    
    db_media_kit = MediaKit(
        user_id=current_user.id,
        content=media_kit.content,
        statistics=json.dumps(media_kit.statistics) if isinstance(media_kit.statistics, dict) else media_kit.statistics,
        brand_partnerships=json.dumps(media_kit.brand_partnerships) if isinstance(media_kit.brand_partnerships, list) else media_kit.brand_partnerships,
        case_studies=json.dumps(media_kit.case_studies) if isinstance(media_kit.case_studies, list) else media_kit.case_studies,
        is_public=media_kit.is_public
    )
    
    db.add(db_media_kit)
    db.commit()
    db.refresh(db_media_kit)
    
    return db_media_kit

@router.get("/my-mediakit")
def get_my_media_kit(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    media_kit = db.query(MediaKit).filter(MediaKit.user_id == current_user.id).first()
    
    if not media_kit:
        return None
    
    return media_kit

@router.get("/{user_id}", response_model=MediaKitResponse)
def get_user_media_kit(user_id: str, db: Session = Depends(get_db)):
    media_kit = db.query(MediaKit).filter(
        MediaKit.user_id == user_id,
        MediaKit.is_public == True
    ).first()
    
    if not media_kit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media kit not found or not public"
        )
    
    return media_kit

@router.put("/update")
def update_media_kit(
    update_data: MediaKitUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    media_kit = db.query(MediaKit).filter(MediaKit.user_id == current_user.id).first()
    
    if not media_kit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media kit not found"
        )
    
    for field, value in update_data.dict(exclude_unset=True).items():
        if field in ["statistics", "brand_partnerships", "case_studies"] and value is not None:
            if isinstance(value, (dict, list)):
                setattr(media_kit, field, json.dumps(value))
            else:
                setattr(media_kit, field, value)
        else:
            setattr(media_kit, field, value)
    
    db.commit()
    return {"message": "Media kit updated successfully"}