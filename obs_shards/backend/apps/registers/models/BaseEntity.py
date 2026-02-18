"""
    `backend/apps/registers/models/BaseEntity.py`
    
    Abstract base model for the `obs-shards/registers` application
    Virtually all other register classes are derived from this class.
    
    @author:    nícolas-rosenthal
    @version:   1.0
    @date:      2026-02-17
"""
import uuid
from django.db import models


class BaseEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schema_version = models.CharField(max_length=10, default="v2")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=100)

    class Meta:
        abstract = True
