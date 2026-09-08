"""
User (credentials) Repository.

Owns ONLY authentication data (id, username, email, password hash,
role). Profile data (preferences, favorites, history) belongs to the
User Service's own repository -- each microservice owns its slice of
data, they are linked only by user id.
"""
from common.base_repository import BaseRepository
from common.storage.json_storage import JSONStorage

import config


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(JSONStorage(config.USERS_FILE))

    def get_by_username(self, username: str):
        username = username.lower()
        for user in self.get_all():
            if user.get("username", "").lower() == username:
                return user
        return None
