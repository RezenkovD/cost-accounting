from sqlalchemy.orm import Session

import src
from src.schemas.category import CategoryCreate


def create_user_category(db: Session, category: CategoryCreate):
    db_category = src.models.category.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
