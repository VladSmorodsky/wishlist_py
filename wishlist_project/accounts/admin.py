from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {
            'fields': ('telegram_id', 'image'),
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            'fields': ('telegram_id', 'image'),
        }),
    )
