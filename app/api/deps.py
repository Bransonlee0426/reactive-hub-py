"""
API dependencies for FastAPI dependency injection

This module provides reusable dependencies for API endpoints including
database sessions, pagination parameters, and other common functionality.
"""

from typing import Generator
from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency
    
    Provides a database session for API endpoints with automatic cleanup.
    This is the primary way to access the database in API endpoints.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        @app.get("/users/")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    finally:
        db.close()


def get_pagination_params(
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    size: int = Query(10, ge=1, le=100, description="Items per page (max 100)")
) -> dict:
    """
    Pagination parameters dependency
    
    Provides standardized pagination parameters for list endpoints.
    
    Args:
        page: Page number (minimum 1)
        size: Items per page (minimum 1, maximum 100)
        
    Returns:
        dict: Dictionary with 'page', 'size', 'skip', and 'limit' values
        
    Example:
        @app.get("/users/")
        def get_users(
            pagination: dict = Depends(get_pagination_params),
            db: Session = Depends(get_db)
        ):
            skip = pagination["skip"]
            limit = pagination["limit"]
            return db.query(User).offset(skip).limit(limit).all()
    """
    skip = (page - 1) * size
    
    return {
        "page": page,
        "size": size,
        "skip": skip,
        "limit": size
    }


class CommonQueryParams:
    """
    Common query parameters for filtering and searching
    
    This class can be used as a dependency to provide common
    query parameters across multiple endpoints.
    """
    
    def __init__(
        self,
        search: str = Query(None, description="Search term"),
        active_only: bool = Query(True, description="Filter only active records"),
        order_by: str = Query("id", description="Field to order by"),
        order_desc: bool = Query(False, description="Order in descending order")
    ):
        self.search = search
        self.active_only = active_only
        self.order_by = order_by
        self.order_desc = order_desc


def check_database_connection(db: Session = Depends(get_db)) -> bool:
    """
    Database connection health check dependency
    
    Verifies that the database connection is working properly.
    
    Args:
        db: Database session
        
    Returns:
        bool: True if database is connected and responsive
        
    Raises:
        HTTPException: If database connection fails
    """
    try:
        # Simple query to test database connection
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return True
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {str(e)}"
        ) 