"""
    `shards/config/__init__.py`
"""
#   Registering Celery in Django
from .celery import app as celery_app
__all__ = ('celery_app', )