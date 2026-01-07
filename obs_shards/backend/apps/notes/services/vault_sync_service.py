"""
    `backend/apps/notes/services/vault_sync_service.py`
    
    Services for syncing Obsidian vaults
"""


from apps.notes.services.vault_exporter import VaultExportService
from apps.notes.services.vault_importer import VaultImportService

class VaultSyncService:
    def __init__(self, vault_path):
        self.vault_path = vault_path

    def run(self):
        import_result = VaultImportService(self.vault_path).run()
        export_result = VaultExportService(self.vault_path).run()

        return {
            "import": import_result,
            "export": export_result
        }
