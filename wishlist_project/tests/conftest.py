import pytest
from rest_framework.test import APIClient

from accounts.models import User
from friendship.models import Friendship
from wishlist_app.models import Wish


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def get_user(db):
    return User.objects.create_user(
        email="test@test.com",
        username="test",
        password="12345678"
    )

@pytest.fixture
def get_friends(db):
    user_object = User.objects.create_user(
        email="test_user@test.com",
        username="test_user",
        password="12345678"
    )
    friend = User.objects.create_user(
        email="friend@test.com",
        username="friend",
        password="012345678"
    )
    Friendship.objects.create(user=user_object, friend=friend)
    return [user_object, friend]

# @pytest.fixture
# def auth_client(api_client: APIClient, user):
#     api_client.force_authenticate(user=user)
#     return api_client
