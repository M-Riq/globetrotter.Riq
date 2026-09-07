"""
Internal (service-to-service) Routes.

Not exposed through the API Gateway's public routing table. Called
by the Auth Service right after a successful registration so the
User Service can create the profile shell (preferences, empty
favorites/history) immediately.
"""
from flask import Blueprint, request

from common.responses import error
import config
from services.user_service import UserService

internal_bp = Blueprint("internal_users", __name__)


@internal_bp.route("/profiles", methods=["POST"])
def init_profile():
    if request.headers.get("X-Internal-Key") != config.INTERNAL_SERVICE_KEY:
        return error("forbidden", 403)
    return UserService.init_profile(request.get_json(silent=True) or {})
