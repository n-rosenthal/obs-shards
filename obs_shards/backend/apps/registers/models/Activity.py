from django.db import models
from pgvector.django import VectorField


from BaseEntity import BaseEntity
from TextReference import TextReference


class Activity(BaseEntity):
    category = models.CharField(max_length=120)
    title = models.CharField(max_length=500)
    body = models.TextField()
    
    #   semantic search over activities
    embedding = VectorField(dimensions=1536, null=True, blank=True)

    activity_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    duration = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    mood = models.CharField(max_length=120, null=True, blank=True)

    people = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    def generate_embedding(text: str) -> list[float]:
        """
        Generate an embedding for the given text.

        This method should be overridden in subclasses to provide a meaningful
        way of generating an embedding for the given text.

        :param text: str, the text to generate an embedding for
        :return: list[float], the generated embedding
        """
        pass

    def save(self, *args, **kwargs):
        self.type = "activity"
        
        if not self.embedding:
            self.embedding = self.generate_embedding(self.title + " " + self.body)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ReadingActivity(Activity):
    text = models.ForeignKey(
        TextReference,
        on_delete=models.CASCADE,
        related_name="reading_sessions"
    )

    pages_initial = models.IntegerField()
    pages_end = models.IntegerField()

    @property
    def pages_count(self):
        return self.pages_end - self.pages_initial

    def save(self, *args, **kwargs):
        self.type = "activity/reading"
        super().save(*args, **kwargs)
