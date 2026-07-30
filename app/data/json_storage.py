"""
Generic JSON storage utilities.
"""

import json
import os


def read_json(filepath: str) -> list:
    """
    Read a JSON file and return its content.
    """

    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding="utf-8") as file:

        content = file.read().strip()

        if not content:
            return []

        return json.loads(content)


def write_json(filepath: str, data: list):

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as file:

        json.dump(data, file, indent=2)