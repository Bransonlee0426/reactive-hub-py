"""
API endpoint for creating books.

This module provides the API endpoint to add a new book to the database.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.book import Book as BookModel
from app.schemas.book import Book as BookSchema, BookCreate

router = APIRouter()


@router.post(
    "/",
    response_model=BookSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
    description="Add a new book to the database.",
    tags=["Books"]
)
def create_book(
    *,
    db: Session = Depends(deps.get_db),
    book_in: BookCreate
) -> BookModel:
    """
    Create a new book record in the database.

    - **Args**:
        - `db (Session)`: The database session, injected by FastAPI.
        - `book_in (BookCreate)`: The book data from the request body, validated by Pydantic.

    - **Returns**:
        - `BookModel`: The newly created book record, which will be serialized into the `BookSchema` format.
    """
    # Create a new SQLAlchemy model instance from the Pydantic schema
    db_book = BookModel(**book_in.model_dump())
    
    # Add the new book to the database session
    db.add(db_book)
    
    # Commit the transaction to save the book to the database
    db.commit()
    
    # Refresh the instance to get the data back from the database,
    # including auto-generated fields like `id` and `created_at`.
    db.refresh(db_book)
    
    return db_book
