"""
Destination Routes -- visitor-facing search/filter/consult.
"""
from flask import Blueprint, request

from services.destination_service import DestinationService

destination_bp = Blueprint("destinations", __name__)


@destination_bp.route("", methods=["GET"])
def search_destinations():
    return DestinationService.search(request.args)


@destination_bp.route("/<destination_id>", methods=["GET"])
def get_destination(destination_id):
    return DestinationService.get_by_id(destination_id)
