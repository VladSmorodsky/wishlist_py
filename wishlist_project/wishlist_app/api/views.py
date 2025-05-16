from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED

from accounts.models import User
from wishlist_app.api.serializers import WishlistSerializer
from wishlist_app.models import Wish


class MyWishListApiView(ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wish.objects.filter(user=self.request.user)


class CreateWishApiView(CreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    status_code = HTTP_201_CREATED

    def get_queryset(self):
        return Wish.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=HTTP_201_CREATED)


class AllFriendsWishesListApiView(ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = User.objects.filter(Q(friendships__friend=user) | Q(friends__user=user)).distinct()
        return Wish.active.filter(user__in=friends)


class FriendWishesListApiView(ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    pk_url_kwarg = 'friend_id'

    def get_queryset(self):
        user = self.request.user
        friend_pk = self.kwargs['friend_id']
        friend = get_object_or_404(User, Q(friendships__friend=user) | Q(friends__user=user), pk=friend_pk)
        return Wish.active.filter(user=friend)
