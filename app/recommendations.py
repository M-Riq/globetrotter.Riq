"""
Recommendations Routes

Personalised destination recommendations.

Routes
------
GET /recommendations
    Returns destinations that best match the authenticated user's preferences.
    Requires a valid JWT in the Authorization header.
"""
from flask import Blueprint, request

from app.utils.jwt import get_current_user
from app.utils.jwt import get_current_user
from app.services.recommendation_service import RecommendationService
from app.utils.responses import error


recommendations_bp = Blueprint("recommendations", __name__)


@recommendations_bp.route("/recommendations", methods=["GET"])
@recommendations_bp.route(
    "/recommendations",
    methods=["GET"],
)
def get_recommendations():

    username = get_current_user(request)

    if not username:
        return error(
            "authentication required",
            401,
        )

    try:
        limit = int(
            request.args.get("limit", 5)
        )
    except ValueError:
        return error(
            "limit must be an integer",
            400,
        )

    return RecommendationService.get_recommendations(
        username,
        limit,
    )