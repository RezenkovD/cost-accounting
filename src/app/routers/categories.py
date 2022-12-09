from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app import schemas
from app.crud import crud_category
from app.crud.crud_user import get_current_active_user
from app.db import get_db

router = APIRouter(
    prefix="/users",
    tags=["categories"],
)


@router.post("/create-category/", response_model=schemas.Category)
def create_category_for_user(
    category: schemas.CategoryBase,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return crud_category.create_user_category(db, category, current_user)
