import os

SERVICE_NAME = "admin-service"
PORT = int(os.environ.get("PORT", 5006))
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me")

USER_SERVICE_URL = os.environ.get("USER_SERVICE_URL", "http://user-service:5002")
DESTINATION_SERVICE_URL = os.environ.get("DESTINATION_SERVICE_URL", "http://destination-service:5003")
ITINERARY_SERVICE_URL = os.environ.get("ITINERARY_SERVICE_URL", "http://itinerary-service:5005")

CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")
