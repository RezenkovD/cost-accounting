from tests.conftest import client

from tests.factories.users import UserFactory


def test_create_category_for_user(db):
    user = UserFactory.create(email="test@gmail.com")

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
