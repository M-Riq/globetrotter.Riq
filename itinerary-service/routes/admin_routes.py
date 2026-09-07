"""
Admin-only, read-only Itinerary Routes.

Admins consult itinerary/reach data for stats -- they never create
itineraries (only destinations).
"""
from flask import Blueprint

from common.jwt_utils import require_role
from services.itinerary_service import ItineraryService

admin_itinerary_bp = Blueprint("admin_itineraries", __name__)


@admin_itinerary_bp.route("", methods=["GET"])
@require_role("admin")
def list_all_itineraries():
    return ItineraryService.admin_list_all()
