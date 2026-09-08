"""
Thin HTTP clients used only to aggregate stats for the admin
dashboard. Each call forwards the admin's own JWT to the target
service's existing admin endpoint -- the Admin Service does not
re-implement user/destination/itinerary management logic, it only
aggregates numbers that already live in those services.
"""
import requests

import config


def _get(url: str, auth_header: str):
    try:
        resp = requests.get(url, headers={"Authorization": auth_header}, timeout=5)
    except requests.RequestException:
        return None
    if resp.status_code != 200:
        return None
    return resp.json().get("data")


class UserStatsClient:
    @staticmethod
    def get_all_users(auth_header: str):
        return _get(f"{config.USER_SERVICE_URL}/api/admin/users", auth_header)


class DestinationStatsClient:
    @staticmethod
    def get_all_destinations(auth_header: str):
        return _get(f"{config.DESTINATION_SERVICE_URL}/api/admin/destinations", auth_header)


class ItineraryStatsClient:
    @staticmethod
    def get_all_itineraries(auth_header: str):
        return _get(f"{config.ITINERARY_SERVICE_URL}/api/admin/itineraries", auth_header)
