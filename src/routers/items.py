from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import src
from src.db.database import get_db


router = APIRouter(
    prefix="/users",
    tags=["items"],
)


@router.post("/{user_id}/item/", response_model=src.schemas.item.Item)
def create_item_for_user(
    user_id: int, item: src.schemas.item.ItemCreate, db: Session = Depends(get_db)
):
    return src.crud.crud_item.create_user_item(db=db, item=item, user_id=user_id)
