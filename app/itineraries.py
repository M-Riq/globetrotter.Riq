"""
Itinerary Routes
"""

from flask import Blueprint, request

from app.utils.jwt import get_current_user
from app.utils.responses import error
from app.services.itinerary_service import ItineraryService


itineraries_bp = Blueprint(
    "itineraries",
    __name__,
)


@itineraries_bp.route(
    "/itineraries",
    methods=["POST"],
)
def create_itinerary():

    username = get_current_user(request)

    if not username:
        return error(
            "authentication required",
            401,
        )

    data = request.get_json(silent=True) or {}

    return ItineraryService.create(
        username,
        data,
    )


@itineraries_bp.route(
    "/itineraries",
    methods=["GET"],
)
def list_itineraries():

    username = get_current_user(request)

    if not username:
        return error(
            "authentication required",
            401,
        )

    return ItineraryService.get_all(
        username,
    )