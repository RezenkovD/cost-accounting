from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.crud import crud_user
from app.crud.crud_user import get_current_active_user
from app.db import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/create-user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@router.get("/read-user/", response_model=schemas.User)
def read_user(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@router.get("/read-users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users
