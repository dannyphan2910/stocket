from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "performance-snapshot-task": {
        "task": "tasks.performance_snapshot",
        "schedule": crontab(minute=31, hour='9,10,11,12,13,14,15', day_of_week='mon-fri')
    }
}

# celery -A backend.celery worker -l DEBUG -E
