"""
Admin Destination Routes -- create/modify/delete/consult.
"""
from flask import Blueprint, request

from common.jwt_utils import require_role
from services.destination_service import DestinationService

admin_destination_bp = Blueprint("admin_destinations", __name__)


@admin_destination_bp.route("", methods=["GET"])
@require_role("admin")
def list_destinations():
    return DestinationService.admin_list()


@admin_destination_bp.route("", methods=["POST"])
@require_role("admin")
def create_destination():
    return DestinationService.create(request.get_json(silent=True) or {})


@admin_destination_bp.route("/<destination_id>", methods=["PUT"])
@require_role("admin")
def update_destination(destination_id):
    return DestinationService.update(destination_id, request.get_json(silent=True) or {})


@admin_destination_bp.route("/<destination_id>", methods=["DELETE"])
@require_role("admin")
def delete_destination(destination_id):
    return DestinationService.delete(destination_id)
