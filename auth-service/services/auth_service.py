"""
Authentication Service.

Contains all business logic related to authentication. Layering
(Route -> Service -> Repository, standardized responses, Validators)
is preserved exactly as in the original monolith.
"""
import uuid

import requests
from flask import current_app

from common.exceptions import ValidationException
from common.jwt_utils import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
)
from common.password_utils import hash_password, verify_password
from common.responses import error, success
from repositories.user_repository import UserRepository
from validators.auth_validators import validate_login_data, validate_register_data

import config


class AuthService:
    repository = UserRepository()

    @staticmethod
    def register(data: dict):
        try:
            validate_register_data(data)
        except ValidationException as exc:
            return error(exc.message, 400)

        username = data.get("username").strip()
        password = data.get("password")
        email = (data.get("email") or "").strip()
        preferences = data.get("preferences", []) or []

        if AuthService.repository.get_by_username(username):
            return error("username already exists", 409)

        user = {
            "id": str(uuid.uuid4()),
            "username": username,
            "email": email,
            "password_hash": hash_password(password),
            "role": "user",
            "preferences": preferences,
        }
        AuthService.repository.save(user)
        AuthService._init_user_profile(user["id"], username, preferences)

        return success(
            data={"id": user["id"], "username": username, "preferences": preferences},
            message="User registered successfully",
            status=201,
        )

    @staticmethod
    def _init_user_profile(user_id: str, username: str, preferences: list):
        """Best-effort call to the User Service so the profile shell
        (preferences, empty favorites/history) exists immediately.
        Registration must never fail just because the User Service is
        momentarily unavailable -- it will lazily create the profile
        itself on first access."""
        try:
            requests.post(
                f"{config.USER_SERVICE_URL}/internal/users/profiles",
                json={"user_id": user_id, "username": username, "preferences": preferences},
                headers={"X-Internal-Key": config.INTERNAL_SERVICE_KEY},
                timeout=3,
            )
        except requests.RequestException:
            current_app.logger.warning("Could not reach user-service to init profile for %s", user_id)

    @staticmethod
    def login(data: dict):
        try:
            validate_login_data(data)
        except ValidationException as exc:
            return error(exc.message, 400)

        username = data.get("username").strip()
        password = data.get("password")

        user = AuthService.repository.get_by_username(username)
        if not user or not verify_password(password, user["password_hash"]):
            return error("invalid credentials", 401)

        secret = current_app.config["SECRET_KEY"]
        access_token = create_access_token(user["id"], user["username"], user.get("role", "user"), secret)
        refresh_token = create_refresh_token(user["id"], secret)

        return success(
            data={
                "token": access_token,
                "refresh_token": refresh_token,
                "user": {"id": user["id"], "username": user["username"], "role": user.get("role", "user")},
            },
            message="Login successful",
            status=200,
        )

    @staticmethod
    def admin_login(data: dict):
        email = (data.get("username") or data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        if not email or not password:
            return error("email and password are required", 400)

        if email != config.ADMIN_EMAIL.lower() or password != config.ADMIN_PASSWORD:
            return error("invalid credentials", 401)

        secret = current_app.config["SECRET_KEY"]
        access_token = create_access_token("admin", config.ADMIN_EMAIL, "admin", secret)
        refresh_token = create_refresh_token("admin", secret)

        return success(
            data={
                "token": access_token,
                "refresh_token": refresh_token,
                "user": {"id": "admin", "username": config.ADMIN_EMAIL, "role": "admin"},
            },
            message="Admin login successful",
            status=200,
        )

    @staticmethod
    def refresh(data: dict):
        token = data.get("refresh_token")
        if not token:
            return error("refresh_token is required", 400)

        secret = current_app.config["SECRET_KEY"]
        try:
            payload = decode_token(token, secret)
        except Exception:
            return error("invalid or expired refresh token", 401)

        if payload.get("type") != "refresh":
            return error("invalid token type", 401)

        user_id = payload["sub"]
        if user_id == "admin":
            new_access = create_access_token("admin", config.ADMIN_EMAIL, "admin", secret)
        else:
            user = AuthService.repository.get_by_id(user_id)
            if not user:
                return error("user not found", 404)
            new_access = create_access_token(user["id"], user["username"], user.get("role", "user"), secret)

        return success(data={"token": new_access}, message="Token refreshed", status=200)

    @staticmethod
    def verify(request_obj):
        secret = current_app.config["SECRET_KEY"]
        payload = get_current_user(request_obj, secret)
        if not payload:
            return error("invalid or missing token", 401)
        return success(data=payload, message="Token is valid", status=200)
