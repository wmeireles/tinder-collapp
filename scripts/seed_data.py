#!/usr/bin/env python3
"""
Seed script para dados de teste do Collapp
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.models import User, UserProfile, UserPlan, CollaborationType
from app.core.security import get_password_hash
import uuid

def create_sample_users():
    db = SessionLocal()
    
    try:
        # Sample users data
        users_data = [
            {
                "email": "ana.lifestyle@gmail.com",
                "name": "Ana Silva",
                "bio": "Lifestyle blogger apaixonada por moda sustentável e bem-estar",
                "plan": UserPlan.PRO,
                "profile": {
                    "social_platforms": {
                        "instagram": "@ana_lifestyle",
                        "tiktok": "@ana_sustentavel",
                        "youtube": "Ana Lifestyle"
                    },
                    "follower_counts": {
                        "instagram": 45000,
                        "tiktok": 23000,
                        "youtube": 12000
                    },
                    "content_types": ["lifestyle", "fashion", "sustainability"],
                    "niches": ["moda sustentável", "bem-estar", "lifestyle"],
                    "languages": ["pt", "en"],
                    "country": "BR",
                    "city": "São Paulo",
                    "collaboration_types": [CollaborationType.BRAND_DEAL, CollaborationType.CONTENT_SWAP],
                    "min_followers": 10000
                }
            }
        ]
        
        for user_data in users_data:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if existing_user:
                print(f"User {user_data['email']} already exists, skipping...")
                continue
            
            # Create user
            profile_data = user_data.pop("profile")
            user = User(
                **user_data,
                password_hash=get_password_hash("password123"),
                onboarding_completed=True,
                email_verified=True
            )
            
            db.add(user)
            db.flush()  # Get the user ID
            
            # Create profile
            profile = UserProfile(
                user_id=user.id,
                **profile_data,
                profile_completion_score=85
            )
            
            db.add(profile)
            print(f"Created user: {user.email}")
        
        db.commit()
        print("✅ Sample users created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating sample users: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🌱 Seeding database with sample data...")
    create_sample_users()
    print("🎉 Seeding completed!")