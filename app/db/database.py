from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Database URL with fallback
DATABASE_URL = settings.DATABASE_URL or "postgresql://collapp_db_user:kLtOpKktAQfLLTv0DNCWESwCge3rUgm7@dpg-d3j7al2li9vc73dq7350-a/collapp_db"

# Sync engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    echo=settings.DEBUG,
    connect_args={
        "client_encoding": "utf8",
        "application_name": "collapp_backend"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for sync database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Async functionality removed for deployment simplicity

def check_db_connection():
    """Health check for database connection"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False