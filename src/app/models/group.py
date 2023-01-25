from sqlalchemy import Column, Integer, String

from app.db import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)


class UserGroup(Base):
    __tablename__ = "user_group"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    group_id = Column(Integer, index=True, nullable=False)
