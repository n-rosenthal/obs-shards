"""
    `shards/scripts/export_vault.py`
    
    Script for exporting an Obsidian vault from the system.
"""

from pathlib import Path
import yaml
from apps.notes.models import Note

EXPORT_PATH = Path("/vault_export")


def run():
    EXPORT_PATH.mkdir(parents=True, exist_ok=True)

    for note in Note.objects.all():
        frontmatter = {
            "title": note.title,
            "doctype": note.doctype,
            "date": note.date.isoformat() if note.date else None,
            **note.metadata,
        }

        content = f"""---
{yaml.safe_dump(frontmatter, sort_keys=False)}
---

{note.content}
"""

        filename = f"{note.title.replace(' ', '_')}.md"
        (EXPORT_PATH / filename).write_text(content, encoding="utf-8")

    print(f"Exported {Note.objects.count()} notes.")
