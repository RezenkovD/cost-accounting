from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import src
from src.db.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["categories"],
)


@router.post("/category/", response_model=src.schemas.category.Category)
def create_category_for_user(
    category: src.schemas.category.CategoryCreate,
    db: Session = Depends(get_db),
):
    return src.crud.crud_category.create_user_category(db=db, category=category)
