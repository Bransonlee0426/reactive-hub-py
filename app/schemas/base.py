"""
Base Pydantic schemas for API request/response validation

This module provides base schema classes for consistent API data validation,
serialization, and response formatting throughout the application.
"""

from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict


# Base response schema for database models
class BaseResponse(BaseModel):
    """
    Base response schema for all database model responses
    
    Includes common fields that all models inherit:
    - id: Primary key
    - created_at: Creation timestamp
    - updated_at: Last update timestamp
    - is_active: Soft delete status
    """
    
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    model_config = ConfigDict(
        from_attributes=True,  # Allow conversion from SQLAlchemy models
        validate_assignment=True,  # Validate on assignment
        use_enum_values=True,  # Use enum values instead of enum objects
    )


# Generic type for paginated responses
T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic paginated response schema
    
    Used for endpoints that return lists of items with pagination information.
    
    Args:
        T: The type of items in the response
        
    Example:
        PaginatedResponse[UserResponse] for paginated user lists
    """
    
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    
    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        size: int
    ) -> "PaginatedResponse[T]":
        """
        Create a paginated response with calculated pages
        
        Args:
            items: List of items for current page
            total: Total number of items across all pages
            page: Current page number (1-based)
            size: Number of items per page
            
        Returns:
            PaginatedResponse instance with calculated pages
        """
        pages = (total + size - 1) // size  # Ceiling division
        
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )


class MessageResponse(BaseModel):
    """
    Simple message response schema
    
    Used for endpoints that only need to return a status message.
    """
    
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """
    Error response schema
    
    Used for consistent error message formatting.
    """
    
    message: str
    error_code: Optional[str] = None
    details: Optional[Any] = None
    success: bool = False


# Base request schemas
class BaseCreate(BaseModel):
    """
    Base schema for create operations
    
    Inherit from this for creating new resources.
    Does not include id, timestamps, or is_active fields.
    """
    
    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        str_strip_whitespace=True,  # Automatically strip whitespace
    )


class BaseUpdate(BaseModel):
    """
    Base schema for update operations
    
    Inherit from this for updating existing resources.
    All fields are optional to support partial updates.
    """
    
    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        extra="ignore",  # Ignore extra fields not defined in schema
    ) 