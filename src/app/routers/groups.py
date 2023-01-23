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


@router.post("/create-group/", response_model=schemas.Group)
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


@router.post("/get-group/", response_model=list[schemas.User])
def get_list_group_users(
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
