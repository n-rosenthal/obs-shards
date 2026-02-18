from django.db import models

from BaseEntity import BaseEntity

class Author(BaseEntity):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    birthyear = models.CharField(max_length=10, null=True, blank=True)
    nationality = models.CharField(max_length=120, null=True, blank=True)
    genres = models.JSONField(default=list, blank=True)

    def save(self, *args, **kwargs):
        self.type = "reference/text-reference/author"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"