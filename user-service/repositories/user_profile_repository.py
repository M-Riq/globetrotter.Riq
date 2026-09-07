"""
User Profile Repository.

Owns preferences, favorites and "reached destinations" history --
everything about a visitor EXCEPT credentials (which stay in the
Auth Service). Linked to the Auth Service's user record only by
`user_id`.
"""
from common.base_repository import BaseRepository
from common.storage.json_storage import JSONStorage

import config


class UserProfileRepository(BaseRepository):
    def __init__(self):
        super().__init__(JSONStorage(config.PROFILES_FILE))

    def get_by_user_id(self, user_id: str):
        return self.get_by_id(user_id, id_field="user_id")

    def upsert(self, profile: dict):
        existing = self.get_by_user_id(profile["user_id"])
        if existing:
            self.storage.update(profile["user_id"], profile, id_field="user_id")
        else:
            self.save(profile)
        return profile
