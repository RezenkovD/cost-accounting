import factory

from app.models import Item
from tests.conftest import session


class ItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Item
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    user_id = factory.Faker("user_id")
    description = factory.Faker("title")
    price = factory.Faker("price")
    time = factory.Faker("time")
    category_id = factory.Faker("category_id")
