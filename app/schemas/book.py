"""
Book resource Pydantic schemas for API request/response validation

This module provides Pydantic models for Book resource validation,
including schemas for creation requests and API responses.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    """
    Schema for creating a new book
    
    This model validates the JSON data from request body when adding a new book.
    Contains only the fields that users need to provide.
    
    Fields:
        title: Book title (required)
        author: Book author (required) 
        source_url: URL where the book can be found (required)
    """
    
    title: str = Field(
        min_length=1,
        max_length=255,
        description="Book title",
        examples=["The Pragmatic Programmer"]
    )
    
    author: str = Field(
        min_length=1,
        max_length=255,
        description="Book author",
        examples=["Andrew Hunt, David Thomas"]
    )
    
    source_url: str = Field(
        min_length=1,
        max_length=500,
        description="URL where the book can be found",
        examples=["https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/"]
    )
    
    model_config = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True,  # Automatically strip whitespace
        use_enum_values=True
    )


class Book(BookCreate):
    """
    Schema for Book API responses
    
    This model defines the JSON data format returned to users.
    Includes all fields from BookCreate plus database-generated fields.
    
    Inherits:
        All fields from BookCreate (title, author, source_url)
        
    Additional fields:
        id: Database primary key
        curation_status: Status of book curation process
        created_at: When the book record was created
    """
    
    id: int = Field(
        description="Unique identifier for the book",
        examples=[1]
    )
    
    curation_status: str = Field(
        description="Current status of the book curation process",
        examples=["pending"]
    )
    
    created_at: datetime = Field(
        description="Timestamp when the book was added to the system",
        examples=["2024-06-30T10:30:00Z"]
    )
    
    model_config = ConfigDict(
        from_attributes=True,  # Critical: allows reading from SQLAlchemy ORM objects
        validate_assignment=True,
        use_enum_values=True
    ) 