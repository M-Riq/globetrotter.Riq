"""
User Repository
"""

from app.config import USERS_FILE
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):

    def __init__(self):
        super().__init__(USERS_FILE)

    def get_by_username(self, username):

        users = self.get_all()

        for user in users:

            if user["username"] == username:
                return user

        return None

    def save(self, user):

        self.append(user)