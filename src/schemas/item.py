from pydantic import BaseModel
from pydantic.schema import datetime
from src.schemas.category import Category


class ItemBase(BaseModel):
    description: str
    price: float
    time: datetime


class ItemCreate(ItemBase):
    category_id: int


class Item(ItemBase):
    id: int
    user_id: int
    category: Category

    class Config:
        orm_mode = True
