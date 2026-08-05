"""
app/destinations.py

Destination search endpoint.

Routes
------
GET /destinations?q=paris&tag=food&continent=Europe
    Returns destinations that match any of the provided query parameters.
    All parameters are optional; omitting them returns the full catalogue.
"""
from flask import Blueprint, request, jsonify

from app.services.destination_service import DestinationService
# from app.repositories.destination_repository import DestinationRepository

# ---------------------------------------------------------------------------
# 1 — Le Blueprint
# ---------------------------------------------------------------------------
destinations_bp = Blueprint("destinations", __name__)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 2 — La route
# ---------------------------------------------------------------------------
@destinations_bp.route("/destination s", methods=["GET"])
def search_destinations():

    return DestinationService.search(
        request.args
    )
# ---------------------------------------------------------------------------

