from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.crud.crud_user import get_current_user
from app.models.category import Category
from app.schemas.item import ItemCreate
from app.models import Item, User


def read_items_for_user(db: Session, current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    return db.query(Item).filter_by(user_id=user_id).all()


def create_user_item(
    db: Session,
    item: ItemCreate,
    user_id: int,
):
    db_item = Item(**item.dict())
    db_item.user_id = user_id

    users = (
        db.query(User)
        .join(Category, Category.user_id == User.id)
        .filter(Category.id == db_item.category_id)
        .all()
    )
    if len(users) == 0:
        raise HTTPException(
            status_code=404, detail="Invalid Category ID. None of the users have it."
        )
    elif len(users) > 1:
        raise HTTPException(
            status_code=404, detail="Several users have the same category."
        )
    else:
        user = users[0]
    if user.id == db_item.user_id:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    else:
        raise HTTPException(
            status_code=404, detail="The user is not the owner of this category."
        )
