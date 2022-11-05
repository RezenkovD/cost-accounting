from sqlalchemy.orm import Session
from schemas.category import CategoryCreate
import models.category


def create_user_category(db: Session, category: CategoryCreate, user_id: int):
    db_category = models.category.Category(**category.dict())
    db_category.user_id = user_id
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
