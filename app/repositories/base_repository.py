"""
Base Repository

Provides common JSON file operations for all repositories.
"""

import json
import os


class BaseRepository:
    """
    Generic repository for JSON storage.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath

    def get_all(self):
        """
        Return every record.
        """

        if not os.path.exists(self.filepath):
            return []

        with open(self.filepath, "r", encoding="utf-8") as file:

            content = file.read().strip()

            if not content:
                return []

            return json.loads(content)

    def save_all(self, data):
        """
        Save the entire collection.
        """

        os.makedirs(
            os.path.dirname(self.filepath),
            exist_ok=True,
        )

        with open(self.filepath, "w", encoding="utf-8") as file:

            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False,
            )

    def append(self, item):
        """
        Append one record.
        """

        records = self.get_all()

        records.append(item)

        self.save_all(records)