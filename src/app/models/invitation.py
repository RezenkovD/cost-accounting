import enum
import datetime

from sqlalchemy import Column, Integer, Enum, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class StatusDB(str, enum.Enum):
    AWAITING = "awaiting"
    ACCEPTED = "accepted"
    DENIED = "denied"
    OVERDUE = "OVERDUE"


class StatusUser(str, enum.Enum):
    ACCEPTED = "accepted"
    DENIED = "denied"


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, Enum(StatusDB), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    time = Column(DateTime, default=datetime.datetime.utcnow)

    group = relationship("Group", back_populates="invitations")
    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship("User", foreign_keys=[recipient_id])
