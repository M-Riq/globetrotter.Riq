"""
Itinerary Routes.
"""
from flask import Blueprint, request

from common.jwt_utils import require_auth
from services.itinerary_service import ItineraryService

itinerary_bp = Blueprint("itineraries", __name__)


@itinerary_bp.route("/generate", methods=["POST"])
@require_auth
def generate_itinerary():
    """Preview a route (origin -> destination) without saving it."""
    return ItineraryService.generate(request.get_json(silent=True) or {})


@itinerary_bp.route("", methods=["POST"])
@require_auth
def create_itinerary():
    """Save an itinerary -- typically once the visitor has reached (or
    plans to reach) a destination, with their impression/rating."""
    return ItineraryService.create(request.current_user["sub"], request.get_json(silent=True) or {})


@itinerary_bp.route("", methods=["GET"])
@require_auth
def list_itineraries():
    return ItineraryService.list_for_user(request.current_user["sub"])


@itinerary_bp.route("/<itinerary_id>", methods=["GET"])
@require_auth
def get_itinerary(itinerary_id):
    return ItineraryService.get_one(request.current_user["sub"], itinerary_id)


@itinerary_bp.route("/<itinerary_id>/share", methods=["POST"])
@require_auth
def share_itinerary(itinerary_id):
    return ItineraryService.share_whatsapp(request.current_user["sub"], itinerary_id)
