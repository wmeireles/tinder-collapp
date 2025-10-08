#!/usr/bin/env python3
"""
Script para verificar e corrigir usuário
"""
import sys
import os
sys.path.append('/opt/render/project/src')

from app.db.database import engine
from app.db.models import User
from app.core.security import get_password_hash, verify_password
from sqlalchemy.orm import sessionmaker

def check_user(email: str):
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"❌ Usuário {email} não encontrado")
            print("Criando usuário...")
            
            # Criar usuário com senha padrão
            new_user = User(
                email=email,
                password_hash=get_password_hash("123456"),
                name="Willian Meireles",
                is_admin=True,
                is_active=True,
                email_verified=True
            )
            db.add(new_user)
            db.commit()
            print(f"✅ Usuário criado: {email} / senha: 123456")
            return
        
        print(f"✅ Usuário encontrado: {user.name} ({email})")
        print(f"   - Ativo: {user.is_active}")
        print(f"   - Admin: {getattr(user, 'is_admin', False)}")
        print(f"   - Email verificado: {user.email_verified}")
        
        # Testar senha atual
        test_passwords = ["123456", "password", "admin", "collapp"]
        
        for pwd in test_passwords:
            if verify_password(pwd, user.password_hash):
                print(f"✅ Senha atual: {pwd}")
                return
        
        print("❌ Senha não encontrada, redefinindo para '123456'")
        user.password_hash = get_password_hash("123456")
        user.is_admin = True
        db.commit()
        print("✅ Senha redefinida para: 123456")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    email = "willianmeireles2021@gmail.com"
    check_user(email)