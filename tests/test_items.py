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


def test_create_item_for_user(test_db):
    from tests.test_categories import test_create_category_for_user

    test_create_category_for_user(test_db)

    response = client.post(
        f"/users/1/item/",
        json={
            "description": "Redmi Buds 3",
            "price": 1299,
            "time": "2022-11-01T08:52:53.301000",
            "category_id": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Redmi Buds 3"
    assert data["price"] == 1299
    assert data["user_id"] == 1

    response = client.post(
        f"/users/1/item/",
        json={
            "description": "Pasta",
            "price": 56,
            "time": "2022-11-17T08:52:53.301000",
            "category_id": 2,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Pasta"
    assert data["price"] == 56
    assert data["user_id"] == 1

    response = client.post(
        f"/users/1/item/",
        json={
            "description": "Potato",
            "price": 100,
            "time": "2022-12-01T08:52:53.301000",
            "category_id": 2,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Potato"
    assert data["price"] == 100
    assert data["user_id"] == 1
