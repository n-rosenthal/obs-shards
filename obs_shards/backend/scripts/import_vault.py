"""
    `shards/scripts/import_vault.py`
    
    Script for importing an Obsidian vault into the system.
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.notes.services.vault_service import VaultImportService

if __name__ == "__main__":
    service = VaultImportService("/vault")
    result = service.run()
    print(result)