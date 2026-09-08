"""
Standardized API responses.

Kept byte-for-byte compatible with the original monolith's contract
(app/utils/responses.py) so the already-built Next.js frontend keeps
working unchanged against every microservice.
"""
from flask import jsonify


def success(data=None, message=None, status=200):
    payload = {}
    if message:
        payload["message"] = message
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status


def error(message, status=400):
    return jsonify({
        "success": False,
        "error": message,
    }), status
