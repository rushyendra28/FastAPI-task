# app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import List, Optional

# ---- Auth Schemas ----
# app/schemas.py

# app/schemas.py

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # ← input only

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # ← allows ORM → Pydantic mapping

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# ---- Author Schemas ----
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None
    birth_date: Optional[date] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True

class AuthorWithBooks(Author):
    books: List["BookSummary"] = []

# ---- Book Schemas ----
class BookBase(BaseModel):
    title: str
    isbn: Optional[str] = None
    published_date: Optional[date] = None
    description: Optional[str] = None
    available: bool = True
    author_id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    published_date: Optional[date] = None
    description: Optional[str] = None
    available: Optional[bool] = None
    author_id: Optional[int] = None

class BookSummary(BaseModel):
    id: int
    title: str
    available: bool

    class Config:
        from_attributes = True

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True

class BookDetail(Book):
    author: Author

# ---- Borrow Schemas ----
class BorrowRecordBase(BaseModel):
    user_id: int
    book_id: int
    due_date: datetime

class BorrowCreate(BaseModel):
    book_id: int

class BorrowRecord(BorrowRecordBase):
    id: int
    borrowed_at: datetime
    returned_at: Optional[datetime] = None

    class Config:
        from_attributes = True

AuthorWithBooks.model_rebuild()