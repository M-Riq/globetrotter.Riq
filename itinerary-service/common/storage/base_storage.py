"""
Storage backend interface.

Every microservice's Repository layer talks ONLY to this interface,
never to a concrete file/DB implementation. Today the only
implementation is JSONStorage (keeping the monolith's JSON storage,
per spec). Tomorrow a PostgresStorage can implement the same
contract and be swapped in via config alone -- no Service or Route
code has to change, satisfying the "migration future vers
PostgreSQL sans modifier les Services" requirement.
"""
from abc import ABC, abstractmethod


class BaseStorage(ABC):

    @abstractmethod
    def get_all(self) -> list:
        """Return every record in the collection."""
        raise NotImplementedError

    @abstractmethod
    def save_all(self, records: list) -> None:
        """Persist the entire collection."""
        raise NotImplementedError

    def append(self, record: dict) -> None:
        records = self.get_all()
        records.append(record)
        self.save_all(records)

    def get_by_id(self, record_id: str, id_field: str = "id"):
        for record in self.get_all():
            if record.get(id_field) == record_id:
                return record
        return None

    def update(self, record_id: str, updates: dict, id_field: str = "id"):
        records = self.get_all()
        updated = None
        for record in records:
            if record.get(id_field) == record_id:
                record.update(updates)
                updated = record
                break
        if updated is not None:
            self.save_all(records)
        return updated

    def delete(self, record_id: str, id_field: str = "id") -> bool:
        records = self.get_all()
        filtered = [r for r in records if r.get(id_field) != record_id]
        if len(filtered) == len(records):
            return False
        self.save_all(filtered)
        return True
