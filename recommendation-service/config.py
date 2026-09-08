import os

SERVICE_NAME = "recommendation-service"
PORT = int(os.environ.get("PORT", 5004))
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me")

USER_SERVICE_URL = os.environ.get("USER_SERVICE_URL", "http://user-service:5002")
DESTINATION_SERVICE_URL = os.environ.get("DESTINATION_SERVICE_URL", "http://destination-service:5003")

CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

# Relative weights used by the default scoring engine. Kept in config
# (not hardcoded in the engine) so they can be tuned, A/B tested, or
# eventually learned/overridden by a future ML-based scorer.
WEIGHTS = {
    "preference_match": float(os.environ.get("WEIGHT_PREFERENCE_MATCH", 4.0)),
    "rating": float(os.environ.get("WEIGHT_RATING", 2.0)),
    "popularity": float(os.environ.get("WEIGHT_POPULARITY", 1.5)),
    "budget_fit": float(os.environ.get("WEIGHT_BUDGET_FIT", 1.0)),
    "proximity": float(os.environ.get("WEIGHT_PROXIMITY", 1.5)),
}
