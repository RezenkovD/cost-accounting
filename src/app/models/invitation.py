from enum import Enum as En
import datetime

from sqlalchemy import Column, Integer, Enum, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class StatusDB(str, En):
    awaiting = "awaiting"
    accepted = "accepted"
    denied = "denied"
    overdue = "overdue"


class StatusUser(str, En):
    accepted = "accepted"
    denied = "denied"


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, Enum(StatusDB), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, index=True, nullable=False)
    group_id = Column(Integer, index=True, nullable=False)
    time = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="invitation")
