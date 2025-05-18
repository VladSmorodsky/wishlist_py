import pytest
from django.core.exceptions import ValidationError

from wishlist_app.models import Wish


@pytest.mark.usefixtures('get_user')
class TestWishModel:
    def test_create_wish_without_name(self, get_user):
        wish = Wish.objects.create(user=get_user, name='')
        with pytest.raises(ValidationError) as error:
            wish.full_clean()

    def test_create_wish_without_user(self, get_user):
        wish = Wish.objects.create(user=get_user, name='')
        with pytest.raises(ValidationError):
            wish.full_clean()
