from rest_framework import serializers

from wishlist_app.models import Wish


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ['name', 'url', 'description', 'user']
        read_only_fields = ['user']


class WishDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = '__all__'
