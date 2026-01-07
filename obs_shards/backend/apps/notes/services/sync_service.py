"""
    `backend/apps/notes/services/sync_service.py`
    
    Services for syncing Obsidian vaults
"""

import time
import redis

from apps.notes.services.vault_service import (
    VaultImportService,
    VaultExportService,
)

class DistributedLock:
    """
    A distributed lock implementation using Redis.
    """
    def __init__(self, key: str, timeout=300):
        """
        Initialize a DistributedLock instance.

        :param key: str, the key for the lock
        :param timeout: int, the timeout for the lock in seconds
        """
        self.key = key
        self.timeout = timeout
        self.client = redis.Redis.from_url("redis://redis:6379/0")

    def acquire(self) -> bool:
        """
        Acquires the distributed lock.

        :return: bool, True if the lock was acquired successfully, False otherwise
        """
        return self.client.set(self.key, "1", nx=True, ex=self.timeout)

    def release(self):
        """
        Releases the distributed lock.
        """
        self.client.delete(self.key)


def sync_vault():
    lock = DistributedLock("vault_sync_lock")

    if not lock.acquire():
        return {"status": "skipped", "reason": "lock_active"}

    try:
        import_result = VaultImportService("/vault").run()
        export_result = VaultExportService("/vault").run()

        return {
            "import": import_result,
            "export": export_result,
        }
    finally:
        lock.release()
