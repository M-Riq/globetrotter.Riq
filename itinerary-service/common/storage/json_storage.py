"""
JSON-file storage backend (current, transitional implementation).

Uses a lock file alongside the data file so concurrent Gunicorn
workers within the same service don't corrupt writes.
"""
import json
import os

from filelock import FileLock

from common.storage.base_storage import BaseStorage


class JSONStorage(BaseStorage):
    """Generic JSON-file storage for a single collection."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.lock_path = f"{filepath}.lock"

    def get_all(self) -> list:
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as file:
            content = file.read().strip()
        if not content:
            return []
        return json.loads(content)

    def save_all(self, records: list) -> None:
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with FileLock(self.lock_path):
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump(records, file, indent=2, ensure_ascii=False)
