"""
    `backend/apps/notes/services/vault_importer.py`
    
    Obsidian vault import service
"""

from pathlib import Path
from apps.notes.models import Note
from apps.notes.services.markdown_parser import MarkdownParser
from apps.notes.services.conflict_detector import ConflictDetector

class VaultImportService:
    """
    Obsidian Vault import service
    """
    def __init__(self, vault_path: str):
        """
        Initializes a VaultImportService instance.

        :param vault_path: str, the path to the Obsidian vault to be imported
        """
        self.vault = Path(vault_path)

    def run(self) -> dict:
        """
        Imports all notes from the Obsidian vault into the database.

        :return: A dictionary containing the number of created, updated, and conflicted notes.
        :rtype: dict[str, int]
        """
        results = {"created": 0, "updated": 0, "conflicts": 0}

        for file in self.vault.rglob("*.md"):
            external_id = file.relative_to(self.vault).as_posix()
            text = file.read_text(encoding="utf-8")

            parsed = MarkdownParser.parse(text)

            note, created = Note.objects.get_or_create(
                external_id=external_id,
                defaults={
                    "title": parsed.metadata.get("title", file.stem),
                    "content": parsed.content,
                    "content_hash": parsed.content_hash,
                    "metadata": parsed.metadata,
                }
            )

            if created:
                results["created"] += 1
                continue

            conflict = ConflictDetector.check_import_conflict(note, parsed)

            if conflict:
                note.mark_conflict(parsed)
                results["conflicts"] += 1
                continue

            if note.content_hash != parsed.content_hash:
                note.content = parsed.content
                note.metadata = parsed.metadata
                note.content_hash = parsed.content_hash
                note.save()
                results["updated"] += 1

        return results
