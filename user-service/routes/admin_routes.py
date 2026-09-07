"""
Admin-only User Management Routes.
"""
from flask import Blueprint

from common.jwt_utils import require_role
from services.user_service import UserService

admin_user_bp = Blueprint("admin_users", __name__)


@admin_user_bp.route("", methods=["GET"])
@require_role("admin")
def list_users():
    return UserService.list_all_profiles()


@admin_user_bp.route("/<user_id>", methods=["GET"])
@require_role("admin")
def get_user(user_id):
    return UserService.get_profile_by_id(user_id)


@admin_user_bp.route("/<user_id>", methods=["DELETE"])
@require_role("admin")
def delete_user(user_id):
    return UserService.delete_profile(user_id)
