from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.crud import crud_group
from app.crud.crud_group import get_list_users_group
from app.crud.crud_user import get_current_active_user
from app.db.database import get_db
from app import schemas

router = APIRouter(
    prefix="/groups",
    tags=["groups"],
)


@router.post("/", response_model=schemas.Group)
def create_group(
    group: schemas.GroupCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> schemas.Group:
    group = crud_group.create_group(db, group.title, current_user.id)
    return group


@router.get("/{group_id}/", response_model=list[schemas.User])
def read_user_group(
    group_id: int,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> list[schemas.User]:
    list_users = get_list_users_group(db, current_user.id, group_id)
    return list_users
