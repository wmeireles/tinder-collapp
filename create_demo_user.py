#!/usr/bin/env python3

from app.db.database import get_db
from app.db.models import User
from app.core.security import get_password_hash
import uuid

def create_demo_user():
    """Create demo user for testing"""
    
    db = next(get_db())
    
    # Check if demo user exists
    existing = db.query(User).filter(User.email == "demo@demo.com").first()
    if existing:
        print("Demo user already exists")
        return
    
    # Create demo user
    demo_user = User(
        id=uuid.uuid4(),
        email="demo@demo.com",
        password_hash=get_password_hash("demo123"),
        name="Demo User",
        bio="Demo user for testing",
        onboarding_completed=True,
        is_active=True,
        email_verified=True
    )
    
    db.add(demo_user)
    db.commit()
    print(f"✅ Demo user created: demo@demo.com / demo123")

if __name__ == "__main__":
    create_demo_user()