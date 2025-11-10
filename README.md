# 📚 Library Management API

A FastAPI-based REST API for managing a digital library — users, authors, books, and borrowing records.

### Explanation
The project follows a clean, modular structure centered around FastAPI’s async capabilities. At the root, configuration files like `.env.example` and `requirements.txt` manage environment and dependencies. The core logic resides in the `app/` directory: `main.py` initializes the FastAPI app and handles startup events (e.g., creating database tables); `database.py` sets up the async SQLAlchemy engine and session; `models.py` defines ORM classes (`User`, `Author`, `Book`, `BorrowRecord`) with relationships; `schemas.py` contains Pydantic models for request/response validation (e.g., `UserCreate`, `UserOut`, `BookDetail`); `security.py` handles password hashing (bcrypt with 72-byte truncation); `auth.py` manages JWT token creation/validation and user dependency injection; `crud.py` encapsulates all database operations; and the `routers/` subdirectory separates concerns into dedicated modules for authentication, authors, books, and borrowing — each applying authentication via `Depends(auth.get_current_user)`. This separation ensures maintainability, testability, and scalability, while leveraging FastAPI’s dependency system for secure, reusable components.

## 🚀 Features
- 🔐 JWT-based authentication (register/login)
- 📝 CRUD for authors & books
- 📖 Borrow/return book tracking
- 🔍 Search & filter books (by title, author, availability)
- 🛡️ Protected endpoints (requires valid token)

## 🛠️ Tech Stack
- **Framework**: FastAPI (async)
- **Database**: PostgreSQL (with SQLAlchemy ORM)
- **Auth**: JWT (HS256), bcrypt hashing
- **Validation**: Pydantic models

---

## 📦 Setup & Run

### Prerequisites
- Python 3.9+
- PostgreSQL (or switch to SQLite — see `database.py`)
- `pip`, `virtualenv`

### 1. Clone & Install
```bash
git clone https://github.com/rushyendra28/library-api.git
cd library-api
python -m venv venv
venv\Scripts\activate  # Windows
# venv/bin/activate    # Linux/macOS
pip install -r requirements.txt

### API testing

curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "buddy",
    "email": "buddy@example.com",
    "password": "SecurePass123!"
  }'

Response:
{
  "id": 1,
  "username": "buddy",
  "email": "buddy@example.com",
  "is_active": true,
  "created_at": "2025-11-10T15:30:45.123456"
}

curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "buddy",
    "password": "SecurePass123!"
  }'

Response:
{
  "access_token": "TOKEN",
  "token_type": "bearer"
}

curl -X POST http://localhost:8000/api/v1/authors/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "J.K. Rowling",
    "bio": "Author of the Harry Potter series",
    "birth_date": "1965-07-31"
  }'

Response:
{
  "id": 1,
  "name": "J.K. Rowling",
  "bio": "Author of the Harry Potter series",
  "birth_date": "1965-07-31"
}

curl -X POST http://localhost:8000/api/v1/books/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Harry Potter and the Philosopher's Stone",
    "isbn": "978-0747532699",
    "published_date": "1997-06-26",
    "description": "The first novel in the Harry Potter series.",
    "available": true,
    "author_id": 1
  }'

Response:
{
  "id": 1,
  "title": "Harry Potter and the Philosopher's Stone",
  "isbn": "978-0747532699",
  "published_date": "1997-06-26",
  "description": "The first novel in the Harry Potter series.",
  "available": true,
  "author_id": 1
}

curl -X POST http://localhost:8000/api/v1/borrow \
  -H "Authorization: Bearer Response" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1
  }'

Response:
{
  "id": 1,
  "user_id": 1,
  "book_id": 1,
  "borrowed_at": "2025-11-10T15:40:12.123456",
  "due_date": "2025-11-24T15:40:12.123456",
  "returned_at": null
}

curl -X POST http://localhost:8000/api/v1/return/1 \
  -H "Authorization: Bearer TOKEN"

Response:
{
  "id": 1,
  "user_id": 1,
  "book_id": 1,
  "borrowed_at": "2025-11-10T15:40:12.123456",
  "due_date": "2025-11-24T15:40:12.123456",
  "returned_at": "2025-11-10T15:45:30.789012"
}

curl -X GET http://localhost:8000/api/v1/borrow/history \
  -H "Authorization: Bearer TOKEN"

[
  {
    "id": 1,
    "user_id": 1,
    "book_id": 1,
    "borrowed_at": "2025-11-10T15:40:12.123456",
    "due_date": "2025-11-24T15:40:12.123456",
    "returned_at": "2025-11-10T15:45:30.789012"
  }
]