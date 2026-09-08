"""
Auth payload validators (same pattern as the monolith's
app/utils/validators.py, extended for email/preferences).
"""
from common.exceptions import ValidationException


def validate_register_data(data: dict):
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    preferences = data.get("preferences", [])

    if not username:
        raise ValidationException("Username is required.")
    if len(username) < 3:
        raise ValidationException("Username must be at least 3 characters.")
    if not password:
        raise ValidationException("Password is required.")
    if len(password) < 6:
        raise ValidationException("Password must be at least 6 characters.")
    if preferences is not None and not isinstance(preferences, list):
        raise ValidationException("preferences must be a list.")


def validate_login_data(data: dict):
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username:
        raise ValidationException("Username is required.")
    if not password:
        raise ValidationException("Password is required.")
