from typing import Optional

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status
from pydantic.schema import date

from app.crud import get_user, get_user_statistics
from app.models import Group, UserGroup


def create_group(
    db: Session,
    group_title: str,
    user_id: int,
) -> Group:
    db_group = Group(title=group_title)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    add_user_in_group(db, user_id, db_group.id)
    return db_group


def add_user_in_group(
    db: Session,
    user_id: int,
    group_id: int,
) -> None:
    db_user_group = UserGroup(user_id=user_id, group_id=group_id)
    db.add(db_user_group)
    db.commit()
    db.refresh(db_user_group)


def get_list_users_group(
    db: Session,
    user_id: int,
    group_id: int,
) -> list:
    try:
        get_user_in_group = (
            db.query(UserGroup)
            .filter(and_(UserGroup.user_id == user_id, UserGroup.group_id == group_id))
            .one()
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not in this group!",
        )
    group_id = get_user_in_group.group_id
    db_query = db.query(UserGroup).filter_by(group_id=group_id).all()
    list_user_groups_id = [x.user_id for x in db_query]
    list_data_user_group = [get_user(db, x) for x in list_user_groups_id]
    return list_data_user_group


def get_list_groups(
    db: Session,
    user_id: int,
) -> list:
    list_user_groups_id = db.query(UserGroup).filter_by(user_id=user_id).all()
    list_user_groups_id = [x.group_id for x in list_user_groups_id]
    list_user_groups = [
        db.query(Group).filter_by(id=x).one() for x in list_user_groups_id
    ]
    return list_user_groups


def get_group_statistics(
    db: Session, user_id: int, group_id: int, filter_date: Optional[date] = None
) -> list:
    try:
        get_user_in_group = (
            db.query(UserGroup)
            .filter(and_(UserGroup.user_id == user_id, UserGroup.group_id == group_id))
            .one()
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not in this group!",
        )
    group_id = get_user_in_group.group_id
    db_query = db.query(UserGroup).filter_by(group_id=group_id).all()
    list_user_groups_id = [x.user_id for x in db_query]
    list_stats = [get_user_statistics(db, x, filter_date) for x in list_user_groups_id]
    return list_stats
