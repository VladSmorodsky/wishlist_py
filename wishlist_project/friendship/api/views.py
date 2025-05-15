from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from friendship.api.serializers import FriendRequestSerializer, FriendshipSerializer
from friendship.models import FriendRequest, FriendRequestStatus, Friendship


# Friend Request Views

class FriendRequestListCreateView(ListCreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(Q(from_user=user) | Q(to_user=user))

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)


class FriendRequestAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        friend_request = get_object_or_404(
            FriendRequest,
            pk=pk,
            to_user=request.user,
            status=FriendRequestStatus.PENDING
        )
        friend_request.accept()
        return Response({"status": "accepted"}, status=status.HTTP_200_OK)


class FriendRequestRejectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        friend_request = get_object_or_404(
            FriendRequest,
            pk=pk,
            to_user=request.user,
            status=FriendRequestStatus.PENDING
        )
        friend_request.reject()
        return Response({"status": "rejected"}, status=status.HTTP_200_OK)


# Friendship Views

class FriendshipMixinApiView(ListAPIView, DestroyAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(Q(friendships__friend=user) | Q(friends__user=user)).distinct()


class FriendshipListView(FriendshipMixinApiView):
    pass


class FriendshipDestroyView(FriendshipMixinApiView):
    lookup_url_kwarg = 'pk'

    def perform_destroy(self, instance):
        deleted_friend = instance.friend
        instance.delete()
        Friendship.objects.filter(user=deleted_friend, friend=self.request.user).delete()
