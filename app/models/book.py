"""
Book SQLAlchemy model for database operations

This module defines the Book database model with all required fields
that correspond to the Pydantic schemas.
"""

from sqlalchemy import Column, String, Text
from app.models.base import BaseModel


class Book(BaseModel):
    """
    Book database model
    
    Represents a book record in the database with the following fields:
    - title: Book title (required, max 255 chars)
    - author: Book author (required, max 255 chars)  
    - source_url: URL where book can be found (required, max 500 chars)
    - curation_status: Status of curation process (default: "pending")
    
    Inherits from BaseModel:
    - id: Primary key
    - created_at: Creation timestamp
    - updated_at: Last update timestamp
    - is_active: Soft delete flag
    """
    
    __tablename__ = "books"
    
    # Book specific fields
    title = Column(
        String(255),
        nullable=False,
        index=True,  # Index for search performance
        comment="Book title"
    )
    
    author = Column(
        String(255),
        nullable=False,
        index=True,  # Index for search by author
        comment="Book author"
    )
    
    source_url = Column(
        String(500),
        nullable=False,
        comment="URL where the book can be found"
    )
    
    curation_status = Column(
        String(50),
        nullable=False,
        default="pending",
        index=True,  # Index for filtering by status
        comment="Status of the book curation process"
    )
    
    def __repr__(self):
        """
        String representation for debugging
        """
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}', status='{self.curation_status}')>" 