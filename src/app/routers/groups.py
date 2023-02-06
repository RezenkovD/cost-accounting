from typing import Optional

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.crud import crud_group
from app.crud.crud_group import get_list_users_group, get_list_groups
from app.crud.crud_user import get_current_active_user
from app.db.database import get_db
from app import schemas
from app.utils import transform_date_or_422

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


@router.get("/group/{group_id}/", response_model=list[schemas.User])
def read_user_group(
    group_id: int,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> list[schemas.User]:
    list_users = get_list_users_group(db, current_user.id, group_id)
    return list_users


@router.get("/list-groups/", response_model=list[schemas.Group])
def read_list_groups(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> list[schemas.Group]:
    list_groups = get_list_groups(db, current_user.id)
    return list_groups


@router.get("/group-statistics/", response_model=list[schemas.Statistics])
def read_users_group_statistics(
    group_id: int,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    filter_date: Optional[str] = None,
) -> list[schemas.Statistics]:
    date_ = None
    if filter_date is not None:
        date_ = transform_date_or_422(filter_date)
    list_users_group = crud_group.get_group_statistics(
        db, current_user.id, group_id, date_
    )
    return list_users_group
