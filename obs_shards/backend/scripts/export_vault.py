"""
    `shards/scripts/export_vault.py`
    
    Script for exporting an Obsidian vault from the system.
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.notes.services.vault_service import VaultExportService

if __name__ == "__main__":
    service = VaultExportService("/vault")
    result = service.run()
    print(result)
