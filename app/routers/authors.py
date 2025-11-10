# app/routers/authors.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud, database, models, auth  # ✅ add models
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# async def get_current_user(
#     token: str = Depends(oauth2_scheme),   # ← MUST be this
#     db: AsyncSession = Depends(database.get_db)
# ):
#     return await auth.get_current_user(token=token, db=db)
router = APIRouter(prefix="/api/v1/authors", tags=["Authors"])



@router.post("/", response_model=schemas.Author, status_code=status.HTTP_201_CREATED)
async def create_author(
    author: schemas.AuthorCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return await crud.create_author(db=db, author=author)

@router.get("/", response_model=List[schemas.Author])
async def read_authors(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return await crud.get_authors(db=db, skip=skip, limit=limit)

@router.get("/{author_id}", response_model=schemas.AuthorWithBooks)
async def read_author(
    author_id: int,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    author = await crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    # Preload books
    # Note: In real app, use joinedload in query for efficiency
    return author