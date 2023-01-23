from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.crud import crud_group
from app.crud.crud_user import get_current_active_user
from app.db.database import get_db
from app import schemas

router = APIRouter(
    prefix="/groups",
    tags=["groups"],
)


@router.post("/", response_model=schemas.Group)
def create_group_for_users(
    group: schemas.GroupCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if not crud_group.create_user_group(db, group, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect title or password",
        )
    return crud_group.create_user_group(db, group, current_user.id)


@router.post("/group/", response_model=list[schemas.User])
def read_list_group_users(
    group: schemas.GroupBase,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if not crud_group.get_data_about_all_users_for_group(db, group, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect title or password",
        )
    return crud_group.get_data_about_all_users_for_group(db, group, current_user.id)


@router.post("/group-user-statistics/", response_model=list[schemas.Statistics])
def read_users_group_statistics(
    group: schemas.GroupBase,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    list_users_group = crud_group.get_users_group_statistics(db, group, current_user.id)
    if not list_users_group:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect title or password",
        )
    return list_users_group
