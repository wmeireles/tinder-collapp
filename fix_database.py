#!/usr/bin/env python3
"""
Script para corrigir estrutura do banco PostgreSQL em produção
"""
import os
from sqlalchemy import create_engine, text
from app.db.models import Base

def fix_database():
    # URL do banco em produção (pegar do Render)
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL não encontrada")
        return
    
    # Corrigir URL para SQLAlchemy 2.0
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    print(f"🔗 Conectando ao banco: {database_url[:50]}...")
    
    try:
        engine = create_engine(database_url)
        
        # Criar todas as tabelas
        print("📊 Criando/atualizando tabelas...")
        Base.metadata.create_all(bind=engine)
        
        # Verificar se tabela users existe
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users'
            """))
            columns = [row[0] for row in result]
            print(f"✅ Colunas da tabela users: {columns}")
            
            if 'password_hash' not in columns:
                print("❌ Coluna password_hash não existe!")
                # Adicionar coluna se não existir
                conn.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)"))
                conn.commit()
                print("✅ Coluna password_hash adicionada!")
            
        print("🎉 Banco de dados corrigido com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    fix_database()