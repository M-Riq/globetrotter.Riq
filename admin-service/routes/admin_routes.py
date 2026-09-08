"""
Admin Dashboard Routes.
"""
from flask import Blueprint, request

from common.jwt_utils import require_role
from services.admin_service import AdminService

admin_bp = Blueprint("admin_dashboard", __name__)


@admin_bp.route("/dashboard/stats", methods=["GET"])
@require_role("admin")
def dashboard_stats():
    return AdminService.dashboard_stats(request.headers.get("Authorization"))
