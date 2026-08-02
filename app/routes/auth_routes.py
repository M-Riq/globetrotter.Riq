# ---------------------------------------------------------------------------
# Authentication Routes
# ---------------------------------------------------------------------------

from flask import Blueprint, request

from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    return AuthService.register(
        request.get_json(silent=True) or {}
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    return AuthService.login(
        request.get_json(silent=True) or {}
    )