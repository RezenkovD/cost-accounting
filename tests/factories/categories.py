import factory

from app.models import Category
from tests.conftest import session


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    user_id = factory.Faker("user_id")
    title = factory.Faker("title")
