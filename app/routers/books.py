# app/routers/books.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import schemas, crud, database, models, auth

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: schemas.BookCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return await crud.create_book(db=db, book=book)

@router.get("/", response_model=List[schemas.Book])
async def read_books(
    title: Optional[str] = None,
    author_id: Optional[int] = None,
    available: Optional[bool] = None,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return await crud.get_books(
        db=db,
        skip=skip,
        limit=limit,
        title=title,
        author_id=author_id,
        available=available
    )

@router.get("/{book_id}", response_model=schemas.BookDetail)
async def read_book(
    book_id: int,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    book = await crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    # Ensure author is loaded
    await db.refresh(book, ["author"])
    return book

@router.patch("/{book_id}", response_model=schemas.Book)
async def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    updated = await crud.update_book(db=db, book_id=book_id, book_update=book_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    success = await crud.delete_book(db=db, book_id=book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return