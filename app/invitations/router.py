from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, Invitation
from app.invitations.schemas import InvitationCreate, InvitationResponse, InvitationUse
from app.auth.dependencies import get_current_user
import secrets
import string

router = APIRouter(prefix="/invitations", tags=["invitations"])

def generate_invite_code():
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))

@router.post("/create", response_model=InvitationResponse)
def create_invitation(
    invitation: InvitationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    invite_code = generate_invite_code()
    
    db_invitation = Invitation(
        inviter_id=current_user.id,
        invite_code=invite_code,
        email=invitation.email,
        status="pending"
    )
    
    db.add(db_invitation)
    db.commit()
    db.refresh(db_invitation)
    
    return db_invitation

@router.get("/my-invitations")
def get_my_invitations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    invitations = db.query(Invitation).filter(
        Invitation.inviter_id == current_user.id
    ).all()
    
    result = []
    for inv in invitations:
        used_by_user = None
        if inv.used_by:
            used_by_user = db.query(User).filter(User.id == inv.used_by).first()
        
        result.append({
            "id": inv.id,
            "invite_code": inv.invite_code,
            "email": inv.email,
            "status": inv.status,
            "used_by": used_by_user.name if used_by_user else None,
            "created_at": inv.created_at,
            "used_at": inv.used_at
        })
    
    return result

@router.post("/use")
def use_invitation(
    invitation_use: InvitationUse,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from datetime import datetime
    
    invitation = db.query(Invitation).filter(
        Invitation.invite_code == invitation_use.invite_code,
        Invitation.status == "pending"
    ).first()
    
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired invitation code"
        )
    
    # Mark invitation as used
    invitation.status = "used"
    invitation.used_by = current_user.id
    invitation.used_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True, 
        "message": "Convite usado! Você e o convidante ganharam créditos.",
        "credits_earned": 50
    }

@router.get("/stats")
def get_invitation_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_sent = db.query(Invitation).filter(Invitation.inviter_id == current_user.id).count()
    accepted = db.query(Invitation).filter(
        Invitation.inviter_id == current_user.id,
        Invitation.status == "used"
    ).count()
    
    credits_earned = accepted * 50
    
    return {
        "total_sent": total_sent,
        "accepted": accepted,
        "pending": total_sent - accepted,
        "credits_earned": credits_earned,
        "share_link": f"https://collapp.com/invite/{current_user.id}"
    }