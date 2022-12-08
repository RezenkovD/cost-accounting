from sqlalchemy.orm import Session

from app.schemas import CategoryCreate
from app.models import Category


def create_user_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
