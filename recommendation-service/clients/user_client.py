"""
HTTP client for the User Service.
"""
import requests

import config


class UserClient:
    @staticmethod
    def get_my_preferences(auth_header: str):
        """Forwards the caller's own JWT to the User Service -- the
        Recommendation Service never needs its own credentials to read
        a user's preferences, it just relays the request's identity."""
        try:
            resp = requests.get(
                f"{config.USER_SERVICE_URL}/api/users/me",
                headers={"Authorization": auth_header},
                timeout=5,
            )
        except requests.RequestException:
            return None
        if resp.status_code != 200:
            return None
        return resp.json().get("data")
