from django.contrib import admin

from wishlist_app.models import Wish


# Register your models here.

@admin.register(Wish)
class WishlistAdmin(admin.ModelAdmin):
    list_filter = ['user', 'name', 'url']
    search_fields = ['name']
