"""
Transport estimation for a given origin -> destination pair.

The estimator compares the GlobeTrotter transport modes:
- walking
- moto
- taxi

Mapbox is used only once, when available, to obtain the real road
distance. If Mapbox is unavailable or fails, the estimator falls
back to the straight-line Haversine distance.

Important:
This module estimates transport options.
It does NOT generate the main navigation route.
"""

import config

from services.maps.fallback_generator import haversine_km
from services.maps.mapbox_client import MapboxClient


# ============================================================
# COORDINATE NORMALIZATION
# ============================================================

def _extract_coordinates(point):
    """
    Normalize supported coordinate representations.

    Supported inputs:

        (latitude, longitude)

    or:

        {
            "lat": latitude,
            "lng": longitude
        }

    or:

        {
            "latitude": latitude,
            "longitude": longitude
        }

    Returns:
        (latitude, longitude)
    """

    if isinstance(point, dict):

        lat = point.get(
            "lat",
            point.get("latitude")
        )

        lng = point.get(
            "lng",
            point.get("longitude")
        )

        if lat is None or lng is None:
            raise ValueError(
                "Invalid coordinate object."
            )

        return (
            float(lat),
            float(lng),
        )

    if isinstance(point, (list, tuple)) and len(point) >= 2:

        return (
            float(point[0]),
            float(point[1]),
        )

    raise ValueError(
        "Invalid coordinate format."
    )


# ============================================================
# ROAD DISTANCE
# ============================================================

def _get_distance_km(origin, destination):
    """
    Get the distance used by the transport estimator.

    Priority:
        1. Mapbox road distance
        2. Haversine straight-line distance

    Mapbox is called only once.
    """

    origin_coords = _extract_coordinates(origin)
    destination_coords = _extract_coordinates(destination)

    # --------------------------------------------------------
    # Try Mapbox
    # --------------------------------------------------------

    if MapboxClient.is_available():

        try:

            route = MapboxClient.directions(
                origin_coords,
                destination_coords,
                mode="driving",
            )

            if route:

                distance_km = route.get(
                    "distance_km"
                )

                if distance_km is not None:

                    return round(
                        float(distance_km),
                        2,
                    )

        except Exception as exc:

            print(
                f"[TransportEstimator] "
                f"Mapbox distance error: {exc}"
            )

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    distance_km = haversine_km(
        origin_coords,
        destination_coords,
    )

    return round(
        distance_km,
        2,
    )


# ============================================================
# TRANSPORT COMPARISON
# ============================================================

def compare_transport_options(
    origin,
    destination,
) -> list:
    """
    Compare walking, moto and taxi.

    The distance is shared between all transport options.

    Mapbox provides the road distance when available.
    Local transport profiles provide estimated duration
    and price.
    """

    distance_km = _get_distance_km(
        origin,
        destination,
    )

    options = []

    for mode, profile in config.TRANSPORT_PROFILES.items():

        speed_kmh = profile.get(
            "speed_kmh"
        )

        base_fare = profile.get(
            "base_fare",
            0,
        )

        price_per_km = profile.get(
            "price_per_km",
            0,
        )

        # ----------------------------------------------------
        # Duration
        # ----------------------------------------------------

        if speed_kmh:

            duration_min = round(
                (distance_km / speed_kmh) * 60,
                1,
            )

        else:

            duration_min = None

        # ----------------------------------------------------
        # Estimated price
        # ----------------------------------------------------

        price = round(
            base_fare
            + price_per_km * distance_km
        )

        options.append({
            "mode": mode,

            "distance_km": distance_km,

            "duration_min": duration_min,

            "estimated_price_fcfa": price,
        })

    return options