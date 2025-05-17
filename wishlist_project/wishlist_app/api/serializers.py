from rest_framework import serializers

from wishlist_app.models import Wish


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ['id', 'name', 'url', 'description', 'user', 'is_active']


class WishDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = '__all__'
        read_only_fields = ('user',)
