-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Create custom types
CREATE TYPE user_plan AS ENUM ('free', 'pro', 'enterprise');
CREATE TYPE collaboration_type AS ENUM ('brand_deal', 'content_swap', 'joint_project', 'mentorship');
CREATE TYPE social_platform AS ENUM ('instagram', 'tiktok', 'youtube', 'twitter', 'linkedin', 'twitch');

-- Set timezone
SET timezone = 'UTC';