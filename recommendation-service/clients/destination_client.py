"""
HTTP client for the Destination Service.
"""
import requests

import config


class DestinationClient:
    @staticmethod
    def search(params: dict):
        try:
            resp = requests.get(
                f"{config.DESTINATION_SERVICE_URL}/api/destinations",
                params=params,
                timeout=5,
            )
        except requests.RequestException:
            return []
        if resp.status_code != 200:
            return []
        return resp.json().get("data", [])
