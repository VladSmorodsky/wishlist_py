from django.conf import settings
from rest_framework import serializers

from friendship.models import FriendRequest, Friendship


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the FriendRequest model
    """
    from_user = serializers.ReadOnlyField(source="from_user.username")
    to_user = serializers.SlugRelatedField(
        slug_field='username', queryset=settings.AUTH_USER_MODEL.objects.all()
    )

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']

class FriendshipSerializer(serializers.ModelSerializer):
    friend = serializers.ReadOnlyField(source="friend.username")
    class Meta:
        model = Friendship
        fields = ['friend', 'created_at']
