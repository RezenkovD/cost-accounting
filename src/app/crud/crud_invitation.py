import datetime

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status
import starlette

from app import schemas
from app.crud import get_user
from app.crud.crud_group import add_user_in_group
from app.models import Invitation, UserGroup


def response_to_invitation(
    db: Session,
    invitation_id: int,
    user_id: int,
    status: str,
) -> schemas.Invitation:
    invitation = (
        db.query(Invitation)
        .filter(
            and_(
                Invitation.recipient_id == user_id,
                Invitation.status == "awaiting",
                Invitation.id == invitation_id,
            )
        )
        .one_or_none()
    )
    if invitation is None:
        raise HTTPException(
            status_code=starlette.status.HTTP_404_NOT_FOUND,
            detail="Invitation is not found",
        )
    invitation.status = status
    db.commit()
    if status == "accepted":
        add_user_in_group(db=db, user_id=user_id, group_id=invitation.group_id)
    return invitation


def get_invitation(
    db: Session,
    user_id: int,
) -> list[schemas.Invitation]:
    list_overdue_invitation = (
        db.query(Invitation)
        .filter(
            and_(
                Invitation.recipient_id == user_id,
                Invitation.status == "awaiting",
                Invitation.time + datetime.timedelta(days=1) < datetime.datetime.now(),
            )
        )
        .all()
    )
    for invitation in list_overdue_invitation:
        invitation.status = "overdue"
        db.commit()
    list_invitation = (
        db.query(Invitation)
        .filter(
            and_(Invitation.recipient_id == user_id, Invitation.status == "awaiting")
        )
        .all()
    )
    return list_invitation


def create_invitation(
    db: Session,
    user_id: int,
    recipient_id: int,
    group_id: int,
) -> schemas.Invitation:
    get_user_in_group = (
        db.query(UserGroup)
        .filter(and_(UserGroup.user_id == user_id, UserGroup.group_id == group_id))
        .one_or_none()
    )
    if get_user_in_group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not in this group!",
        )
    if get_user(db, recipient_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not found!",
        )
    get_recipient_in_group = (
        db.query(UserGroup)
        .filter(and_(UserGroup.user_id == recipient_id, UserGroup.group_id == group_id))
        .one_or_none()
    )
    if get_recipient_in_group:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="The recipient is already in this group!",
        )
    get_invitation = (
        db.query(Invitation)
        .filter(
            and_(
                Invitation.status == "awaiting",
                Invitation.recipient_id == recipient_id,
                Invitation.group_id == group_id,
            )
        )
        .one_or_none()
    )
    if get_invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The invitation has already been sent. Wait for a reply!",
        )
    db_invitation = Invitation(
        status="awaiting",
        sender_id=user_id,
        recipient_id=recipient_id,
        group_id=group_id,
        time=datetime.datetime.utcnow(),
    )
    db.add(db_invitation)
    db.commit()
    db.refresh(db_invitation)
    return db_invitation
