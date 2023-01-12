from fastapi import Depends
from sqlalchemy.orm import Session

from app import schemas
from app.crud.crud_user import get_current_active_user
from app.schemas import CategoryBase
from app.models import Category


def create_user_category(
    db: Session,
    category: CategoryBase,
    user_id: int,
):
    db_category = Category(title=category.title, user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
