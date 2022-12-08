from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas import UserCreate
from app.models import User
from app.utils import get_password_hash, verify_password


def get_user(db: Session, user_id: int):
    return db.query(User).filter_by(id=user_id).one_or_none()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter_by(email=email).one_or_none()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_username(db: Session, email: str):
    return db.query(User).filter_by(email=email).one_or_none()


def authenticate_user(db: Session, email: str, password: str):
    db_user = get_user_username(db, email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=404, detail="Invalid password")
    return db_user
