# app/routers/borrow.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud, database, models, auth

router = APIRouter(prefix="/api/v1", tags=["Borrowing"])

@router.post("/borrow", response_model=schemas.BorrowRecord, status_code=status.HTTP_201_CREATED)
async def borrow_book(
    borrow: schemas.BorrowCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    try:
        record = await crud.borrow_book(db=db, borrow=borrow, user_id=current_user.id)
        return record
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/return/{record_id}", response_model=schemas.BorrowRecord)
async def return_book(
    record_id: int,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    try:
        record = await crud.return_book(db=db, record_id=record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Borrow record not found")
        if record.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not your borrow record")
        return record
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/borrow/history", response_model=List[schemas.BorrowRecord])
async def get_borrow_history(
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return await crud.get_borrow_history(db=db, user_id=current_user.id)