from django.conf import settings
from django.db import models

from accounts.models import User


class ActiveWishlistManager(models.Manager):
    """
    Get active wishes
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


# Create your models here.
class Wish(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveWishlistManager()

    class Meta:
        ordering = ['-created_at']
        db_table = 'Wish'

    def __str__(self):
        return self.name
