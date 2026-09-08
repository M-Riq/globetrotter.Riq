"""
Shared JWT + RBAC utilities used by every GlobeTrotter microservice.

This is the single source of truth for how tokens are minted and
validated. It is copied into each service's Docker build context
(see each service's Dockerfile) so that every service authenticates
requests identically without duplicating the business logic itself
(only the file is duplicated at build time, not the logic).

Token payload shape:
    {
        "sub": "<user id, or 'admin'>",
        "username": "<username or admin email>",
        "role": "user" | "admin",
        "type": "access" | "refresh",
        "iat": <issued at>,
        "exp": <expiry>,
    }
"""
import datetime
from functools import wraps

import jwt
from flask import current_app, request

from common.responses import error

ACCESS_TOKEN_EXPIRES_HOURS = 24
REFRESH_TOKEN_EXPIRES_DAYS = 30


def create_access_token(user_id: str, username: str, role: str, secret: str) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "sub": user_id,
        "username": username,
        "role": role,
        "type": "access",
        "iat": now,
        "exp": now + datetime.timedelta(hours=ACCESS_TOKEN_EXPIRES_HOURS),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def create_refresh_token(user_id: str, secret: str) -> str:
    """Prepared refresh-token support (per spec: 'préparer le support du
    Refresh Token'). Longer-lived, carries no role/username so it can't
    be used directly as an access token even if replayed against a
    protected route."""
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "sub": user_id,
        "type": "refresh",
        "iat": now,
        "exp": now + datetime.timedelta(days=REFRESH_TOKEN_EXPIRES_DAYS),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_token(token: str, secret: str) -> dict:
    return jwt.decode(token, secret, algorithms=["HS256"])


def get_current_user(request_obj, secret: str):
    """Extract + validate the JWT from the Authorization header.

    Returns the decoded access-token payload (dict) if valid, else None.
    """
    auth_header = request_obj.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ", 1)[1]
    try:
        payload = decode_token(token, secret)
    except jwt.PyJWTError:
        return None
    if payload.get("type") != "access":
        return None
    return payload


def require_auth(view_func):
    """Route decorator: any authenticated user (user or admin)."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        secret = current_app.config["SECRET_KEY"]
        user = get_current_user(request, secret)
        if not user:
            return error("authentication required", 401)
        request.current_user = user
        return view_func(*args, **kwargs)

    return wrapper


def require_role(*roles):
    """Route decorator implementing RBAC, e.g. @require_role('admin')."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            secret = current_app.config["SECRET_KEY"]
            user = get_current_user(request, secret)
            if not user:
                return error("authentication required", 401)
            if user.get("role") not in roles:
                return error("insufficient permissions", 403)
            request.current_user = user
            return view_func(*args, **kwargs)

        return wrapper

    return decorator
