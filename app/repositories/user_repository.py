"""
User Repository
"""

import os

from app.data.json_storage import (
    read_json,
    write_json,
)
from app.config import USERS_FILE

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# USERS_FILE = os.path.join(
#     BASE_DIR,
#     "data",
#     "users.json",
# )


class UserRepository:

    @staticmethod
    def get_all():

        return read_json(USERS_FILE)

    @staticmethod
    def get_by_username(username):

        users = UserRepository.get_all()

        for user in users:

            if user["username"] == username:
                return user

        return None

    @staticmethod
    def save(user):

        users = UserRepository.get_all()

        users.append(user)

        write_json(
            USERS_FILE,
            users,
        )