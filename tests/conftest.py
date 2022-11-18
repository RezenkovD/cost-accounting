import pytest
from fastapi.testclient import TestClient

from main import app
from db.database import get_db
from db.database import Base
from db.test_database import engine, override_get_db


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
