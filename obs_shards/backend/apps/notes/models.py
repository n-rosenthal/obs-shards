"""
    `backend/apps/notes/models.py`
    
    Models for the `obs-shards/notes` application.
"""
#   unique identifier for notes
import uuid

#   Django base model
from django.db import models


class Note(models.Model):
    """
        `Note` model
        
        Representation of a `.md` note file.
    """
    class NoteType(models.TextChoices):
        """
            `NoteType` enumerated type
            
            Possible values for the `doctype` field in a `Note`
        """
        STUDY   = "study", "Study"
        JOURNAL = "journal", "Journal"
        PROJECT = "project", "Project"
        TASK    = "task", "Task"
        TEMP    = "temp", "Temp"
        OTHER   = "other", "Other"

    #   unique identifier
    id = models.UUIDField(
        #   notes are uniquely identified by their UUID
        primary_key=True,
        default=uuid.uuid4,

        #   after creation, the UUID can't be changed
        editable=False
    )

    #   title and content
    title = models.CharField(max_length=255)
    content = models.TextField()

    #   YAML frontmatter
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Frontmatter-like arbitrary metadata"
    )
    
    #   note type
    doctype = models.CharField(
        max_length=20,
        choices=NoteType.choices,
        
        #   by default, group Notes using the `TEMP` doctype
        default=NoteType.TEMP
    )

    #   date for the note, if important
    date = models.DateField(
        null=True,
        blank=True,
        help_text="Semantic date (mainly for journal entries)"
    )
    
    #   time interval for the note, if important
    interval = models.JSONField(
        null=True,
        blank=True,
        help_text="Semantic time interval (mainly for journal entries)"
    )



    #   timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
            `Meta` class
            
            Defines ordering for default queryset and indexes for faster queries
        """
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["doctype"]),
            models.Index(fields=["date"]),
        ]

    def __str__(self):
        """
        Return a human-readable string representation of the Note

        :return: A string of the form "[{id}] {title} ({type})"
        :rtype: str
        """
        return f"[{id}] {self.title} ({self.type})"

