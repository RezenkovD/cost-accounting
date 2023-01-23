from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud import get_user, get_user_statistics
from app.models import Group, UsersGroup
from app.schemas.groups import GroupCreate, GroupBase
from app.utils import get_password_hash, verify_password


def get_data_about_all_users_for_group(
    db: Session,
    group: GroupBase,
    user_id: int,
):
    list_user_id = get_list_user_id_for_group(db, group, user_id)
    if list_user_id:
        all_users = []
        for x in list_user_id:
            all_users.append(get_user(db, x))
        return all_users
    else:
        return False


def get_list_user_id_for_group(
    db: Session,
    group: GroupBase,
    user_id: int,
):
    s_group = get_group(db, group.title)
    if s_group is not None:
        user_group = check_user_group(db, user_id, s_group.id)
        if user_group is not None:
            db_query = db.query(UsersGroup).filter_by(group_id=s_group.id).all()
            list_user_id = []
            for x in range(len(db_query)):
                list_user_id.append(db_query[x].user_id)
            return list_user_id
        else:
            return False
    else:
        return False


def create_user_group(
    db: Session,
    group: GroupCreate,
    user_id: int,
):
    s_group = get_group(db, group.title)

    if s_group is not None:
        if not verify_password(group.group_password, s_group.group_password):
            return False
    else:
        s_group = Group(
            title=group.title, group_password=get_password_hash(group.group_password)
        )
        db.add(s_group)
        db.commit()
        db.refresh(s_group)

    user_group = check_user_group(db, user_id, s_group.id)
    if user_group is None:
        db_users_group = UsersGroup(user_id=user_id, group_id=s_group.id)
        db.add(db_users_group)
        db.commit()
        db.refresh(db_users_group)

    return s_group


def get_group(db: Session, title: str):
    return db.query(Group).filter_by(title=title).one_or_none()


def check_user_group(db: Session, user_id: int, group_id: int):
    return (
        db.query(UsersGroup)
        .filter(and_(UsersGroup.user_id == user_id, UsersGroup.group_id == group_id))
        .one_or_none()
    )


def get_users_group_statistics(
    db: Session,
    group: GroupBase,
    user_id: int,
):
    list_id_users_group = get_list_user_id_for_group(db, group, user_id)
    if list_id_users_group:
        list_stats = []
        for x in range(len(list_id_users_group)):
            list_stats.append(get_user_statistics(db, list_id_users_group[x]))
        return list_stats
    else:
        return False
