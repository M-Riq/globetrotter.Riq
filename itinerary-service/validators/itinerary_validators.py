from common.exceptions import ValidationException


def validate_generate_request(data: dict):
    for field in ("origin_lat", "origin_lng", "destination_id"):
        if data.get(field) in (None, ""):
            raise ValidationException(f"{field} is required.")
    try:
        float(data["origin_lat"])
        float(data["origin_lng"])
    except (TypeError, ValueError):
        raise ValidationException("origin_lat/origin_lng must be numbers.")


def validate_reached_data(data: dict):
    if not data.get("destination_id"):
        raise ValidationException("destination_id is required.")
