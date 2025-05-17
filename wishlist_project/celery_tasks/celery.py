import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wishlist_project.settings')

app = Celery('wishlist_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(['celery_tasks.tasks'])

app.conf.beat_schedule = {
    'send_wish_notification': {
        'task': 'celery_tasks.tasks.send_wish_notification',
        'schedule': crontab(hour=9, minute=0),
    }
}