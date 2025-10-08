#!/usr/bin/env python3
"""
Setup database tables for Render deployment
"""
import psycopg2
import sys

# Render database URL
# External Database URL for local connections
DATABASE_URL = "postgresql://collapp_db_user:kLtOpKktAQfLLTv0DNCWESwCge3rUgm7@dpg-d3j7al2li9vc73dq7350-a.oregon-postgres.render.com/collapp_db"

def setup_database():
    """Setup database with all tables and data"""
    try:
        print("Connecting to Render database...")
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("Creating extensions...")
        cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        cur.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
        
        print("Creating enum types...")
        cur.execute("DROP TYPE IF EXISTS userplan CASCADE;")
        cur.execute("CREATE TYPE userplan AS ENUM ('free', 'pro', 'pro_plus');")
        
        cur.execute("DROP TYPE IF EXISTS collaborationtype CASCADE;")
        cur.execute("CREATE TYPE collaborationtype AS ENUM ('video', 'photo', 'story', 'reel', 'live', 'podcast', 'blog', 'event');")
        
        print("Creating tables...")
        
        # Users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT true,
            plan userplan DEFAULT 'free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # User profiles table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            full_name VARCHAR(255),
            bio TEXT,
            avatar_url VARCHAR(500),
            social_platforms JSONB DEFAULT '{}',
            content_types TEXT[],
            niches TEXT[],
            audience_size INTEGER DEFAULT 0,
            engagement_rate DECIMAL(5,2) DEFAULT 0.0,
            location VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Test user
        print("Creating test user...")
        cur.execute("""
        INSERT INTO users (email, hashed_password, is_active) 
        VALUES ('test@collapp.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3QJflLxQjm', true)
        ON CONFLICT (email) DO NOTHING;
        """)
        
        conn.commit()
        print("✅ Database setup completed successfully!")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
    
    return True

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)