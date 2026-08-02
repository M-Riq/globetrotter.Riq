"""
Application configuration.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")

DESTINATIONS_FILE = os.path.join(DATA_DIR, "destinations.json")

ITINERARIES_FILE = os.path.join(DATA_DIR, "itineraries.json")

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "globetrotter-secret-change-in-prod",
)

PORT = int(
    os.environ.get("PORT", 5000)
)