from sqlalchemy.orm import Session
from sql_app import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_goods(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Goods).offset(skip).limit(limit).all()


def create_user_goods(db: Session, goods: schemas.GoodsCreate, user_id: int):
    db_goods = models.Goods(**goods.dict())
    db_goods.user_id = user_id
    db.add(db_goods)
    db.commit()
    db.refresh(db_goods)
    return db_goods
