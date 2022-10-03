from typing import List

from pydantic import BaseModel
from pydantic.schema import datetime


class GoodsBase(BaseModel):
    description: str
    price: float
    time: datetime


class GoodsCreate(GoodsBase):
    pass


class Goods(GoodsBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    goods: List[Goods] = []

    class Config:
        orm_mode = True
