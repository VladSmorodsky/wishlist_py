from django.db.models.query_utils import Q
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED

from accounts.models import User
from wishlist_app.api.serializers import WishlistSerializer, WishDetailSerializer
from wishlist_app.models import Wish

# Manage user's wishes

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
        data = request.data
        data['user'] = self.request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class RetrieveUpdateDestroyWishApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = WishDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'wish_id'

    def get_queryset(self):
        return Wish.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        print('[UPDATE]')
        serializer.save(user=self.request.user)

# Friends Wishes

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
        friend = User.objects.filter(Q(friendships__friend=user) | Q(friends__user=user), pk=friend_pk)[:1]
        return Wish.active.filter(user=friend)
