import os

SERVICE_NAME = "user-service"
PORT = int(os.environ.get("PORT", 5002))
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me")

DATA_DIR = os.environ.get("DATA_DIR", os.path.join(os.path.dirname(__file__), "data"))
PROFILES_FILE = os.path.join(DATA_DIR, "user_profiles.json")

AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://auth-service:5001")
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

# Shared secret for trusted service-to-service calls (never exposed
# through the API Gateway's public routes).
INTERNAL_SERVICE_KEY = os.environ.get("INTERNAL_SERVICE_KEY", "dev-internal-key-change-me")
