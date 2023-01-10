from tests.conftest import client


def test_create_item_for_user(session):
    response = client.post(
        "/users/", json={"email": "test1@gmail.com", "password": "testA89"}
    )
    data = response.json()
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

    response = client.post(
        "/users/category/",
        json={"title": "Books"},
        headers={"Authorization": "Bearer " + token},
    )
    data_category = response.json()
    category_id = data_category["id"]

    response = client.post(
        "users/create-item/",
        json={
            "description": "1984 Orwell",
            "price": 250,
            "time": "2023-01-10T09:58:37.234",
            "category_id": category_id,
        },
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 200
    data_item = response.json()
    item_id = data_item["id"]
    assert data_item == {
        "description": "1984 Orwell",
        "price": 250.0,
        "time": "2023-01-10T09:58:37.234000",
        "id": item_id,
        "user_id": user_id,
        "category": {"title": "Books", "id": category_id, "user_id": user_id},
    }
