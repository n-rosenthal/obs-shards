"""
    `backend/apps/notes/services/vault_service.py`
    
    Obsidian vault services for importing and exporting content.
    
    The vault synchronization tasks apply a `diff` function for content hashing and visualizing the changes in the files.
"""

import hashlib

from pathlib import Path
from django.utils import timezone

from apps.notes.models import Note



def compute_hash(content: str) -> str:
    """
        Computes the SHA-256 hash for a given `content` string.
        
        params:
        ---
            content (str): The content to be hashed.
            
        returns:
        ---
            str: The SHA-256 hash of the content.
    """
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

class VaultImportService:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)

    def run(self) -> dict:
        created = 0
        updated = 0
        skipped = 0

        for md_file in self.vault_path.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            content_hash = compute_hash(content)

            note, was_created = Note.objects.get_or_create(
                metadata__vault_path=str(md_file),
                defaults={
                    "title": md_file.stem,
                    "content": content,
                    "metadata": {
                        "vault_path": str(md_file),
                        "content_hash": content_hash,
                    },
                }
            )

            if was_created:
                created += 1
                continue

            stored_hash = note.metadata.get("content_hash")
            if stored_hash == content_hash:
                skipped += 1
                continue

            note.content = content
            note.metadata["content_hash"] = content_hash
            note.updated_at = timezone.now()
            note.save(update_fields=["content", "metadata", "updated_at"])

            updated += 1

        return {
            "created": created,
            "updated": updated,
            "skipped": skipped,
        }


class VaultExportService:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)

    def run(self) -> dict:
        exported = 0
        skipped = 0

        for note in Note.objects.all():
            vault_path = note.metadata.get("vault_path")

            if not vault_path:
                skipped += 1
                continue

            file_path = self.vault_path / vault_path
            file_path.parent.mkdir(parents=True, exist_ok=True)

            content = note.content
            content_hash = compute_hash(content)

            # simple diff, prep. for further implementations
            if file_path.exists():
                existing = file_path.read_text(encoding="utf-8")
                if compute_hash(existing) == content_hash:
                    skipped += 1
                    continue

            file_path.write_text(content, encoding="utf-8")

            note.metadata["content_hash"] = content_hash
            note.metadata["exported_at"] = timezone.now().isoformat()
            note.save(update_fields=["metadata", "updated_at"])

            exported += 1

        return {
            "exported": exported,
            "skipped": skipped,
        }