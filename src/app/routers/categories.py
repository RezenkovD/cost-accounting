from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app import schemas
from app.crud import crud_category
from app.db import get_db

router = APIRouter(
    prefix="/users",
    tags=["categories"],
)


@router.post("/category/", response_model=schemas.Category)
def create_category_for_user(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
):
    return crud_category.create_user_category(db=db, category=category)
