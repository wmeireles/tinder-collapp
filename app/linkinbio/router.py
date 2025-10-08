from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, LinkInBio
from app.linkinbio.schemas import LinkInBioCreate, LinkInBioUpdate, LinkInBioResponse
from app.auth.dependencies import get_current_user
import json

router = APIRouter(prefix="/linkinbio", tags=["linkinbio"])

@router.post("/create", response_model=LinkInBioResponse)
def create_link_in_bio(
    link_data: LinkInBioCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if slug already exists
    existing = db.query(LinkInBio).filter(LinkInBio.slug == link_data.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug already exists"
        )
    
    db_link = LinkInBio(
        user_id=current_user.id,
        slug=link_data.slug,
        title=link_data.title,
        bio=link_data.bio,
        links=json.dumps([link.dict() for link in link_data.links]),
        theme_config=json.dumps(link_data.theme_config)
    )
    
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    return db_link

@router.get("/my-pages")
def get_my_pages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pages = db.query(LinkInBio).filter(LinkInBio.user_id == current_user.id).all()
    return pages

@router.get("/{slug}", response_model=LinkInBioResponse)
def get_link_in_bio(slug: str, db: Session = Depends(get_db)):
    link_page = db.query(LinkInBio).filter(
        LinkInBio.slug == slug,
        LinkInBio.is_active == True
    ).first()
    
    if not link_page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )
    
    return link_page

@router.put("/{slug}")
def update_link_in_bio(
    slug: str,
    update_data: LinkInBioUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    link_page = db.query(LinkInBio).filter(
        LinkInBio.slug == slug,
        LinkInBio.user_id == current_user.id
    ).first()
    
    if not link_page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )
    
    for field, value in update_data.dict(exclude_unset=True).items():
        if field == "links" and value:
            setattr(link_page, field, json.dumps([link.dict() for link in value]))
        elif field == "theme_config" and value:
            setattr(link_page, field, json.dumps(value))
        else:
            setattr(link_page, field, value)
    
    db.commit()
    return {"message": "Page updated successfully"}