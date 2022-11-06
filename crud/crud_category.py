from sqlalchemy.orm import Session
from schemas.category import CategoryCreate
import models.category


def create_user_category(db: Session, category: CategoryCreate):
    db_category = models.category.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
