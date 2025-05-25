import pytest
from django.urls.base import reverse

from wishlist_app.models import Wish


@pytest.mark.usefixtures("api_client", "get_user", "get_friends")
class TestWishAPI:
    my_wishes_endpoint = "/api/wishes/me"

    def test_get_endpoint(self, api_client, get_user):
        api_client.force_authenticate(user=get_user)
        response = api_client.get(self.my_wishes_endpoint)
        assert response.status_code == 200

    def test_get_endpoint_wish_unauthorized_user(self, api_client):
        response = api_client.get(self.my_wishes_endpoint)
        assert response.status_code == 401

    def test_create_wish_endpoint(self, api_client, get_user):
        url = reverse('create-wish')
        wish_data = {"name": "My Wish"}
        api_client.force_authenticate(user=get_user)
        response = api_client.post(url, data=wish_data, format="json")
        received_wish = response.json()
        assert response.status_code == 201
        assert received_wish["name"] == wish_data["name"]
        assert received_wish['user'] == get_user.id

    def test_get_friends_wishes_endpoint(self, api_client, get_friends):
        user, friend = get_friends
        wish = Wish.objects.create(user=friend, name="My Wish")
        api_client.force_authenticate(user=user)
        url = reverse('all-friends-wishes')
        response = api_client.get(url, format="json")
        received_wish = response.json()[0]
        assert response.status_code == 200
        assert received_wish['id'] == wish.id
        assert received_wish['name'] == wish.name
        assert received_wish['description'] == wish.description
        assert received_wish['user'] == wish.user.id
