from enum import Enum

from pydantic import BaseModel
from pydantic.schema import datetime


class CategoryEnum(str, Enum):
    books = "Books"
    cafes_and_restaurants = "Cafes and restaurants"
    travels = "Travels"
    products_and_supermarkets = "Products and supermarkets"
    household_appliances = "Household appliances"
    transfer_to_the_card = "Transfer to the card"
    others = "Others"


class ItemBase(BaseModel):
    description: str
    price: float
    time: datetime
    category: CategoryEnum


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
