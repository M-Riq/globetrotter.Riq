"""
JWT utilities.
"""
from flask import current_app
import datetime

import jwt


def create_token(username: str, secret: str) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)

    payload = {
        "sub": username,
        "iat": now,
        "exp": now + datetime.timedelta(hours=24),
    }

    return jwt.encode(payload, secret, algorithm="HS256")


def decode_token(token: str, secret: str):
    return jwt.decode(token, secret, algorithms=["HS256"])


def get_current_user(request_obj):
    """
    Extract and validate the JWT from the Authorization header.

    Returns:
        username (str) if authenticated
        None otherwise
    """

    auth_header = request_obj.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ", 1)[1]

    try:
        payload = decode_token(
            token,
            current_app.config["SECRET_KEY"],
        )

        return payload.get("sub")

    except jwt.PyJWTError:
        return None