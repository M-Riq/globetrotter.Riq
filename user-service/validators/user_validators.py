from common.exceptions import ValidationException


def validate_profile_update(data: dict):
    preferences = data.get("preferences")
    if preferences is not None and not isinstance(preferences, list):
        raise ValidationException("preferences must be a list.")


def validate_favorite_data(data: dict):
    if not data.get("destination_id"):
        raise ValidationException("destination_id is required.")
