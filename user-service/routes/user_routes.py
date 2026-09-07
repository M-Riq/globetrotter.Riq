"""
User Routes -- visitor-facing profile, preferences, favorites, history.
"""
from flask import Blueprint, request

from common.jwt_utils import require_auth
from services.user_service import UserService

user_bp = Blueprint("users", __name__)


@user_bp.route("/me", methods=["GET"])
@require_auth
def get_me():
    return UserService.get_profile(request.current_user)


@user_bp.route("/me", methods=["PUT"])
@require_auth
def update_me():
    return UserService.update_profile(request.current_user, request.get_json(silent=True) or {})


@user_bp.route("/me/favorites", methods=["GET"])
@require_auth
def list_favorites():
    return UserService.list_favorites(request.current_user)


@user_bp.route("/me/favorites", methods=["POST"])
@require_auth
def add_favorite():
    return UserService.add_favorite(request.current_user, request.get_json(silent=True) or {})


@user_bp.route("/me/favorites/<destination_id>", methods=["DELETE"])
@require_auth
def remove_favorite(destination_id):
    return UserService.remove_favorite(request.current_user, destination_id)
