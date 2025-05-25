from django.contrib.auth.models import User, AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    telegram_id = models.BigIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to="profile_pics/", null=True, blank=True)

    def __str__(self):
        return f"{self.username}"
