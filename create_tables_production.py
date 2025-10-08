#!/usr/bin/env python3
"""
Script para criar tabelas no PostgreSQL de produção
Execute este script no Render para criar as tabelas
"""
import os
import sys
sys.path.append('/opt/render/project/src')

from app.db.database import engine
from app.db.models import Base

def create_tables():
    print("🔄 Criando tabelas no PostgreSQL...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        
        # Verificar se funcionou
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            print(f"📊 Tabelas criadas: {tables}")
            
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")

if __name__ == "__main__":
    create_tables()