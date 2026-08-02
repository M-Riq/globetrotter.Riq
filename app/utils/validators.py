"""
Application validators.

Contains reusable validation functions.
"""

from app.exceptions.validation_exception import ValidationException


def validate_register_data(data: dict):
    """
    Validate registration payload.
    """

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username:
        raise ValidationException(
            "Username is required."
        )

    if not password:
        raise ValidationException(
            "Password is required."
        )


def validate_login_data(data: dict):
    """
    Validate login payload.
    """

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username:
        raise ValidationException(
            "Username is required."
        )

    if not password:
        raise ValidationException(
            "Password is required."
        )