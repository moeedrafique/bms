# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_management_system.settings')

# Create a Celery instance and configure it using the settings from Django.
app = Celery('bakery_management_system')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps by looking for a 'tasks.py' file.
app.autodiscover_tasks()
