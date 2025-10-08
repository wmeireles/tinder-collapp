#!/usr/bin/env python3
"""
Script para tornar um usuário admin
Execute: python make_admin.py email@exemplo.com
"""
import sys
import os
sys.path.append('/opt/render/project/src')

from app.db.database import engine
from app.db.models import User
from sqlalchemy.orm import sessionmaker

def make_admin(email: str):
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"❌ Usuário com email {email} não encontrado")
            return
        
        user.is_admin = True
        db.commit()
        
        print(f"✅ Usuário {user.name} ({email}) agora é admin!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python make_admin.py email@exemplo.com")
        sys.exit(1)
    
    email = sys.argv[1]
    make_admin(email)