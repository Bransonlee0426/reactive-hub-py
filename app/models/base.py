"""
Base SQLAlchemy model for all database tables

This module provides the base model class that all other models inherit from.
It includes common fields like ID, timestamps, and soft delete functionality.
"""

from sqlalchemy import Column, Integer, DateTime, Boolean, func
from app.core.database import Base


class BaseModel(Base):
    """
    Base model class for all database tables
    
    Provides common fields and functionality:
    - Primary key ID
    - Created and updated timestamps
    - Soft delete functionality via is_active field
    """
    
    __abstract__ = True  # This ensures BaseModel won't create a table
    
    # Primary key
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Primary key identifier"
    )
    
    # Timestamp fields
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
        comment="Record creation timestamp"
    )
    
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Record last update timestamp"
    )
    
    # Soft delete functionality
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        index=True,  # Index for faster queries
        comment="Soft delete flag - True: active, False: deleted"
    )
    
    def soft_delete(self):
        """
        Perform soft delete by setting is_active to False
        """
        self.is_active = False
    
    def restore(self):
        """
        Restore soft deleted record by setting is_active to True
        """
        self.is_active = True
    
    def __repr__(self):
        """
        String representation for debugging
        """
        return f"<{self.__class__.__name__}(id={self.id}, active={self.is_active})>" 