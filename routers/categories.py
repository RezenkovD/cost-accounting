from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import crud
import schemas

from db.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["categories"],
)


@router.post("/category/", response_model=schemas.category.Category)
def create_category_for_user(
    category: schemas.category.CategoryCreate,
    db: Session = Depends(get_db),
):
    return crud.crud_category.create_user_category(db=db, category=category)
