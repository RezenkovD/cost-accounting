from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import crud
import schemas

from db.get_database import get_db


router = APIRouter(
    prefix="/users",
    tags=["items"],
)


@router.post("/{user_id}/item/", response_model=schemas.item.Item)
def create_item_for_user(
    user_id: int, item: schemas.item.ItemCreate, db: Session = Depends(get_db)
):
    return crud.crud_item.create_user_item(db=db, item=item, user_id=user_id)
