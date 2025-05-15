from django.urls.conf import path

from friendship.api.views import FriendRequestListCreateView, FriendRequestAcceptView, FriendRequestRejectView, \
    FriendshipListView

urlpatterns = [
    path('requests/', FriendRequestListCreateView.as_view(), name='friend-request-list'),
    path('requests/<int:pk>/accept/', FriendRequestAcceptView.as_view(), name='friend-request-accept'),
    path('requests/<int:pk>/reject/', FriendRequestRejectView.as_view(), name='friend-request-reject'),

    path('friends/', FriendshipListView.as_view(), name='friend-list'),
]
