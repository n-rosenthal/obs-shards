"""
    Models for the `obs-shards/notes` application.
"""

import uuid
from django.db import models
from django.utils import timezone


class Note(models.Model):
    """
    Representation of a `.md` note file synchronized with a vault.
    """

    # ───────────────────────────────
    # Enums
    # ───────────────────────────────

    class NoteType(models.TextChoices):
        STUDY   = "study", "Study"
        JOURNAL = "journal", "Journal"
        PROJECT = "project", "Project"
        TASK    = "task", "Task"
        TEMP    = "temp", "Temp"
        OTHER   = "other", "Other"

    class SyncStatus(models.TextChoices):
        CLEAN     = "clean", "Clean"
        MODIFIED  = "modified", "Modified"
        CONFLICT  = "conflict", "Conflict"

    class ModifiedFrom(models.TextChoices):
        DB     = "db", "Database"
        VAULT  = "vault", "Vault"
        BOTH   = "both", "Both / Unknown"

    # ───────────────────────────────
    # Identity (semantic)
    # ───────────────────────────────

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    schema_version = models.PositiveSmallIntegerField(
        default=1,
        help_text="Applied frontmatter schema version"
    )

    title = models.CharField(max_length=255)

    doctype = models.CharField(
        max_length=50,
        choices=NoteType.choices,
        default=NoteType.TEMP
    )

    date = models.DateField(
        null=True,
        blank=True,
        help_text="Semantic date (mainly for journal entries)"
    )

    interval = models.JSONField(
        null=True,
        blank=True,
        help_text="Semantic time interval (mainly for journal entries)"
    )

    # ───────────────────────────────
    # Vault mapping (operational)
    # ───────────────────────────────

    vault_path = models.CharField(
        max_length=1024,
        unique=True,
        help_text="Relative path of the markdown file in the vault"
    )

    vault_mtime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last modification time reported by the filesystem"
    )

    # ───────────────────────────────
    # Core content
    # ───────────────────────────────

    content = models.TextField()

    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Parsed YAML frontmatter (unmapped fields)"
    )

    # ───────────────────────────────
    # Hashes & versioning
    # ───────────────────────────────

    content_hash = models.CharField(
        max_length=64,
        help_text="Hash of the current markdown body"
    )

    metadata_hash = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text="Hash of the YAML frontmatter"
    )

    last_synced_hash = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text="Hash at last successful sync"
    )

    # ───────────────────────────────
    # Sync control
    # ───────────────────────────────

    sync_status = models.CharField(
        max_length=20,
        choices=SyncStatus.choices,
        default=SyncStatus.CLEAN
    )

    last_modified_from = models.CharField(
        max_length=10,
        choices=ModifiedFrom.choices,
        default=ModifiedFrom.DB
    )

    last_sync_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of the last successful synchronization"
    )

    # ───────────────────────────────
    # Conflict handling
    # ───────────────────────────────

    conflict = models.BooleanField(default=False)

    conflict_data = models.JSONField(
        null=True,
        blank=True,
        help_text="Structured conflict payload"
    )

    # ───────────────────────────────
    # Timestamps (operational)
    # ───────────────────────────────

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ───────────────────────────────
    # Meta
    # ───────────────────────────────

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["doctype"]),
            models.Index(fields=["date"]),
            models.Index(fields=["sync_status"]),
            models.Index(fields=["vault_path"]),
            models.Index(fields=["schema_version"]),
        ]

    def __str__(self):
        return f"[{self.id}] {self.title} ({self.doctype})"

    # ───────────────────────────────
    # Helpers
    # ───────────────────────────────

    def mark_synced(self):
        self.last_synced_hash = self.content_hash
        self.sync_status = self.SyncStatus.CLEAN
        self.conflict = False
        self.conflict_data = None
        self.last_sync_at = timezone.now()