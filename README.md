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

