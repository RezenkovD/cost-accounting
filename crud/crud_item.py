from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.item import ItemCreate
import models.item
from crud.crud_user import get_user


def create_user_item(db: Session, item: ItemCreate, user_id: int):
    if get_user(db, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_item = models.item.Item(**item.dict())
    db_item.user_id = user_id
    if db_item.user_id == db_item.category_id:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    else:
        raise HTTPException(status_code=404, detail="You have no such category")
