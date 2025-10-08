import uuid
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Boolean, Float, Enum, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

class UserPlan(enum.Enum):
    FREE = "FREE"
    PRO = "PRO"
    ENTERPRISE = "ENTERPRISE"

class CollaborationType(enum.Enum):
    BRAND_DEAL = "brand_deal"
    CONTENT_SWAP = "content_swap"
    JOINT_PROJECT = "joint_project"
    MENTORSHIP = "mentorship"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100))
    bio = Column(Text)
    profile_photo = Column(String(500))
    onboarding_completed = Column(Boolean, default=False)
    plan = Column(Enum(UserPlan), default=UserPlan.FREE)
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    # Social media data
    social_platforms = Column(JSONB, default={})
    follower_counts = Column(JSONB, default={})
    engagement_rates = Column(JSONB, default={})
    
    # Content and niche data
    content_types = Column(ARRAY(String), default=[])
    niches = Column(ARRAY(String), default=[])
    languages = Column(ARRAY(String), default=["en"])
    
    # Location and demographics
    country = Column(String(2))
    city = Column(String(100))
    timezone = Column(String(50))
    age_range = Column(String(10))
    
    # Collaboration preferences
    collaboration_types = Column(ARRAY(Enum(CollaborationType)), default=[])
    collaboration_goals = Column(Text)
    min_followers = Column(Integer, default=0)
    preferred_brands = Column(ARRAY(String), default=[])
    
    # Metadata
    profile_completion_score = Column(Integer, default=0)
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profile")

# Removido - substituído por UserProfile acima

class Swipe(Base):
    __tablename__ = "swipes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    swiper_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    swiped_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)  # like, dislike, boost
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Match(Base):
    __tablename__ = "matches"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_a_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user_b_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    match_percent = Column(Integer)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Chat(Base):
    __tablename__ = "chats"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    match_id = Column(String, ForeignKey("matches.id"))
    wanted_id = Column(String, ForeignKey("wanted_posts.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_id = Column(String, ForeignKey("chats.id"), nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String, default="text")  # text, file, link
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WantedPost(Base):
    __tablename__ = "wanted_posts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    collaboration_type = Column(String, nullable=False)
    requirements = Column(Text)
    deadline = Column(DateTime)
    status = Column(String, default="open")
    niches = Column(ARRAY(String), default=[])
    platforms = Column(ARRAY(String), default=[])
    sizes = Column(ARRAY(String), default=[])
    budget = Column(String)
    location = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WantedApplication(Base):
    __tablename__ = "wanted_applications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    wanted_post_id = Column(String, ForeignKey("wanted_posts.id"), nullable=False)
    applicant_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    message = Column(Text)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LinkInBio(Base):
    __tablename__ = "link_in_bio"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    slug = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    bio = Column(Text)
    theme_config = Column(Text)  # JSON string
    links = Column(Text)  # JSON string
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class MediaKit(Base):
    __tablename__ = "media_kits"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    statistics = Column(Text)  # JSON string
    brand_partnerships = Column(Text)  # JSON string
    case_studies = Column(Text)  # JSON string
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Offer(Base):
    __tablename__ = "offers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    package_details = Column(Text)  # JSON string
    price = Column(Float)
    currency = Column(String, default="USD")
    delivery_time = Column(Integer)  # days
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OfferAcceptance(Base):
    __tablename__ = "offer_acceptances"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    offer_id = Column(String, ForeignKey("offers.id"), nullable=False)
    accepter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    message = Column(Text)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    inviter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    invite_code = Column(String, unique=True, nullable=False)
    email = Column(String)
    status = Column(String, default="pending")
    used_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    used_at = Column(DateTime)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    achievement_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    plan = Column(String, nullable=False)
    stripe_subscription_id = Column(String)
    status = Column(String, nullable=False)
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())