import factory

from app.models import Category
from .base_factory import BaseFactory


class CategoryFactory(BaseFactory):
    user_id = factory.Faker("user_id")
    title = factory.Faker("title")

    class Meta:
        model = Category
