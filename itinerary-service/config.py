import os
from pathlib import Path
from dotenv import load_dotenv

# Root directory of the microservices project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the root .env file
load_dotenv(BASE_DIR / ".env")


SERVICE_NAME = "itinerary-service"
PORT = int(os.environ.get("PORT", 5005))
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me")

DATA_DIR = os.environ.get(
    "DATA_DIR",
    os.path.join(os.path.dirname(__file__), "data")
)

ITINERARIES_FILE = os.path.join(DATA_DIR, "itineraries.json")

DESTINATION_SERVICE_URL = os.environ.get(
    "DESTINATION_SERVICE_URL",
    "http://destination-service:5003"
)

CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")


# Mapbox Directions API
MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_ACCESS_TOKEN", "")


TRANSPORT_PROFILES = {
    "walking": {
        "speed_kmh": 5.0,
        "base_fare": 0,
        "price_per_km": 0
    },
    "moto": {
        "speed_kmh": 25.0,
        "base_fare": 200,
        "price_per_km": 150
    },
    "taxi": {
        "speed_kmh": 30.0,
        "base_fare": 300,
        "price_per_km": 250
    },
}