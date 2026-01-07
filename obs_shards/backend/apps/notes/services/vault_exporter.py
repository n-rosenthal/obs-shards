"""
    `backend/apps/notes/services/vault_exporter.py`
    
    Obsidian vault export service
"""


import yaml

from pathlib import Path

from apps.notes.models import Note


class VaultExportService:
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path)

    def run(self):
        exported = 0

        for note in Note.objects.filter(conflict=False):
            if note.content_hash == note.last_synced_hash:
                continue

            path = self.vault / note.external_id
            path.parent.mkdir(parents=True, exist_ok=True)

            text = self.render_markdown(note)
            path.write_text(text, encoding="utf-8")

            note.last_synced_hash = note.content_hash
            note.save()
            exported += 1

        return {"exported": exported}

    def render_markdown(self, note):
        frontmatter = yaml.safe_dump(note.metadata, sort_keys=False).strip()
        return f"""---
{frontmatter}
---

{note.content}
"""
