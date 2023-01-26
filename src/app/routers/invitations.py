import datetime
from typing import Union

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.crud.crud_invitation import (
    create_invitation,
    get_invitation,
    response_to_invitation,
)
from app.crud.crud_user import get_current_active_user
from app.db.database import get_db
from app import schemas
from app.models.invitation import StatusUser

router = APIRouter(
    prefix="/invitations",
    tags=["invitations"],
)


@router.post("/", response_model=schemas.Invitation)
def create_user_invitation(
    recipient_id: int,
    group_id: int,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Union[schemas.Invitation, HTTPException]:
    invitation = create_invitation(db, current_user.id, recipient_id, group_id)
    if invitation:
        return invitation
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect title or password or the user is already in the group",
        )


@router.get("/invitation-list/", response_model=list[schemas.Invitation])
def get_invitation_list(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> list[schemas.Invitation]:
    list_invitation = get_invitation(db, current_user.id)
    return list_invitation


@router.post("/response-invitation/", response_model=schemas.Invitation)
def response_invitation(
    status_i: StatusUser,
    invitation_id: int,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Union[schemas.Invitation, bool]:
    response = response_to_invitation(db, invitation_id, current_user.id, status_i)
    if response:
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation is not found",
        )
