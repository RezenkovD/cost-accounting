from tests.conftest import client
from tests.factories.users import UserFactory
from tests.factories.categories import CategoryFactory
from tests.factories.items import ItemFactory


def test_get_stats(db):
    user_one = UserFactory.create()
    user_two = UserFactory.create()
    user_one_email = user_one.email
    user_two_email = user_two.email
    category_one = CategoryFactory.create(user_id=user_one.id, title="Accessories")
    category_two = CategoryFactory.create(user_id=user_one.id, title="Food")

    item_one = ItemFactory.create(
        user_id=user_one.id,
        description="Redmi Buds 3",
        price=1299,
        time="2022-11-01T08:52:53.301000",
        category_id=category_one.id,
    )
    item_two = ItemFactory.create(
        user_id=user_one.id,
        description="Pasta",
        price=56,
        time="2022-11-17T08:52:53.301000",
        category_id=category_two.id,
    )
    item_three = ItemFactory.create(
        user_id=1,
        description="Potato",
        price=100,
        time="2022-12-01T08:52:53.301000",
        category_id=category_two.id,
    )

    response = client.get(f"/users/1/statistics")
    assert response.status_code == 200
    statistics = response.json()
    assert statistics == {
        "email": user_one_email,
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
        "email": user_two_email,
        "costs": 0,
        "number_purchases": 0,
        "details": {},
        "number_purchases_category": {},
    }


def test_get_stats_month(db):
    user_one = UserFactory.create()
    user_two = UserFactory.create()
    user_one_email = user_one.email
    user_two_email = user_two.email
    category_one = CategoryFactory.create(user_id=user_one.id, title="Accessories")
    category_two = CategoryFactory.create(user_id=user_one.id, title="Food")

    item_one = ItemFactory.create(
        user_id=user_one.id,
        description="Redmi Buds 3",
        price=1299,
        time="2022-11-01T08:52:53.301000",
        category_id=category_one.id,
    )
    item_two = ItemFactory.create(
        user_id=user_one.id,
        description="Pasta",
        price=56,
        time="2022-11-17T08:52:53.301000",
        category_id=category_two.id,
    )
    item_three = ItemFactory.create(
        user_id=1,
        description="Potato",
        price=100,
        time="2022-12-01T08:52:53.301000",
        category_id=category_two.id,
    )

    response = client.get(f"/users/1/statistics/2022-11")
    assert response.status_code == 200
    statistics = response.json()
    assert statistics == {
        "email": user_one_email,
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
        "email": user_two_email,
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
        "email": user_one_email,
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
        "email": user_one_email,
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
