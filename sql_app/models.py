import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    goods = relationship("Goods", back_populates="user")


class Goods(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String, index=True)
    price = Column(DECIMAL, index=True)
    time = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="goods")
