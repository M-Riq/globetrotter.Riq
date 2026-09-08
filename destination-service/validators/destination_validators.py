"""
Destination Validators.

Validation centralisée des données liées aux destinations GlobeTrotter.
Les coordonnées latitude/longitude sont obligatoires pour permettre :
- l'affichage des destinations sur la carte,
- le calcul des distances,
- le calcul des itinéraires Mapbox,
- les recherches autour d'une destination.
"""

import config

from common.exceptions import ValidationException


REQUIRED_FIELDS = [
    "name",
    "description",
    "category",
    "latitude",
    "longitude",
]


def validate_destination_data(
    data: dict,
    partial: bool = False,
):
    """
    Validate destination data.

    Args:
        data: Destination payload.
        partial: If True, only fields present in data are validated.
    """

    # ============================================================
    # REQUIRED FIELDS
    # ============================================================

    if not partial:
        for field in REQUIRED_FIELDS:
            if data.get(field) in (None, ""):
                raise ValidationException(
                    f"{field} is required."
                )

    # ============================================================
    # NAME
    # ============================================================

    if "name" in data and data["name"] is not None:
        if not isinstance(data["name"], str):
            raise ValidationException(
                "name must be a string."
            )

        if not data["name"].strip():
            raise ValidationException(
                "name cannot be empty."
            )

    # ============================================================
    # DESCRIPTION
    # ============================================================

    if "description" in data and data["description"] is not None:
        if not isinstance(data["description"], str):
            raise ValidationException(
                "description must be a string."
            )

    # ============================================================
    # CATEGORY
    # ============================================================

    if "category" in data and data["category"]:
        if data["category"] not in config.CATEGORIES:
            raise ValidationException(
                f"category must be one of: "
                f"{', '.join(config.CATEGORIES)}"
            )

    # ============================================================
    # COORDINATES
    # ============================================================

    if "latitude" in data and data["latitude"] is not None:
        try:
            latitude = float(data["latitude"])
        except (TypeError, ValueError):
            raise ValidationException(
                "latitude must be a number."
            )

        if not -90 <= latitude <= 90:
            raise ValidationException(
                "latitude must be between -90 and 90."
            )

    if "longitude" in data and data["longitude"] is not None:
        try:
            longitude = float(data["longitude"])
        except (TypeError, ValueError):
            raise ValidationException(
                "longitude must be a number."
            )

        if not -180 <= longitude <= 180:
            raise ValidationException(
                "longitude must be between -180 and 180."
            )

    # ============================================================
    # TAGS
    # ============================================================

    if "tags" in data and data["tags"] is not None:
        if not isinstance(data["tags"], list):
            raise ValidationException(
                "tags must be a list."
            )

    # ============================================================
    # IMAGES
    # ============================================================

    if "images" in data and data["images"] is not None:
        if not isinstance(data["images"], list):
            raise ValidationException(
                "images must be a list."
            )

    # ============================================================
    # OPENING HOURS
    # ============================================================

    if "opening_hours" in data and data["opening_hours"] is not None:
        if not isinstance(data["opening_hours"], (str, list, dict)):
            raise ValidationException(
                "opening_hours must be a string, list or object."
            )

    # ============================================================
    # BUDGET
    # ============================================================

    if "budget_estimate" in data and data["budget_estimate"] is not None:
        try:
            budget = float(data["budget_estimate"])
        except (TypeError, ValueError):
            raise ValidationException(
                "budget_estimate must be a number."
            )

        if budget < 0:
            raise ValidationException(
                "budget_estimate cannot be negative."
            )

    # ============================================================
    # RATING
    # ============================================================

    if "rating" in data and data["rating"] is not None:
        try:
            rating = float(data["rating"])
        except (TypeError, ValueError):
            raise ValidationException(
                "rating must be a number."
            )

        if not 0 <= rating <= 5:
            raise ValidationException(
                "rating must be between 0 and 5."
            )

    # ============================================================
    # POPULARITY
    # ============================================================

    if "popularity" in data and data["popularity"] is not None:
        try:
            popularity = float(data["popularity"])
        except (TypeError, ValueError):
            raise ValidationException(
                "popularity must be a number."
            )

        if popularity < 0:
            raise ValidationException(
                "popularity cannot be negative."
            )