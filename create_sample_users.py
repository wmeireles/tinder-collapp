#!/usr/bin/env python3
"""
Script para criar usuários de exemplo com onboarding completo
"""
from sqlalchemy.orm import sessionmaker
from app.db.database import engine
from app.db.models import User, UserProfile, UserPlan
from app.core.security import get_password_hash
import uuid

def create_sample_users():
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    sample_users = [
        {
            "email": "ana@example.com",
            "name": "Ana Silva",
            "bio": "Creator de lifestyle e viagem",
            "niches": ["lifestyle", "travel"],
            "platforms": {"instagram": "ana_lifestyle", "youtube": "AnaViaja"}
        },
        {
            "email": "pedro@example.com", 
            "name": "Pedro Santos",
            "bio": "Tech reviewer e gaming",
            "niches": ["tech", "gaming"],
            "platforms": {"youtube": "PedroTech", "twitch": "pedrogamer"}
        },
        {
            "email": "maria@example.com",
            "name": "Maria Costa",
            "bio": "Food blogger e receitas",
            "niches": ["food", "lifestyle"],
            "platforms": {"instagram": "maria_cozinha", "tiktok": "mariacooks"}
        }
    ]
    
    try:
        for user_data in sample_users:
            # Verificar se já existe
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if existing:
                continue
                
            # Criar usuário
            user = User(
                email=user_data["email"],
                password_hash=get_password_hash("123456"),
                name=user_data["name"],
                bio=user_data["bio"],
                plan=UserPlan.FREE,
                is_active=True,
                onboarding_completed=True
            )
            db.add(user)
            db.flush()
            
            # Criar perfil
            profile = UserProfile(
                user_id=user.id,
                social_platforms=user_data["platforms"],
                niches=user_data["niches"],
                content_types=["posts", "videos"],
                collaboration_types=["content_swap"],
                profile_completion_score=80
            )
            db.add(profile)
            
        db.commit()
        print("✅ Usuários de exemplo criados!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_users()