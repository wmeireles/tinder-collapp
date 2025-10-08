from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, WantedPost, WantedApplication, Chat, Message
from app.wanted.schemas import WantedPostCreate, WantedPostResponse, WantedApplicationCreate, WantedApplicationResponse
from app.auth.dependencies import get_current_user
from typing import List

router = APIRouter(prefix="/wanted", tags=["wanted"])

@router.post("/posts", response_model=WantedPostResponse)
def create_wanted_post(post: WantedPostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    wanted_post = WantedPost(
        author_id=current_user.id,
        title=post.title,
        description=post.description,
        collaboration_type=post.collaboration_type,
        requirements=post.requirements,
        deadline=post.deadline,
        niches=post.niches,
        platforms=post.platforms,
        sizes=post.sizes,
        budget=post.budget,
        location=post.location
    )
    db.add(wanted_post)
    db.commit()
    db.refresh(wanted_post)
    
    return WantedPostResponse(
        id=wanted_post.id,
        title=wanted_post.title,
        description=wanted_post.description,
        collaboration_type=wanted_post.collaboration_type,
        requirements=wanted_post.requirements,
        deadline=wanted_post.deadline,
        status=wanted_post.status,
        author={"id": current_user.id, "name": current_user.name},
        created_at=wanted_post.created_at,
        niches=wanted_post.niches,
        platforms=wanted_post.platforms,
        sizes=wanted_post.sizes,
        budget=wanted_post.budget,
        location=wanted_post.location
    )

@router.get("/posts", response_model=List[WantedPostResponse])
def get_wanted_posts(db: Session = Depends(get_db)):
    posts = db.query(WantedPost, User).join(User).filter(
        WantedPost.status == "open"
    ).all()
    
    result = []
    for post, author in posts:
        result.append(WantedPostResponse(
            id=post.id,
            title=post.title,
            description=post.description,
            collaboration_type=post.collaboration_type,
            requirements=post.requirements,
            deadline=post.deadline,
            status=post.status,
            author={"id": author.id, "name": author.name},
            created_at=post.created_at,
            niches=post.niches or [],
            platforms=post.platforms or [],
            sizes=post.sizes or [],
            budget=post.budget,
            location=post.location
        ))
    
    return result

@router.post("/applications", response_model=WantedApplicationResponse)
def apply_to_wanted(application: WantedApplicationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Validate input
    if not application.wanted_post_id or not application.wanted_post_id.strip():
        raise HTTPException(status_code=400, detail="wanted_post_id is required")
    
    # Check if post exists
    wanted_post = db.query(WantedPost).filter(WantedPost.id == application.wanted_post_id).first()
    if not wanted_post:
        raise HTTPException(status_code=404, detail="Wanted post not found")
    
    # Check if already applied
    existing = db.query(WantedApplication).filter(
        WantedApplication.wanted_post_id == application.wanted_post_id,
        WantedApplication.applicant_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this post")
    
    # Check if chat already exists for this wanted post and user combination
    existing_chat = db.query(Chat).filter(
        Chat.wanted_id == application.wanted_post_id
    ).first()
    
    if not existing_chat:
        # Create chat only if it doesn't exist
        new_chat = Chat(wanted_id=application.wanted_post_id)
        db.add(new_chat)
        db.flush()  # Get the chat ID
        chat_id = new_chat.id
    else:
        chat_id = existing_chat.id
    
    new_application = WantedApplication(
        wanted_post_id=application.wanted_post_id,
        applicant_id=current_user.id,
        message=application.message
    )
    db.add(new_application)
    
    # Create initial message in chat if there's a message
    if application.message:
        initial_message = Message(
            chat_id=chat_id,
            sender_id=current_user.id,
            content=application.message,
            message_type="text"
        )
        db.add(initial_message)
    
    db.commit()
    db.refresh(new_application)
    
    return {
        "id": new_application.id,
        "wanted_post_id": new_application.wanted_post_id,
        "applicant": {"id": current_user.id, "name": current_user.name},
        "message": new_application.message,
        "status": new_application.status,
        "created_at": new_application.created_at,
        "chat_id": chat_id
    }

@router.get("/my-posts", response_model=List[WantedPostResponse])
def get_my_wanted_posts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    posts = db.query(WantedPost).filter(WantedPost.author_id == current_user.id).all()
    
    result = []
    for post in posts:
        result.append(WantedPostResponse(
            id=post.id,
            title=post.title,
            description=post.description,
            collaboration_type=post.collaboration_type,
            requirements=post.requirements,
            deadline=post.deadline,
            status=post.status,
            author={"id": current_user.id, "name": current_user.name},
            created_at=post.created_at,
            niches=post.niches or [],
            platforms=post.platforms or [],
            sizes=post.sizes or [],
            budget=post.budget,
            location=post.location
        ))
    
    return result

@router.post("/applications/{application_id}/accept")
def accept_application(application_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    application = db.query(WantedApplication, WantedPost).join(WantedPost).filter(
        WantedApplication.id == application_id,
        WantedPost.author_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    app, post = application
    app.status = "accepted"
    
    # Create chat
    chat = Chat(wanted_id=post.id)
    db.add(chat)
    
    db.commit()
    return {"message": "Application accepted", "chat_id": chat.id}