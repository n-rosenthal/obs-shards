from django.db import models

from BaseEntity import BaseEntity
from Author import Author

class TextType(models.TextChoices):
    BOOK = "Book"
    ARTICLE = "Article"
    LETTER = "Letter"
    BLOGPOST = "BlogPost"
    SOCIAL_VIDEO = "SocialMediaVideo"
    JOURNAL = "JournalEntry"


class TextReference(BaseEntity):
    type = models.CharField(max_length=50, choices=TextType.choices)
    title = models.CharField(max_length=500)
    year = models.IntegerField(null=True, blank=True)

    authors = models.ManyToManyField(Author, related_name="texts")

    publisher = models.CharField(max_length=255, null=True, blank=True)
    publisher_location = models.CharField(max_length=255, null=True, blank=True)
    isbn = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.type = "reference/text-reference"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
