"""
    `backend/apps/notes/services/conflict_detector.py`
    
    Simple conflict detector for Obsidian vault sync
"""

class ConflictDetector:
    @staticmethod
    def check_import_conflict(note, parsed) -> bool:
        if note.last_synced_hash is None:
            return False

        db_changed = note.content_hash != note.last_synced_hash
        file_changed = parsed.content_hash != note.last_synced_hash

        return db_changed and file_changed
