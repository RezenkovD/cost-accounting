from tests.conftest import client, db


def test_create_category_for_user(db):
    from tests.test_users import test_create_user

    test_create_user(db)

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
