"""
    `shards/scripts/import_vault.py`
    
    Script for importing an Obsidian vault into the system.
"""

import os
import yaml
from pathlib import Path
from django.utils.timezone import now

#   `Note` model
from apps.notes.models import Note

#   currently hard-coded Vault path
VAULT_PATH = Path("/vault")


def parse_markdown(file_path: Path) -> tuple[str, str, dict, str, str | None]:
    """
    Parse a markdown file and extract metadata, title, content, doctype and date.

    The markdown file is expected to have a YAML frontmatter section, separated by
    a "---" separator. The frontmatter section is parsed into a dictionary and
    returned as the metadata.

    The title is extracted from the frontmatter section, and defaults to the file name
    without extension if not found.

    The doctype is extracted from the frontmatter section, and defaults to "note" if not found.

    The date is extracted from the frontmatter section, and defaults to None if not found.

    :param file_path: Path to the markdown file
    :return: A tuple containing (title, content, metadata, doctype, date)
    """
    #   read the file
    text = file_path.read_text(encoding="utf-8")

    #   parse the frontmatter
    metadata = {}
    content = text

    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        metadata = yaml.safe_load(fm) or {}
        content = body.strip()

    #   extract title, doctype and date
    title = metadata.get("title", file_path.stem)
    doctype = metadata.get("doctype", "temp")
    date = metadata.get("date")

    return title, content, metadata, doctype, date


def run():
    """
    Import markdown files from the Vault directory into the database.

    Iterate over markdown files in the Vault directory, parse the YAML frontmatter and
    extract the title, content, metadata, doctype and date. Then, use Django's ORM
    to update or create a Note instance with the extracted data. The created and
    updated counts are printed at the end of the function.

    :return: None
    """
    created, updated = 0, 0

    for md_file in VAULT_PATH.rglob("*.md"):
        title, content, metadata, doctype, date = parse_markdown(md_file)

        note, is_created = Note.objects.update_or_create(
            title=title,
            defaults={
                "content": content,
                "metadata": metadata,
                "doctype": doctype,
                "date": date,
                "updated_at": now(),
            },
        )

        if is_created:
            created += 1
        else:
            updated += 1

    print(f"({note.id}) Import finished: {created} created, {updated} updated")
