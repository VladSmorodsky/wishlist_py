from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from accounts.models import User


@shared_task
def send_email(email: str, subject: str, body: str):
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email])


@shared_task
def send_wish_notification():
    users = User.objects.filter(is_superuser=False, is_staff=False)
    for user in users:
        send_mail(f"Check your friends wishes!", f"Don't forget to make your friends happy!",
                  settings.DEFAULT_FROM_EMAIL,
                  [user.email])
