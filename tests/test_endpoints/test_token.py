from tests.conftest import client


def test_token_user(session):
    response = client.post(
        "/users/", json={"email": "test1@gmail.com", "password": "testA89"}
    )
    assert response.status_code == 200
    response = client.post(
        "/token/",
        data={
            "username": "test1@gmail.com",
            "password": "testA89",
        },
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    data_token = response.json()
    assert "access_token" in data_token
    assert "token_type" in data_token
