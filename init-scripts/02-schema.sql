-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    bio TEXT,
    profile_photo VARCHAR(500),
    onboarding_completed BOOLEAN DEFAULT FALSE,
    plan user_plan DEFAULT 'free',
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User profiles table
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Social media data (JSONB for flexibility)
    social_platforms JSONB DEFAULT '{}',
    follower_counts JSONB DEFAULT '{}',
    engagement_rates JSONB DEFAULT '{}',
    
    -- Content and niche data
    content_types TEXT[] DEFAULT '{}',
    niches TEXT[] DEFAULT '{}',
    languages TEXT[] DEFAULT '{"en"}',
    
    -- Location and demographics
    country VARCHAR(2),
    city VARCHAR(100),
    timezone VARCHAR(50),
    age_range VARCHAR(10),
    
    -- Collaboration preferences
    collaboration_types collaboration_type[] DEFAULT '{}',
    collaboration_goals TEXT,
    min_followers INTEGER DEFAULT 0,
    preferred_brands TEXT[] DEFAULT '{}',
    
    -- Metadata
    profile_completion_score INTEGER DEFAULT 0,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id)
);

-- Performance indexes
CREATE INDEX idx_users_email ON users USING btree(email);
CREATE INDEX idx_users_plan ON users USING btree(plan);
CREATE INDEX idx_users_active ON users USING btree(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_users_created_at ON users USING btree(created_at);

-- Profile indexes for search and filtering
CREATE INDEX idx_profiles_user_id ON user_profiles USING btree(user_id);
CREATE INDEX idx_profiles_niches ON user_profiles USING gin(niches);
CREATE INDEX idx_profiles_content_types ON user_profiles USING gin(content_types);
CREATE INDEX idx_profiles_languages ON user_profiles USING gin(languages);
CREATE INDEX idx_profiles_country ON user_profiles USING btree(country);
CREATE INDEX idx_profiles_collaboration_types ON user_profiles USING gin(collaboration_types);
CREATE INDEX idx_profiles_social_platforms ON user_profiles USING gin(social_platforms);
CREATE INDEX idx_profiles_completion_score ON user_profiles USING btree(profile_completion_score);
CREATE INDEX idx_profiles_last_activity ON user_profiles USING btree(last_activity);

-- Text search indexes
CREATE INDEX idx_users_name_trgm ON users USING gin(name gin_trgm_ops);
CREATE INDEX idx_users_bio_trgm ON users USING gin(bio gin_trgm_ops);

-- Triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();