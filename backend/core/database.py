"""
Database configuration and connection management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator

from backend.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=StaticPool,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """
    Initialize database tables
    """
    # Import all models to register them with SQLAlchemy
    from backend.models import user, portfolio, asset, transaction, strategy
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")