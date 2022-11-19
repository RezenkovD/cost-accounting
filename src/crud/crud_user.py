from sqlalchemy.orm import Session
from src.schemas.user import UserCreate
from src.models.user import User
import bcrypt


def get_user(db: Session, user_id: int):
    return db.query(User).filter_by(id=user_id).one_or_none()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter_by(email=email).one_or_none()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    str_password = user.password
    encode_password = str_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(encode_password, salt)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
