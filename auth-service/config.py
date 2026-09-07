import os

SERVICE_NAME = "auth-service"
PORT = int(os.environ.get("PORT", 5001))
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me")

DATA_DIR = os.environ.get("DATA_DIR", os.path.join(os.path.dirname(__file__), "data"))
USERS_FILE = os.path.join(DATA_DIR, "users.json")

# Single, constant admin account for now (per spec: "credentials de mail
# et password constant et unique pour l'instant"). Move to a proper
# admin table/service once real admin onboarding is needed.
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@globetrotter.cm")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ChangeMe123!")

CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

USER_SERVICE_URL = os.environ.get("USER_SERVICE_URL", "http://user-service:5002")
INTERNAL_SERVICE_KEY = os.environ.get("INTERNAL_SERVICE_KEY", "dev-internal-key-change-me")
