from tests.conftest import client


def test_read_stats(session):
    response = client.post(
        "/users/", json={"email": "test1@gmail.com", "password": "testA89"}
    )

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
    category_id_one = data_category["id"]

    response = client.post(
        "/users/create-item/",
        json={
            "description": "1984 Orwell",
            "price": 250,
            "time": "2023-01-10T09:58:37.234",
            "category_id": category_id_one,
        },
        headers={"Authorization": "Bearer " + token},
    )

    response = client.get(
        "/users/statistics/",
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 200
    data_statistics = response.json()
    assert data_statistics == {
        "email": "test1@gmail.com",
        "costs": 250.0,
        "number_purchases": 1,
        "details": {
            "Books": 250.0,
        },
        "number_purchases_category": {
            "Books": 1,
        }
    }

    response = client.post(
        "/users/category/",
        json={"title": "Gym"},
        headers={"Authorization": "Bearer " + token},
    )
    data_category = response.json()
    category_id_two = data_category["id"]

    response = client.post(
        "/users/create-item/",
        json={
            "description": "Abonement",
            "price": 200,
            "time": "2023-01-10T11:58:37.234",
            "category_id": category_id_two,
        },
        headers={"Authorization": "Bearer " + token},
    )

    response = client.get(
        "/users/statistics/",
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 200
    data_statistics = response.json()
    assert data_statistics == {
        "email": "test1@gmail.com",
        "costs": 450.0,
        "number_purchases": 2,
        "details": {
            "Books": 250.0,
            "Gym": 200.0,
        },
        "number_purchases_category": {
            "Books": 1,
            "Gym": 1,
        }
    }


def test_read_stats_for_month(session):
    response = client.post(
        "/users/", json={"email": "test1@gmail.com", "password": "testA89"}
    )

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
    category_id_one = data_category["id"]

    response = client.post(
        "/users/create-item/",
        json={
            "description": "1984 Orwell",
            "price": 250,
            "time": "2023-01-10T09:58:37.234",
            "category_id": category_id_one,
        },
        headers={"Authorization": "Bearer " + token},
    )

    response = client.post(
        "/users/category/",
        json={"title": "Gym"},
        headers={"Authorization": "Bearer " + token},
    )
    data_category = response.json()
    category_id_two = data_category["id"]

    response = client.post(
        "/users/create-item/",
        json={
            "description": "Abonement",
            "price": 200,
            "time": "2023-02-10T11:58:37.234",
            "category_id": category_id_two,
        },
        headers={"Authorization": "Bearer " + token},
    )

    response = client.get(
        "/users/statistics/2023-01",
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 200
    data_statistics = response.json()
    assert data_statistics == {
        "email": "test1@gmail.com",
        "costs": 250.0,
        "number_purchases": 1,
        "details": {
            "Books": 250.0,
            "Gym": 0,
        },
        "number_purchases_category": {
            "Books": 1,
            "Gym": 0,
        }
    }

    response = client.get(
        "/users/statistics/2023-02",
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 200
    data_statistics = response.json()
    assert data_statistics == {
        "email": "test1@gmail.com",
        "costs": 200.0,
        "number_purchases": 1,
        "details": {
            "Books": 0,
            "Gym": 200.0,
        },
        "number_purchases_category": {
            "Books": 0,
            "Gym": 1,
        }
    }

    response = client.get(
        "/users/statistics/02-2023",
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 422

    response = client.get(
        "/users/statistics/2023-03",
        headers={"Authorization": "Bearer " + token},
    )
    assert response.status_code == 200
    data_statistics = response.json()
    assert data_statistics == {
        "email": "test1@gmail.com",
        "costs": 0,
        "number_purchases": 0,
        "details": {
            "Books": 0,
            "Gym": 0,
        },
        "number_purchases_category": {
            "Books": 0,
            "Gym": 0
        }
    }