"""
HTTP client for the Destination Service.
"""
import requests

import config


class DestinationClient:
    @staticmethod
    def get_by_id(destination_id: str):
        try:
            resp = requests.get(
                f"{config.DESTINATION_SERVICE_URL}/api/destinations/{destination_id}",
                timeout=5,
            )
        except requests.RequestException:
            return None
        if resp.status_code != 200:
            return None
        return resp.json().get("data")
