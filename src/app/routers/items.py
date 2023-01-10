from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.crud.crud_user import get_current_active_user
from app.db.database import get_db
from app.crud import create_user_item
from app import schemas

router = APIRouter(
    prefix="/users",
    tags=["items"],
)


@router.post("/create-item/", response_model=schemas.Item)
def create_item_for_user(
    item: schemas.ItemCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return create_user_item(db, item, current_user.id)
