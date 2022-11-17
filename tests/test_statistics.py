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


def test_get_stats(test_db):
    from tests.test_items import test_create_item_for_user
    test_create_item_for_user(test_db)

    response = client.get(f"/users/1/statistics")
    assert response.status_code == 200
    statistics = response.json()
    assert statistics == {
        "email": "test@gmail.com",
        "costs": 1455,
        "number_purchases": 3,
        "details": {
            "Accessories": 1299.0,
            "Food": 156.0,
        },
        "number_purchases_category": {
            "Accessories": 1,
            "Food": 2,
        },
    }

    response = client.get(f"/users/2/statistics")
    assert response.status_code == 200
    statistics = response.json()
    assert statistics == {
        "email": "test2@gmail.com",
        "costs": 0,
        "number_purchases": 0,
        "details": {},
        "number_purchases_category": {},
    }


def test_get_stats_month(test_db):
    from tests.test_items import test_create_item_for_user
    test_create_item_for_user(test_db)

    response = client.get(f"/users/1/statistics/2022-11")
    assert response.status_code == 200
    statistics = response.json()
    assert statistics == {
        "email": "test@gmail.com",
        "costs": 1355,
        "number_purchases": 2,
        "details": {
            "Accessories": 1299.0,
            "Food": 56.0,
        },
        "number_purchases_category": {
            "Accessories": 1,
            "Food": 1,
        },
    }

    response = client.get(f"/users/2/statistics/2022-11")
    assert response.status_code == 200
    statistics = response.json()
    assert statistics == {
        "email": "test2@gmail.com",
        "costs": 0,
        "number_purchases": 0,
        "details": {},
        "number_purchases_category": {},
    }

    response = client.get(f"/users/1/statistics/11-2021")
    assert response.status_code == 422

    response = client.get(f"/users/1/statistics/DROP DATABASE")
    assert response.status_code == 422

    response = client.get(f"/users/1/statistics/2021-10")
    assert response.status_code == 200
    statistics = response.json()
    assert statistics == {
        "email": "test@gmail.com",
        "costs": 0,
        "number_purchases": 0,
        "details": {
            "Accessories": 0,
            "Food": 0,
        },
        "number_purchases_category": {
            "Accessories": 0,
            "Food": 0,
        },
    }

    response = client.get(f"/users/1/statistics/2022-12")
    assert response.status_code == 200
    statistics = response.json()
    assert statistics == {
        "email": "test@gmail.com",
        "costs": 100,
        "number_purchases": 1,
        "details": {
            "Accessories": 0,
            "Food": 100.0,
        },
        "number_purchases_category": {
            "Accessories": 0,
            "Food": 1,
        },
    }