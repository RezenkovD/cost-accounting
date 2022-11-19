from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

import src
from src.db.database import get_db


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=src.schemas.user.User)
def create_user(user: src.schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user = src.crud.crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return src.crud.crud_user.create_user(db=db, user=user)


@router.get("/", response_model=list[src.schemas.user.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = src.crud.crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}/", response_model=src.schemas.user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = src.crud.crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
