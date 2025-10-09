#!/usr/bin/env python3
"""
Script para criar usuário admin
Email: admin@admin.com
Senha: admin
"""
from sqlalchemy.orm import sessionmaker
from app.db.database import engine
from app.db.models import User
from app.core.security import get_password_hash

def create_admin():
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Verificar se já existe
        existing = db.query(User).filter(User.email == "admin@admin.com").first()
        if existing:
            print("✅ Admin já existe!")
            existing.is_admin = True
            db.commit()
            return
        
        # Criar novo admin
        hashed_password = get_password_hash("admin")
        
        admin_user = User(
            email="admin@admin.com",
            hashed_password=hashed_password,
            name="Admin",
            is_admin=True,
            is_active=True,
            onboarding_completed=True
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✅ Admin criado!")
        print("Email: admin@admin.com")
        print("Senha: admin")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()