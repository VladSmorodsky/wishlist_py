from rest_framework import serializers

from friendship.models import FriendRequest, Friendship
from accounts.models import User


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the FriendRequest model
    """
    from_user = serializers.ReadOnlyField(source="from_user.username")
    to_user = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
