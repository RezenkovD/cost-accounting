from tests.conftest import client


def test_create_category_for_user(session):
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
        json={"title": "Gym"},
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 200
    data_category = response.json()
    category_id = data_category["id"]
    assert data_category == {"title": "Gym", "id": category_id, "user_id": user_id}
