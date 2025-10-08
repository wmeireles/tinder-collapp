#!/usr/bin/env python3
"""
Script para debug de login
"""
import sys
import os
sys.path.append('/opt/render/project/src')

from app.db.database import engine
from app.db.models import User
from app.core.security import get_password_hash, verify_password
from sqlalchemy.orm import sessionmaker

def debug_login():
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    email = "willianmeireles2021@gmail.com"
    
    try:
        # Verificar se usuário existe
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"❌ Usuário {email} não existe")
            print("Criando usuário...")
            
            user = User(
                email=email,
                password_hash=get_password_hash("123456"),
                name="Willian Meireles",
                is_admin=True,
                is_active=True,
                email_verified=True
            )
            db.add(user)
            db.commit()
            print("✅ Usuário criado com senha: 123456")
            return
        
        print(f"✅ Usuário existe: {user.name}")
        print(f"   Hash atual: {user.password_hash[:50]}...")
        
        # Testar senhas comuns
        test_passwords = ["123456", "password", "admin", "collapp", "willian"]
        
        for pwd in test_passwords:
            if verify_password(pwd, user.password_hash):
                print(f"✅ Senha correta: {pwd}")
                return
        
        print("❌ Nenhuma senha testada funcionou")
        print("Redefinindo senha para '123456'...")
        
        user.password_hash = get_password_hash("123456")
        user.is_admin = True
        db.commit()
        print("✅ Senha redefinida para: 123456")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    debug_login()