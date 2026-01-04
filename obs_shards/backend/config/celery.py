"""
    `shards/config/celery.py`, Configuration for Celery
    
    Defines settings for Celery and sets up automatic task discovery
"""

import os
from celery import Celery

#   Take Django settings from environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

#   Celery instance
app = Celery("obsidian_shards")

#   Config itself from every setting in the (celery namespace of) Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

#   Autodiscover tasks
app.autodiscover_tasks()
