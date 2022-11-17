import pytest
from fastapi.testclient import TestClient

from main import app
from db.database import get_db
from db.database import Base
from db.test_database import engine, override_get_db


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_category_for_user(test_db):
    from tests.test_users import test_create_user

    test_create_user(test_db)

    response = client.post(
        f"/users/category/",
        json={"title": "Accessories", "user_id": 1},
    )
    assert response.status_code == 200
    category = response.json()
    assert category["title"] == "Accessories"
    assert category["user_id"] == 1

    response = client.post(
        f"/users/category/",
        json={"title": "Food", "user_id": 1},
    )
    assert response.status_code == 200
    category = response.json()
    assert category["title"] == "Food"
    assert category["user_id"] == 1
