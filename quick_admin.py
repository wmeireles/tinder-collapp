#!/usr/bin/env python3
import os
from app.db.database import engine
from app.db.models import User
from sqlalchemy.orm import sessionmaker

def make_admin():
    # Substitua pelo seu email
    EMAIL = "willianmeireles2021@gmail.com"
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.email == EMAIL).first()
        if not user:
            print(f"❌ Usuário {EMAIL} não encontrado")
            return
        
        user.is_admin = True
        db.commit()
        
        print(f"✅ {user.name} ({EMAIL}) agora é admin!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    make_admin()