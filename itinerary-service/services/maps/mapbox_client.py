"""
Mapbox integration for directions, geocoding and nearby search.

This is the single point of contact with Mapbox APIs.
Every method returns None on failure so callers can
transparently fall back to fallback_generator.py.
"""

import requests
import config


MAPBOX_BASE_URL = "https://api.mapbox.com"


class MapboxClient:

    @staticmethod
    def is_available() -> bool:
        return bool(config.MAPBOX_ACCESS_TOKEN)

    @staticmethod
    def _token():
        return config.MAPBOX_ACCESS_TOKEN

    @staticmethod
    def directions(origin, destination, mode: str = "walking"):
        """
        Calculate a route between origin and destination using
        Mapbox Directions API.

        Coordinates are expected as:
            (latitude, longitude)

        Supported modes:
            walking
            driving
            cycling
        """

        print(
        "[Mapbox] token configured:",
        bool(config.MAPBOX_ACCESS_TOKEN),
        )

        if not MapboxClient.is_available():
            print("[Mapbox] API unavailable: token missing")
            return None

        try:
            # ---------------------------------------------------------
            # Origin
            # ---------------------------------------------------------

            if isinstance(origin, dict):
                origin_lat = float(
                    origin.get(
                        "lat",
                        origin.get("latitude"),
                    )
                )

                origin_lng = float(
                    origin.get(
                        "lng",
                        origin.get("longitude"),
                    )
                )

            else:
                origin_lat = float(origin[0])
                origin_lng = float(origin[1])

            # ---------------------------------------------------------
            # Destination
            # ---------------------------------------------------------

            if isinstance(destination, dict):
                destination_lat = float(
                    destination.get(
                        "lat",
                        destination.get("latitude"),
                    )
                )

                destination_lng = float(
                    destination.get(
                        "lng",
                        destination.get("longitude"),
                    )
                )

            else:
                destination_lat = float(destination[0])
                destination_lng = float(destination[1])

            # ---------------------------------------------------------
            # Mapbox profile
            # ---------------------------------------------------------

            profile = {
                "walking": "walking",
                "driving": "driving",
                "cycling": "cycling",
            }.get(mode, "walking")

            # ---------------------------------------------------------
            # Mapbox coordinates MUST be:
            #
            # longitude,latitude
            # ---------------------------------------------------------

            coordinates = (
                f"{origin_lng},{origin_lat};"
                f"{destination_lng},{destination_lat}"
            )

            url = (
                f"{MAPBOX_BASE_URL}/directions/v5/mapbox/"
                f"{profile}/{coordinates}"
            )

            params = {
                "access_token": MapboxClient._token(),
                "steps": "true",
                "geometries": "geojson",
                "overview": "full",
                "language": "fr",
            }

            print("[Mapbox] profile:", profile)
            print("[Mapbox] coordinates:", coordinates)

            # ---------------------------------------------------------
            # API request
            # ---------------------------------------------------------

            response = requests.get(
                url,
                params=params,
                timeout=20,
            )

            print(
                "[Mapbox] status:",
                response.status_code,
            )

            response.raise_for_status()

            # ---------------------------------------------------------
            # Parse JSON
            # ---------------------------------------------------------

            data = response.json()

            print(
                "[Mapbox] code:",
                data.get("code"),
            )

            if data.get("code") != "Ok":
                print(
                    "[Mapbox] Directions API returned:",
                    data.get("code"),
                    data.get("message"),
                )

                return None

            # ---------------------------------------------------------
            # Routes
            # ---------------------------------------------------------

            routes = data.get("routes", [])

            if not routes:
                print(
                    "[Mapbox] No route returned."
                )

                return None

            route = routes[0]

            # ---------------------------------------------------------
            # Geometry
            # ---------------------------------------------------------

            geometry = route.get("geometry")

            print(
                "[Mapbox] geometry available:",
                bool(geometry),
            )

            if geometry:
                print(
                    "[Mapbox] geometry type:",
                    geometry.get("type"),
                )

                print(
                    "[Mapbox] geometry points:",
                    len(
                        geometry.get(
                            "coordinates",
                            [],
                        )
                    ),
                )

            # ---------------------------------------------------------
            # Distance / duration
            # ---------------------------------------------------------

            print(
                "[Mapbox] distance:",
                route.get("distance"),
            )

            print(
                "[Mapbox] duration:",
                route.get("duration"),
            )

            # ---------------------------------------------------------
            # Navigation instructions
            # ---------------------------------------------------------

            steps = []

            for leg in route.get("legs", []):
                for step in leg.get("steps", []):

                    instruction = (
                        step
                        .get("maneuver", {})
                        .get("instruction")
                    )

                    if instruction:
                        steps.append(instruction)

            # ---------------------------------------------------------
            # Final route
            # ---------------------------------------------------------

            return {
                "distance_km": round(
                    route["distance"] / 1000,
                    2,
                ),

                "duration_min": round(
                    route["duration"] / 60,
                    1,
                ),

                "polyline": None,

                "geometry": geometry,

                "steps": steps,

                "start_location": {
                    "latitude": origin_lat,
                    "longitude": origin_lng,
                },

                "end_location": {
                    "latitude": destination_lat,
                    "longitude": destination_lng,
                },

                "source": "mapbox",
            }

        except requests.exceptions.Timeout:
            print(
                "[Mapbox] Directions request timed out."
            )
            return None

        except requests.exceptions.RequestException as exc:
            print(
                "[Mapbox] Directions HTTP error:",
                exc,
            )
            return None

        except Exception as exc:
            print(
                "[Mapbox] Directions error:",
                exc,
            )
            return None

    @staticmethod
    def geocode(address: str):

        if not MapboxClient.is_available():
            return None

        try:
            url = (
                f"{MAPBOX_BASE_URL}/search/geocode/v6/forward"
            )

            params = {
                "q": address,
                "access_token": MapboxClient._token(),
                "limit": 1,
                "language": "fr",
            }

            response = requests.get(
                url,
                params=params,
                timeout=10,
            )

            response.raise_for_status()

            data = response.json()

            features = data.get("features", [])

            if not features:
                return None

            feature = features[0]

            coordinates = (
                feature
                .get("geometry", {})
                .get("coordinates", [])
            )

            if len(coordinates) < 2:
                return None

            longitude = coordinates[0]
            latitude = coordinates[1]

            return {
                "latitude": latitude,
                "longitude": longitude,
                "formatted_address": feature.get(
                    "properties", {}
                ).get(
                    "full_address"
                ) or feature.get("place_name", address),
            }

        except Exception as exc:
            print(f"[Mapbox] Geocoding error: {exc}")
            return None

    @staticmethod
    def nearby_places(
        lat: float,
        lng: float,
        keyword: str = None,
        radius: int = 2000,
    ):

        # À implémenter seulement si ton application
        # utilise réellement la recherche de lieux.
        return None