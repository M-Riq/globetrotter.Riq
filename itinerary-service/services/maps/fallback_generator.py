"""
Textual itinerary generator used whenever Google Maps is unavailable
(no API key configured, or a live call failed) -- the "MODE SANS
GOOGLE MAPS" required by the spec. Produces a step-by-step walkthrough
derived from straight-line distance and the locally configured
transport profiles.
"""
import math

import config


def haversine_km(origin, destination) -> float:
    lat1, lon1 = math.radians(origin[0]), math.radians(origin[1])
    lat2, lon2 = math.radians(destination[0]), math.radians(destination[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(a))


def generate_textual_itinerary(origin, destination, destination_name: str, mode: str = "walking") -> dict:
    distance_km = haversine_km(origin, destination)
    distance_m = round(distance_km * 1000)
    profile = config.TRANSPORT_PROFILES.get(mode, config.TRANSPORT_PROFILES["walking"])
    duration_min = round((distance_km / profile["speed_kmh"]) * 60, 1) if profile["speed_kmh"] else None

    steps = ["Départ"]
    if mode == "walking":
        remaining = distance_m
        chunk = 300
        first = True
        while remaining > 0:
            step_m = min(chunk, remaining)
            steps.append(f"Marchez {step_m} mètres")
            remaining -= step_m
            if remaining > 0:
                steps.append("Continuez tout droit")
            first = False
    elif mode == "moto":
        steps.append(f"Prenez une moto-taxi ({distance_km:.1f} km)")
    else:  # taxi
        steps.append(f"Prenez un taxi ({distance_km:.1f} km)")
    steps.append(f"Destination atteinte : {destination_name}")

    return {
        "distance_km": round(distance_km, 2),
        "duration_min": duration_min,
        "polyline": None,

        "geometry": None,

        "steps": steps,

        "start_location": {
            "latitude": origin[0],
            "longitude": origin[1],
        },

        "end_location": {
            "latitude": destination[0],
            "longitude": destination[1],
        },

        "source": "fallback_textual",
    }
