"""
Recommendation Service.

Generates personalised destination recommendations from preferences,
popularity, rating, budget, opening hours and distance. Talks to the
User Service and Destination Service over HTTP -- it owns no data of
its own.
"""
from clients.destination_client import DestinationClient
from clients.user_client import UserClient
from common.responses import error, success
from services.engine.engine import RecommendationEngine

import config


class RecommendationService:
    engine = RecommendationEngine(weights=config.WEIGHTS)

    @staticmethod
    def get_recommendations(auth_header: str, limit: int = 5, lat: str = None, lng: str = None):
        profile = UserClient.get_my_preferences(auth_header)
        if profile is None:
            return error("could not resolve user profile", 502)

        preferences = profile.get("preferences", [])

        search_params = {}
        if lat and lng:
            search_params["lat"] = lat
            search_params["lng"] = lng

        destinations = DestinationClient.search(search_params)
        if not destinations:
            return success(data=[], message="Recommendations retrieved successfully", status=200)

        context = {"preferences": preferences, "max_budget": None}
        ranked = RecommendationService.engine.rank(destinations, context, limit=limit)

        return success(data=ranked, message="Recommendations retrieved successfully", status=200)
