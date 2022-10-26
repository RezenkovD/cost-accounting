import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship

from db.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String, index=True)
    price = Column(DECIMAL, index=True)
    time = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="items")
