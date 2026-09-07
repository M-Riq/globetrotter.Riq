import os

SERVICE_NAME = "api-gateway"
PORT = int(os.environ.get("PORT", 5000))
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

# Routing table: public path prefix -> upstream service base URL.
# Longest prefix wins, so more specific admin routes are listed
# before their more general counterparts where two services could
# otherwise both match the same top-level prefix.
SERVICE_ROUTES = {
    "/api/auth": os.environ.get("AUTH_SERVICE_URL", "http://auth-service:5001"),
    "/api/admin/users": os.environ.get("USER_SERVICE_URL", "http://user-service:5002"),
    "/api/admin/destinations": os.environ.get("DESTINATION_SERVICE_URL", "http://destination-service:5003"),
    "/api/admin/itineraries": os.environ.get("ITINERARY_SERVICE_URL", "http://itinerary-service:5005"),
    "/api/admin": os.environ.get("ADMIN_SERVICE_URL", "http://admin-service:5006"),
    "/api/users": os.environ.get("USER_SERVICE_URL", "http://user-service:5002"),
    "/api/destinations": os.environ.get("DESTINATION_SERVICE_URL", "http://destination-service:5003"),
    "/api/recommendations": os.environ.get("RECOMMENDATION_SERVICE_URL", "http://recommendation-service:5004"),
    "/api/itineraries": os.environ.get("ITINERARY_SERVICE_URL", "http://itinerary-service:5005"),
}

# Ordered longest-prefix-first so /api/admin/destinations is matched
# before the more general /api/admin.
ORDERED_PREFIXES = sorted(SERVICE_ROUTES.keys(), key=len, reverse=True)

HEALTH_ENDPOINTS = {
    "auth-service": os.environ.get("AUTH_SERVICE_URL", "http://auth-service:5001"),
    "user-service": os.environ.get("USER_SERVICE_URL", "http://user-service:5002"),
    "destination-service": os.environ.get("DESTINATION_SERVICE_URL", "http://destination-service:5003"),
    "recommendation-service": os.environ.get("RECOMMENDATION_SERVICE_URL", "http://recommendation-service:5004"),
    "itinerary-service": os.environ.get("ITINERARY_SERVICE_URL", "http://itinerary-service:5005"),
    "admin-service": os.environ.get("ADMIN_SERVICE_URL", "http://admin-service:5006"),
}
