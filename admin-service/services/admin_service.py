"""
Admin Service.

Provides the admin dashboard: system-wide statistics aggregated from
the other services. Owns no data of its own.
"""
from collections import Counter

from clients.aggregation_clients import DestinationStatsClient, ItineraryStatsClient, UserStatsClient
from common.responses import success


class AdminService:
    @staticmethod
    def dashboard_stats(auth_header: str):
        users = UserStatsClient.get_all_users(auth_header) or []
        destinations = DestinationStatsClient.get_all_destinations(auth_header) or []
        itinerary_data = ItineraryStatsClient.get_all_itineraries(auth_header) or {}

        destinations_by_category = dict(Counter(d.get("category", "unknown") for d in destinations))

        stats = {
            "total_users": len(users),
            "total_destinations": len(destinations),
            "destinations_by_category": destinations_by_category,
            "total_itineraries": itinerary_data.get("count_total", 0),
            "total_destinations_reached": itinerary_data.get("count_reached", 0),
        }
        return success(data=stats, message="Dashboard statistics retrieved successfully", status=200)
