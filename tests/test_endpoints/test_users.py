from tests.conftest import client
from tests.factories import CategoryFactory, ItemFactory, UserFactory


def test_create_user(db):
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


def test_read_user(db):
    user_one = UserFactory.create()
    user_one_email = user_one.email
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

    response = client.get(f"/users/1")
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == user_one_email
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
        "email": user_one_email,
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


def test_read_users(db):
    user_one = UserFactory.create(email="test@gmail.com")
    user_two = UserFactory.create(email="test2@gmail.com")
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

    response = client.get(f"/users/")
    assert response.status_code == 200
    users = response.json()
    assert users == [
        {
            "email": user_one_email,
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
            "email": user_two_email,
            "id": 2,
            "items": [],
            "categories": [],
        },
    ]
