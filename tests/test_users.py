from tests.conftest import client, db


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
    from tests.test_items import test_create_item_for_user

    test_create_item_for_user(db)

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


def test_read_users(db):
    from tests.test_items import test_create_item_for_user

    test_create_item_for_user(db)

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
