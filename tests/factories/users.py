import factory

from app.models import User
from tests.conftest import session


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    email = factory.Sequence(lambda n: f"test{n}@gmail.com")
    hashed_password = "hashed_password"
