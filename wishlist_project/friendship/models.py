from enum import Enum

from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class FriendRequestStatus(models.IntegerChoices):
    PENDING = 0, 'Pending'
    ACCEPTED = 1, 'Accepted'
    REJECTED = 2, 'Rejected'


# Create your models here.

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_request', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_request', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(
        choices=FriendRequestStatus,
        default=FriendRequestStatus.PENDING,
    )

    class Meta:
        unique_together = ('from_user', 'to_user')

    def accept(self):
        Friendship.objects.bulk_create([
            Friendship(from_user=self.from_user, to_user=self.to_user),
            Friendship(from_user=self.to_user, to_user=self.from_user),
        ])
        self.status = FriendRequestStatus.ACCEPTED
        self.save()

    def reject(self):
        self.status = FriendRequestStatus.REJECTED
        self.save()
