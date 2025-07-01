"""
Books API endpoints for CRUD operations.

This module provides comprehensive REST API endpoints for managing books,
including Create, Read, Update, and Delete operations.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.api import deps
from app.models.book import Book as BookModel
from app.schemas.book import Book as BookSchema, BookCreate, BookUpdate

router = APIRouter()


# CREATE - Add a new book
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


# READ - Get all books with optional filtering
@router.get(
    "/",
    response_model=List[BookSchema],
    summary="Get all books",
    description="Retrieve a list of all books with optional filtering by status and search terms.",
    tags=["Books"]
)
def get_books(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    curation_status: str = Query(None, description="Filter by curation status (pending, approved, rejected, archived)"),
    search: str = Query(None, description="Search in title and author fields"),
    is_active: bool = Query(True, description="Filter by active status (default: only active books)")
) -> List[BookModel]:
    """
    Retrieve books with optional filtering and pagination.

    - **Args**:
        - `skip`: Number of records to skip (for pagination)
        - `limit`: Maximum number of records to return
        - `curation_status`: Filter by specific curation status
        - `search`: Search term for title and author
        - `is_active`: Filter by active status (default: True, only shows active books)

    - **Returns**:
        - `List[BookModel]`: List of book records matching the criteria
    """
    query = db.query(BookModel)
    
    # Filter by active status (default: only active books)
    query = query.filter(BookModel.is_active.is_(is_active))
    
    # Filter by curation status if provided
    if curation_status:
        query = query.filter(BookModel.curation_status == curation_status)
    
    # Search in title and author if search term provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                BookModel.title.ilike(search_term),
                BookModel.author.ilike(search_term)
            )
        )
    
    # Apply pagination and return results
    return query.offset(skip).limit(limit).all()


# READ - Get a specific book by ID
@router.get(
    "/{book_id}",
    response_model=BookSchema,
    summary="Get a book by ID",
    description="Retrieve a specific book by its unique identifier.",
    tags=["Books"]
)
def get_book(
    *,
    db: Session = Depends(deps.get_db),
    book_id: int
) -> BookModel:
    """
    Retrieve a specific book by its ID.

    - **Args**:
        - `book_id`: The unique identifier of the book

    - **Returns**:
        - `BookModel`: The book record if found

    - **Raises**:
        - `HTTPException 404`: If the book is not found
    """
    book = db.query(BookModel).filter(
        BookModel.id == book_id,
        BookModel.is_active.is_(True)
    ).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    
    return book


# UPDATE - Update an existing book
@router.put(
    "/{book_id}",
    response_model=BookSchema,
    summary="Update a book",
    description="Update an existing book's information.",
    tags=["Books"]
)
def update_book(
    *,
    db: Session = Depends(deps.get_db),
    book_id: int,
    book_update: BookUpdate
) -> BookModel:
    """
    Update an existing book record.

    - **Args**:
        - `book_id`: The unique identifier of the book to update
        - `book_update`: The updated book data (partial updates supported)

    - **Returns**:
        - `BookModel`: The updated book record

    - **Raises**:
        - `HTTPException 404`: If the book is not found
    """
    # Find the existing book
    db_book = db.query(BookModel).filter(
        BookModel.id == book_id,
        BookModel.is_active.is_(True)
    ).first()
    
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    
    # Update only the fields that were provided (partial update)
    update_data = book_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    # Commit the changes
    db.commit()
    db.refresh(db_book)
    
    return db_book


# DELETE - Soft delete a book (set is_active to False)
@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
    description="Soft delete a book (marks as inactive rather than permanently deleting).",
    tags=["Books"]
)
def delete_book(
    *,
    db: Session = Depends(deps.get_db),
    book_id: int
) -> None:
    """
    Soft delete a book by setting is_active to False.

    - **Args**:
        - `book_id`: The unique identifier of the book to delete

    - **Returns**:
        - `None`: No content (204 status)

    - **Raises**:
        - `HTTPException 404`: If the book is not found
    """
    # Find the existing book
    db_book = db.query(BookModel).filter(
        and_(
            BookModel.id == book_id,
            BookModel.is_active.is_(True)
        )
    ).first()
    
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    
    # Soft delete by setting is_active to False
    db_book.is_active = False
    
    # Commit the changes
    db.commit()
    
    return None
