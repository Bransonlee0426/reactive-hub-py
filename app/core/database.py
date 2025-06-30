"""
Database configuration and connection management for Reactive Hub API

This module sets up SQLAlchemy engine, session factory, and provides
database connectivity for the application. It includes connection pooling
and session management utilities.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    settings.database_url,
    pool_size=5,                    # Number of connections to maintain in pool
    max_overflow=10,                # Maximum number of connections beyond pool_size
    pool_timeout=30,                # Timeout in seconds for getting connection from pool
    pool_recycle=3600,              # Time in seconds to recycle connections (1 hour)
    echo=settings.debug,            # Log SQL queries when in debug mode
    echo_pool=False,                # Set to True to log connection pool events
)

# Create SessionLocal class for database sessions
# Each instance of SessionLocal will be a database session
SessionLocal = sessionmaker(
    autocommit=False,               # Don't auto-commit transactions
    autoflush=False,                # Don't auto-flush before queries
    bind=engine                     # Bind to our database engine
)

# Create Base class for our models
# All database models will inherit from this Base class
Base = declarative_base()


def get_db():
    """
    Dependency injection function for FastAPI
    
    Provides a database session that automatically closes when done.
    Use this function with FastAPI's Depends() to inject database sessions
    into your route handlers.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables
    
    This function creates all tables defined by our SQLAlchemy models.
    Typically called during application startup.
    """
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """
    Drop all database tables
    
    This function drops all tables. Use with caution!
    Typically used during development or testing.
    """
    Base.metadata.drop_all(bind=engine) 