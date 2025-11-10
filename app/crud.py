# app/crud.py
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from .security import get_password_hash
from typing import Optional, List
from datetime import datetime, timedelta
from . import models, schemas, auth

# ---- User ----
async def get_user_by_username(db: AsyncSession, username: str) -> Optional[models.User]:
    result = await db.execute(select(models.User).where(models.User.username == username))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[models.User]:
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        username=user.username,
        email=user.email,
       hashed_password = auth.get_password_hash(user.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# ---- Author ----
async def create_author(db: AsyncSession, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    await db.commit()
    await db.refresh(db_author)
    return db_author

async def get_author(db: AsyncSession, author_id: int) -> Optional[models.Author]:
    result = await db.execute(
        select(models.Author)
        .where(models.Author.id == author_id)
        .options(selectinload(models.Author.books))
    )
    return result.scalars().first()

async def get_authors(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[models.Author]:
    result = await db.execute(select(models.Author).offset(skip).limit(limit))
    return result.scalars().all()

# ---- Book ----
async def create_book(db: AsyncSession, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def get_book(db: AsyncSession, book_id: int) -> Optional[models.Book]:
    result = await db.execute(select(models.Book).where(models.Book.id == book_id))
    return result.scalars().first()

async def get_books(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    title: Optional[str] = None,
    author_id: Optional[int] = None,
    available: Optional[bool] = None
) -> List[models.Book]:
    query = select(models.Book)
    if title:
        query = query.where(models.Book.title.ilike(f"%{title}%"))
    if author_id:
        query = query.where(models.Book.author_id == author_id)
    if available is not None:
        query = query.where(models.Book.available == available)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def update_book(db: AsyncSession, book_id: int, book_update: schemas.BookUpdate) -> Optional[models.Book]:
    db_book = await get_book(db, book_id)
    if not db_book:
        return None
    for key, value in book_update.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(db_book, key, value)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, book_id: int) -> bool:
    db_book = await get_book(db, book_id)
    if not db_book:
        return False
    await db.delete(db_book)
    await db.commit()
    return True

# ---- Borrowing ----
async def borrow_book(db: AsyncSession, borrow: schemas.BorrowCreate, user_id: int) -> Optional[models.BorrowRecord]:
    # Check if book exists and is available
    result = await db.execute(
        select(models.Book).where(models.Book.id == borrow.book_id)
    )
    book = result.scalars().first()
    if not book:
        raise ValueError("Book not found")
    if not book.available:
        raise ValueError("Book is not available")

    # Create borrow record
    due_date = datetime.utcnow() + timedelta(days=14)
    record = models.BorrowRecord(
        user_id=user_id,
        book_id=borrow.book_id,
        due_date=due_date
    )
    db.add(record)
    # Mark book as unavailable
    book.available = False
    await db.commit()
    await db.refresh(record)
    return record

async def return_book(db: AsyncSession, record_id: int) -> Optional[models.BorrowRecord]:
    result = await db.execute(
        select(models.BorrowRecord).where(models.BorrowRecord.id == record_id)
    )
    record = result.scalars().first()
    if not record:
        return None
    if record.returned_at:
        raise ValueError("Book already returned")

    record.returned_at = datetime.utcnow()
    # Mark book as available
    book_result = await db.execute(
        select(models.Book).where(models.Book.id == record.book_id)
    )
    book = book_result.scalars().first()
    if book:
        book.available = True

    await db.commit()
    await db.refresh(record)
    return record

async def get_borrow_history(db: AsyncSession, user_id: int) -> List[models.BorrowRecord]:
    result = await db.execute(
        select(models.BorrowRecord)
        .where(models.BorrowRecord.user_id == user_id)
        .order_by(models.BorrowRecord.borrowed_at.desc())
    )
    return result.scalars().all()