import factory

from app.models import Item
from .base_factory import BaseFactory


class ItemFactory(BaseFactory):
    user_id = factory.Faker("user_id")
    description = factory.Faker("title")
    price = factory.Faker("price")
    time = factory.Faker("time")
    category_id = factory.Faker("category_id")

    class Meta:
        model = Item
