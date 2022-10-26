from sqlalchemy.orm import Session
from schemas.item import ItemCreate
import models.item


def get_item(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.item.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: ItemCreate, user_id: int):
    db_item = models.item.Item(**item.dict())
    db_item.user_id = user_id
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
