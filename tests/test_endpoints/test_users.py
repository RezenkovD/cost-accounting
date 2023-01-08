from tests.conftest import client
from tests.factories import CategoryFactory, ItemFactory, UserFactory


def test_read_users(session):
    user_one = UserFactory.create()
    user_two = UserFactory.create()
    user_one_email = user_one.email
    user_two_email = user_two.email

    response = client.get(f"/users/")
    assert response.status_code == 200
    users = response.json()
    breakpoint()
    assert users == [
        {
            "email": user_one_email,
            "id": 1,
            "items": [],
            "categories": [],
        },
        {
            "email": user_two_email,
            "id": 2,
            "items": [],
            "categories": [],
        },
    ]
