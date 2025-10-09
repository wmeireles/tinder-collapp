from sqlalchemy.orm import Session
from app.db.models import User
from app.auth.schemas import UserCreate
from app.core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    from app.db.models import UserPlan
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email, 
        password_hash=hashed_password,
        plan=UserPlan.FREE,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        return False
    return user

def update_user_password(db: Session, user: User, new_password: str):
    user.password_hash = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return user