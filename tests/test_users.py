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


def test_create_user(test_db):
    response = client.post(
        "/users/", json={"email": "test@gmail.com", "password": "testA89"}
    )
    user = response.json()
    assert response.status_code == 200
    assert user["email"] == "test@gmail.com"
    assert "id" in user
    user_id_1 = user["id"]

    response = client.post(
        "/users/", json={"email": "test2@gmail.com", "password": "testB89"}
    )
    user = response.json()
    assert response.status_code == 200
    assert user["email"] == "test2@gmail.com"
    assert "id" in user
    user_id_2 = user["id"]

    assert user_id_1 != user_id_2


def test_read_user(test_db):
    from tests.test_items import test_create_item_for_user
    test_create_item_for_user(test_db)

    response = client.get(f"/users/1")
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
        },
        {
            "description": "Pasta",
            "price": 56,
            "time": "2022-11-17T08:52:53.301000",
            "id": 2,
            "user_id": 1,
            "category": {"title": "Food", "id": 2, "user_id": 1},
        },
        {
            "description": "Potato",
            "price": 100,
            "time": "2022-12-01T08:52:53.301000",
            "id": 3,
            "user_id": 1,
            "category": {"title": "Food", "id": 2, "user_id": 1},
        },
    ]
    assert user["categories"] == [
        {"title": "Accessories", "id": 1, "user_id": 1},
        {"title": "Food", "id": 2, "user_id": 1},
    ]
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
            },
            {
                "description": "Pasta",
                "price": 56,
                "time": "2022-11-17T08:52:53.301000",
                "id": 2,
                "user_id": 1,
                "category": {"title": "Food", "id": 2, "user_id": 1},
            },
            {
                "description": "Potato",
                "price": 100,
                "time": "2022-12-01T08:52:53.301000",
                "id": 3,
                "user_id": 1,
                "category": {"title": "Food", "id": 2, "user_id": 1},
            },
        ],
        "categories": [
            {"title": "Accessories", "id": 1, "user_id": 1},
            {"title": "Food", "id": 2, "user_id": 1},
        ],
    }


def test_read_users(test_db):
    from tests.test_items import test_create_item_for_user
    test_create_item_for_user(test_db)

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
                },
                {
                    "description": "Pasta",
                    "price": 56,
                    "time": "2022-11-17T08:52:53.301000",
                    "id": 2,
                    "user_id": 1,
                    "category": {"title": "Food", "id": 2, "user_id": 1},
                },
                {
                    "description": "Potato",
                    "price": 100,
                    "time": "2022-12-01T08:52:53.301000",
                    "id": 3,
                    "user_id": 1,
                    "category": {"title": "Food", "id": 2, "user_id": 1},
                },
            ],
            "categories": [
                {"title": "Accessories", "id": 1, "user_id": 1},
                {"title": "Food", "id": 2, "user_id": 1},
            ],
        },
        {
            "email": "test2@gmail.com",
            "id": 2,
            "items": [],
            "categories": [],
        },
    ]