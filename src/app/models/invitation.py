from enum import Enum as En
import datetime

from sqlalchemy import Column, Integer, Enum, DateTime, String

from app.db import Base


class MyEnum(str, En):
    awaiting = "awaiting"
    accepted = "accepted"
    denied = "denied"
    overdue = "overdue"


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, Enum(MyEnum), nullable=False)
    sender_id = Column(Integer, index=True, nullable=False)
    recipient_id = Column(Integer, index=True, nullable=False)
    group_id = Column(Integer, index=True, nullable=False)
    time = Column(DateTime, default=datetime.datetime.utcnow)
