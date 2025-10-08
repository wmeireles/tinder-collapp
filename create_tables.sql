-- Script para criar tabelas manualmente no PostgreSQL

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    name VARCHAR,
    bio TEXT,
    profile_photo VARCHAR,
    onboarding_completed BOOLEAN DEFAULT FALSE,
    plan VARCHAR DEFAULT 'free',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS profiles (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR REFERENCES users(id),
    social_media TEXT,
    content_types TEXT,
    niches TEXT,
    target_audience VARCHAR,
    location VARCHAR,
    collaboration_goals TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS swipes (
    id VARCHAR PRIMARY KEY,
    swiper_id VARCHAR REFERENCES users(id),
    swiped_id VARCHAR REFERENCES users(id),
    action VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS matches (
    id VARCHAR PRIMARY KEY,
    user_a_id VARCHAR REFERENCES users(id),
    user_b_id VARCHAR REFERENCES users(id),
    match_percent INTEGER,
    status VARCHAR DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chats (
    id VARCHAR PRIMARY KEY,
    match_id VARCHAR REFERENCES matches(id),
    wanted_id VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS messages (
    id VARCHAR PRIMARY KEY,
    chat_id VARCHAR REFERENCES chats(id),
    sender_id VARCHAR REFERENCES users(id),
    content TEXT NOT NULL,
    message_type VARCHAR DEFAULT 'text',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS wanted_posts (
    id VARCHAR PRIMARY KEY,
    author_id VARCHAR REFERENCES users(id),
    title VARCHAR NOT NULL,
    description TEXT NOT NULL,
    collaboration_type VARCHAR NOT NULL,
    requirements TEXT,
    deadline TIMESTAMP WITH TIME ZONE,
    status VARCHAR DEFAULT 'open',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS wanted_applications (
    id VARCHAR PRIMARY KEY,
    wanted_post_id VARCHAR REFERENCES wanted_posts(id),
    applicant_id VARCHAR REFERENCES users(id),
    message TEXT,
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índices para performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_swipes_swiper ON swipes(swiper_id);
CREATE INDEX IF NOT EXISTS idx_matches_users ON matches(user_a_id, user_b_id);
CREATE INDEX IF NOT EXISTS idx_messages_chat ON messages(chat_id);
CREATE INDEX IF NOT EXISTS idx_wanted_author ON wanted_posts(author_id);