from pydantic import BaseModel
from pydantic.schema import datetime


class ItemBase(BaseModel):
    description: str
    price: float
    time: datetime


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
