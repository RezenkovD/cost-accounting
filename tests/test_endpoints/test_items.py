from tests.conftest import client

from tests.factories.users import UserFactory
from tests.factories.categories import CategoryFactory


def test_create_item_for_user(db):
    user = UserFactory.create(email="test@gmail.com", hashed_password="test89A")

    category_one = CategoryFactory.create(user_id=user.id, title="Accessories")
    category_two = CategoryFactory.create(user_id=user.id, title="Food")

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
