"""
Authentication Routes.
"""
from flask import Blueprint, request

from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    return AuthService.register(request.get_json(silent=True) or {})


@auth_bp.route("/login", methods=["POST"])
def login():
    return AuthService.login(request.get_json(silent=True) or {})


@auth_bp.route("/admin/login", methods=["POST"])
def admin_login():
    return AuthService.admin_login(request.get_json(silent=True) or {})


@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    return AuthService.refresh(request.get_json(silent=True) or {})


@auth_bp.route("/verify", methods=["GET"])
def verify():
    """Used internally by other services / the gateway to validate a
    token without re-implementing JWT logic themselves, if needed."""
    return AuthService.verify(request)
