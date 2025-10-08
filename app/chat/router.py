from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.db.database import get_db
from app.db.models import User, Chat, Message, Match, WantedPost, WantedApplication
from app.chat.schemas import MessageCreate, MessageResponse, ChatResponse
import logging
from app.auth.dependencies import get_current_user
from typing import List

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/chats", response_model=List[ChatResponse])
def get_user_chats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = []
    
    # Only get chats where current user is involved
    
    # 1. Chats from applications current user made
    applications = db.query(WantedApplication).filter(
        WantedApplication.applicant_id == current_user.id
    ).all()
    
    for app in applications:
        chat = db.query(Chat).filter(Chat.wanted_id == app.wanted_post_id).first()
        if chat:
            wanted_post = db.query(WantedPost).filter(WantedPost.id == app.wanted_post_id).first()
            if wanted_post:
                author = db.query(User).filter(User.id == wanted_post.author_id).first()
                if author:
                    last_message = db.query(Message).filter(
                        Message.chat_id == chat.id
                    ).order_by(Message.created_at.desc()).first()
                    
                    last_msg_response = None
                    if last_message:
                        sender = db.query(User).filter(User.id == last_message.sender_id).first()
                        last_msg_response = MessageResponse(
                            id=str(last_message.id),
                            chat_id=str(last_message.chat_id),
                            sender={"id": str(last_message.sender_id), "name": sender.name if sender else "Usuário"},
                            content=last_message.content,
                            message_type=last_message.message_type,
                            created_at=last_message.created_at
                        )
                    
                    result.append(ChatResponse(
                        id=str(chat.id),
                        match_id=None,
                        wanted_id=wanted_post.id,
                        participants=[
                            {"id": str(current_user.id), "name": current_user.name or "Usuário"},
                            {"id": str(author.id), "name": author.name or "Autor"}
                        ],
                        last_message=last_msg_response,
                        created_at=chat.created_at
                    ))
    
    # 2. Chats from wanted posts current user created (where others applied)
    user_posts = db.query(WantedPost).filter(WantedPost.author_id == current_user.id).all()
    for post in user_posts:
        # Get all applications to this post
        applications_to_post = db.query(WantedApplication).filter(
            WantedApplication.wanted_post_id == post.id
        ).all()
        
        for app in applications_to_post:
            chat = db.query(Chat).filter(Chat.wanted_id == post.id).first()
            if chat:
                applicant = db.query(User).filter(User.id == app.applicant_id).first()
                if applicant:
                    last_message = db.query(Message).filter(
                        Message.chat_id == chat.id
                    ).order_by(Message.created_at.desc()).first()
                    
                    last_msg_response = None
                    if last_message:
                        sender = db.query(User).filter(User.id == last_message.sender_id).first()
                        last_msg_response = MessageResponse(
                            id=str(last_message.id),
                            chat_id=str(last_message.chat_id),
                            sender={"id": str(last_message.sender_id), "name": sender.name if sender else "Usuário"},
                            content=last_message.content,
                            message_type=last_message.message_type,
                            created_at=last_message.created_at
                        )
                    
                    # Avoid duplicates
                    if not any(c.id == str(chat.id) for c in result):
                        result.append(ChatResponse(
                            id=str(chat.id),
                            match_id=None,
                            wanted_id=post.id,
                            participants=[
                                {"id": str(current_user.id), "name": current_user.name or "Usuário"},
                                {"id": str(applicant.id), "name": applicant.name or "Aplicante"}
                            ],
                            last_message=last_msg_response,
                            created_at=chat.created_at
                        ))
    
    return result

@router.post("/messages")
def send_message(message: MessageCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Verify chat exists
        chat = db.query(Chat).filter(Chat.id == message.chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        # Verify user has access to this chat
        has_access = False
        
        if chat.match_id:
            # Check if user is part of the match
            match_id = chat.match_id if isinstance(chat.match_id, str) else str(chat.match_id)
            match = db.query(Match).filter(Match.id == match_id).first()
            if match and (match.user_a_id == current_user.id or match.user_b_id == current_user.id):
                has_access = True
        
        elif chat.wanted_id:
            # Check if user is the author of the wanted post
            wanted_post_id = chat.wanted_id if isinstance(chat.wanted_id, str) else str(chat.wanted_id)
            wanted_post = db.query(WantedPost).filter(WantedPost.id == wanted_post_id).first()
            if wanted_post and wanted_post.author_id == current_user.id:
                has_access = True
            
            # Check if user applied to this wanted post
            application = db.query(WantedApplication).filter(
                WantedApplication.wanted_post_id == wanted_post_id,
                WantedApplication.applicant_id == current_user.id
            ).first()
            if application:
                has_access = True
        
        if not has_access:
            raise HTTPException(status_code=403, detail="Access denied")
        
        new_message = Message(
            chat_id=message.chat_id,
            sender_id=current_user.id,
            content=message.content,
            message_type=message.message_type or "text"
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        
        return {
            "id": str(new_message.id),
            "chat_id": str(new_message.chat_id),
            "sender": {"id": str(current_user.id), "name": current_user.name or "Usuário"},
            "content": new_message.content,
            "message_type": new_message.message_type,
            "created_at": new_message.created_at
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in send_message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/messages/{chat_id}")
def get_chat_messages(chat_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Verify chat exists
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        # Verify user has access to this chat
        has_access = False
        
        if chat.match_id:
            # Check if user is part of the match
            match_id = chat.match_id if isinstance(chat.match_id, str) else str(chat.match_id)
            match = db.query(Match).filter(Match.id == match_id).first()
            if match and (match.user_a_id == current_user.id or match.user_b_id == current_user.id):
                has_access = True
        
        elif chat.wanted_id:
            # Check if user is the author of the wanted post
            wanted_post_id = chat.wanted_id if isinstance(chat.wanted_id, str) else str(chat.wanted_id)
            wanted_post = db.query(WantedPost).filter(WantedPost.id == wanted_post_id).first()
            if wanted_post and wanted_post.author_id == current_user.id:
                has_access = True
            
            # Check if user applied to this wanted post
            application = db.query(WantedApplication).filter(
                WantedApplication.wanted_post_id == wanted_post_id,
                WantedApplication.applicant_id == current_user.id
            ).first()
            if application:
                has_access = True
        
        if not has_access:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get all messages for this chat
        messages = db.query(Message).filter(
            Message.chat_id == chat_id
        ).order_by(Message.created_at.asc()).all()
        
        result = []
        for message in messages:
            sender = db.query(User).filter(User.id == message.sender_id).first()
            result.append({
                "id": str(message.id),
                "chat_id": str(message.chat_id),
                "sender": {"id": str(message.sender_id), "name": sender.name if sender else "Usuário"},
                "content": message.content,
                "message_type": message.message_type,
                "created_at": message.created_at
            })
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in get_chat_messages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{chat_id}")
def get_chat_by_id(chat_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Get chat details
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        participants = []
        
        if chat.match_id:
            # Handle match-based chats
            match_id = chat.match_id if isinstance(chat.match_id, str) else str(chat.match_id)
            match = db.query(Match).filter(Match.id == match_id).first()
            if match:
                user_a = db.query(User).filter(User.id == match.user_a_id).first()
                user_b = db.query(User).filter(User.id == match.user_b_id).first()
                if user_a:
                    participants.append({"id": str(user_a.id), "name": user_a.name or "Usuário"})
                if user_b:
                    participants.append({"id": str(user_b.id), "name": user_b.name or "Usuário"})
        
        elif chat.wanted_id:
            # Handle wanted-based chats
            import uuid
            wanted_post_id = chat.wanted_id if isinstance(chat.wanted_id, str) else str(chat.wanted_id)
            wanted_post = db.query(WantedPost).filter(WantedPost.id == wanted_post_id).first()
            if wanted_post:
                author = db.query(User).filter(User.id == wanted_post.author_id).first()
                application = db.query(WantedApplication).filter(
                    WantedApplication.wanted_post_id == str(wanted_post.id)
                ).first()
                if application:
                    applicant = db.query(User).filter(User.id == application.applicant_id).first()
                    
                    if author:
                        participants.append({"id": str(author.id), "name": author.name or "Autor"})
                    if applicant:
                        participants.append({"id": str(applicant.id), "name": applicant.name or "Aplicante"})
        
        # Get last message
        last_message = db.query(Message).filter(
            Message.chat_id == chat.id
        ).order_by(Message.created_at.desc()).first()
        
        last_msg_response = None
        if last_message:
            sender = db.query(User).filter(User.id == last_message.sender_id).first()
            last_msg_response = {
                "id": str(last_message.id),
                "chat_id": str(last_message.chat_id),
                "sender": {"id": str(last_message.sender_id), "name": sender.name if sender else "Usuário"},
                "content": last_message.content,
                "message_type": last_message.message_type,
                "created_at": last_message.created_at
            }
        
        return {
            "id": str(chat.id),
            "match_id": str(chat.match_id) if chat.match_id else None,
            "wanted_id": str(chat.wanted_id) if chat.wanted_id else None,
            "participants": participants,
            "last_message": last_msg_response,
            "created_at": chat.created_at
        }
    except Exception as e:
        import logging
        logging.error(f"Error in get_chat_by_id: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")