# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, crud, auth, database
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta  # ✅ Add this line


router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def register(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(database.get_db)
):
    try:
        db_user = await crud.create_user(db=db, user=user)
        return db_user
    except IntegrityError as e:
        # Check if it's email or username duplicate
        if "ix_users_email" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        elif "ix_users_username" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        else:
            raise  # re-raise unknown DB errors
@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: schemas.UserCreate,  # Reusing for simplicity; better: OAuth2PasswordRequestForm
    db: AsyncSession = Depends(database.get_db)
):
    user = await auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}