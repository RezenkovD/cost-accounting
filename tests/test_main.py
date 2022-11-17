import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from db.get_database import get_db
from db.database import Base
from config import settings

TEST_SQLALCHEMY_DATABASE_URI = settings.TEST_SQLALCHEMY_DATABASE_URI

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URI)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_and_get_user_and_item(test_db):
    response = client.post(
        "/users/", json={"email": "test@gmail.com", "password": "testA89"}
    )
    user = response.json()
    assert response.status_code == 200
    assert user["email"] == "test@gmail.com"
    assert "id" in user
    user_id = user["id"]

    response = client.post(
        f"/users/category/",
        json={"title": "Accessories", "user_id": 1},
    )
    assert response.status_code == 200
    category = response.json()
    assert category["title"] == "Accessories"
    assert category["user_id"] == user_id
    category_id = category["id"]

    response = client.post(
        f"/users/{user_id}/item/",
        json={
            "description": "Redmi Buds 3",
            "price": 1299,
            "time": "2022-11-01T08:52:53.301000",
            "category_id": f"{category_id}",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Redmi Buds 3"
    assert data["price"] == 1299
    assert data["user_id"] == user_id

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "test@gmail.com"
    assert user["items"] == [
        {
            "description": "Redmi Buds 3",
            "price": 1299,
            "time": "2022-11-01T08:52:53.301000",
            "id": 1,
            "user_id": 1,
            "category": {"title": "Accessories", "id": 1, "user_id": 1},
        }
    ]
    assert user["categories"] == [{"title": "Accessories", "id": 1, "user_id": 1}]
    assert user == {
        "email": "test@gmail.com",
        "id": 1,
        "items": [
            {
                "description": "Redmi Buds 3",
                "price": 1299,
                "time": "2022-11-01T08:52:53.301000",
                "id": 1,
                "user_id": 1,
                "category": {"title": "Accessories", "id": 1, "user_id": 1},
            }
        ],
        "categories": [{"title": "Accessories", "id": 1, "user_id": 1}],
    }

    response = client.get(f"/users/")
    assert response.status_code == 200
    users = response.json()
    assert users == [
        {
            "email": "test@gmail.com",
            "id": 1,
            "items": [
                {
                    "description": "Redmi Buds 3",
                    "price": 1299,
                    "time": "2022-11-01T08:52:53.301000",
                    "id": 1,
                    "user_id": 1,
                    "category": {"title": "Accessories", "id": 1, "user_id": 1},
                }
            ],
            "categories": [{"title": "Accessories", "id": 1, "user_id": 1}],
        }
    ]

    response = client.get(f"/users/{user_id}/statistics")
    assert response.status_code == 200
    statistics = response.json()
    assert statistics == {
        "email": "test@gmail.com",
        "costs": 1299,
        "number_purchases": 1,
        "details": {
            "Accessories": 1299.0,
        },
        "number_purchases_category": {
            "Accessories": 1,
        },
    }

    response = client.get(f"/users/{user_id}/statistics/2022-11")
    assert response.status_code == 200
    statistics = response.json()
    assert statistics == {
        "email": "test@gmail.com",
        "costs": 1299,
        "number_purchases": 1,
        "details": {
            "Accessories": 1299.0,
        },
        "number_purchases_category": {
            "Accessories": 1,
        },
    }

    response = client.get(f"/users/{user_id}/statistics/11-2021")
    assert response.status_code == 422

    response = client.get(f"/users/{user_id}/statistics/DROP DATABASE")
    assert response.status_code == 422

    response = client.get(f"/users/{user_id}/statistics/2021-10")
    assert response.status_code == 200
    statistics = response.json()
    assert statistics == {
        "email": "test@gmail.com",
        "costs": 0,
        "number_purchases": 0,
        "details": {
            "Accessories": 0,
        },
        "number_purchases_category": {
            "Accessories": 0,
        },
    }
