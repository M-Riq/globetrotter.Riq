"""
Recommendation Routes.
"""
from flask import Blueprint, request

from common.jwt_utils import require_auth
from common.responses import error
from services.recommendation_service import RecommendationService

recommendation_bp = Blueprint("recommendations", __name__)


@recommendation_bp.route("", methods=["GET"])
@require_auth
def get_recommendations():
    try:
        limit = int(request.args.get("limit", 5))
    except ValueError:
        return error("limit must be an integer", 400)

    return RecommendationService.get_recommendations(
        auth_header=request.headers.get("Authorization"),
        limit=limit,
        lat=request.args.get("lat"),
        lng=request.args.get("lng"),
    )
