from tests.conftest import client
from tests.factories import CategoryFactory, ItemFactory, UserFactory


def test_read_users(session):
    user_one = UserFactory.create()
    user_two = UserFactory.create()
    category_one = CategoryFactory.create(user_id=user_one.id, title="category_one")
    category_two = CategoryFactory.create(user_id=user_one.id, title="category_two")
    item_one = ItemFactory.create(
        user_id=user_one.id,
        description="item_one",
        price=100,
        time="2022-12-01T08:52:53.301000",
        category_id=category_one.id,
    )
    response = client.get(f"/users/")
    assert response.status_code == 200
    users = response.json()
    assert users == [
        {
            "email": user_one.email,
            "id": user_one.id,
            "items": [
                {
                    "description": item_one.description,
                    "price": float(item_one.price),
                    "time": item_one.time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                    "id": item_one.id,
                    "user_id": item_one.user_id,
                    "category": {
                        "title": category_one.title,
                        "id": category_one.id,
                        "user_id": category_one.user_id,
                    },
                },
            ],
            "categories": [
                {
                    "title": category_one.title,
                    "id": category_one.id,
                    "user_id": category_one.user_id,
                },
                {
                    "title": category_two.title,
                    "id": category_two.id,
                    "user_id": category_two.user_id,
                },
            ],
        },
        {
            "email": user_two.email,
            "id": user_two.id,
            "items": [],
            "categories": [],
        },
    ]


def test_create_user(session):
    response = client.post(
        "/users/", json={"email": "test1@gmail.com", "password": "testA89"}
    )
    user = response.json()
    assert response.status_code == 200
    assert user["email"] == "test1@gmail.com"
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


def test_read_user(session):
    response = client.post(
        "/users/", json={"email": "test1@gmail.com", "password": "testA89"}
    )
    data = response.json()
    user_email = data["email"]
    user_id = data["id"]
    response = client.post(
        "/token/",
        data={
            "username": "test1@gmail.com",
            "password": "testA89",
        },
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    data_token = response.json()
    token = data_token["access_token"]

    response = client.get("/users/user/", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200
    user = response.json()
    assert user == {"email": user_email, "id": user_id, "items": [], "categories": []}
