#!/usr/bin/env python3

from app.db.database import engine
import sqlalchemy as sa

def fix_mediakit_table():
    """Fix media_kits table structure"""
    
    with engine.connect() as conn:
        # Drop and recreate the table with correct structure
        conn.execute(sa.text("DROP TABLE IF EXISTS media_kits CASCADE"))
        
        create_table_sql = """
        CREATE TABLE media_kits (
            id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::text,
            user_id UUID NOT NULL REFERENCES users(id),
            content TEXT NOT NULL,
            statistics TEXT,
            brand_partnerships TEXT,
            case_studies TEXT,
            is_public BOOLEAN DEFAULT true,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        )
        """
        
        conn.execute(sa.text(create_table_sql))
        conn.commit()
        print("✅ media_kits table fixed successfully")

if __name__ == "__main__":
    fix_mediakit_table()