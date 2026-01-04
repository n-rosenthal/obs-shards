"""
    `shards/apps/notes/tasks.py`
    
    Celery tasks for syncing Obsidian vaults
"""
#   Celery
from celery import shared_task

#   Django
from django.conf import settings

#   Services for importing and exporting Vault content
from apps.notes.services.vault_service import (
    VaultImportService,
    VaultExportService,
)

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=60)
def sync_vault(self):
    """
    Sync the Obsidian vault in the `VAULT_PATH` directory with the database.

    The task will first import all notes from the vault, then export all notes in the database to the vault.
    The task will retry itself if any exceptions occur, with a backoff of 60 seconds.

    Returns a dictionary containing the number of imported and exported notes.
    """
    vault_path = settings.VAULT_PATH

    importer = VaultImportService(vault_path)
    exporter = VaultExportService(vault_path)

    import_result = importer.run()
    export_count = exporter.run()

    return {
        "import": import_result,
        "exported": export_count,
    }
