from tkinter.font import names

from django.urls.conf import path

from wishlist_app.api.views import MyWishListApiView, CreateWishApiView, AllFriendsWishesListApiView, FriendWishesListApiView

urlpatterns = [
    path('wishes/me/', MyWishListApiView.as_view(), name='my-wishes'),
    path('wishes/friends/', AllFriendsWishesListApiView.as_view(), name='all-friends-wishes'),
    path('wishes/friends/<int:friend_id>', FriendWishesListApiView.as_view(), name='friend-wishes'),
    path('wishes/', CreateWishApiView.as_view(), name='create-wish'),
]