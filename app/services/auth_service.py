"""
Authentication Service

Contains all business logic related to authentication.
"""

import uuid

from flask import current_app, jsonify

from app.repositories.user_repository import UserRepository
from app.utils.password_utils import (
    hash_password,
    verify_password,
)
from app.utils.jwt import create_token
from app.utils.responses import error
from app.utils.responses import success
from app.utils.validators import (validate_register_data,validate_login_data,)


class AuthService:

    @staticmethod
    def register(data: dict):
        validate_register_data(data)

        username = data.get("username").strip()
        password = data.get("password")
        preferences = data.get("preferences", [])

        if UserRepository.get_by_username(username):
            return error("username already exists",409)

        user = {
            "id": str(uuid.uuid4()),
            "username": username,
            "password_hash": hash_password(password),
            "preferences": preferences,
        }

        UserRepository.save(user)

        return success(
        data={
            "username": username
        },
        message="User registered successfully",
        status=201
)

    @staticmethod
    def login(data: dict):
        validate_login_data(data)

        username = data.get("username").strip()
        password = data.get("password")

        user = UserRepository.get_by_username(username)

        if not user:
            return error("invalid credentials", 401)

        if not verify_password(
            password,
            user["password_hash"],
        ):
            return error("invalid credentials", 401)

        token = create_token(
            username,
            current_app.config["SECRET_KEY"],
        )

        return success(data={"token": token },message="Login successful",status=200
)