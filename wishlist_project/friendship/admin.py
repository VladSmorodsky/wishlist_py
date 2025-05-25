from django.contrib import admin

from friendship.models import Friendship, FriendRequest


# Register your models here.

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ("user", "friend")
    list_filter = ("friend",)

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    pass