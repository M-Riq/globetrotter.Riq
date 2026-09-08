import os

SERVICE_NAME = "destination-service"
PORT = int(os.environ.get("PORT", 5003))
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me")

DATA_DIR = os.environ.get("DATA_DIR", os.path.join(os.path.dirname(__file__), "data"))
DESTINATIONS_FILE = os.path.join(DATA_DIR, "destinations.json")

CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

CATEGORIES = [
    "restaurants", "shopping", "vie_nocturne", "tourisme", "hotels",
    "services_administratifs", "sante", "culture", "loisirs", "sports", "transport",
]
