from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    items = relationship("Item", back_populates="user")
    categories = relationship("Category", back_populates="user")
    user_groups = relationship("UserGroup", back_populates="user")
