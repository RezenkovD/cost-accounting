import factory

from app.models import User
from .base_factory import BaseFactory


class UserFactory(BaseFactory):
    email = factory.Sequence(lambda n: f"b{n}@gmail.com")
    hashed_password = "hashed_password"

    class Meta:
        model = User
