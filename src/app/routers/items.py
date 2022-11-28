from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.crud import create_user_item
from app import schemas

router = APIRouter(
    prefix="/users",
    tags=["items"],
)


@router.post("/{user_id}/item/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return create_user_item(db=db, item=item, user_id=user_id)
