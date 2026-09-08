"""
Base Repository.

Generic CRUD delegated to an injected storage backend (see
common/storage/). Domain repositories subclass this and add
domain-specific query methods (get_by_username, get_by_category, ...)
exactly like in the original monolith.
"""


class BaseRepository:
    def __init__(self, storage):
        self.storage = storage

    def get_all(self):
        return self.storage.get_all()

    def get_by_id(self, record_id, id_field: str = "id"):
        return self.storage.get_by_id(record_id, id_field)

    def save(self, record):
        self.storage.append(record)
        return record

    def update(self, record_id, updates: dict, id_field: str = "id"):
        return self.storage.update(record_id, updates, id_field)

    def delete(self, record_id, id_field: str = "id"):
        return self.storage.delete(record_id, id_field)
