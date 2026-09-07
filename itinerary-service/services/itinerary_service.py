"""
Itinerary Service -- the main/orchestrating microservice.

The admin never creates itineraries manually (only destinations).
Itineraries are always generated automatically from:
  - the visitor's current position
  - a chosen destination

Uses Mapbox Directions / Matrix when a Mapbox access token is
configured and reachable; otherwise falls back to a generated
textual itinerary.

Also produces a walk/moto/taxi comparison, and persists
"reached" itineraries with impressions/ratings so a visitor
can review + share their trip history via WhatsApp.
"""

import urllib.parse
import uuid
from datetime import datetime, timezone

from clients.destination_client import DestinationClient
from common.exceptions import ValidationException
from common.responses import error, success
from repositories.itinerary_repository import ItineraryRepository
from services.maps.fallback_generator import generate_textual_itinerary
from services.maps.mapbox_client import MapboxClient
from services.maps.transport_estimator import compare_transport_options
from validators.itinerary_validators import (
    validate_generate_request,
    validate_reached_data,
)


class ItineraryService:

    repository = ItineraryRepository()

    # ------------------------------------------------------------------
    # Core route-building logic
    # ------------------------------------------------------------------

    @staticmethod
    def _build_route(
        origin: tuple,
        destination: dict,
        mode: str,
    ) -> dict:

        dest_coords = (
            destination.get("latitude"),
            destination.get("longitude"),
        )

        route = None

        if MapboxClient.is_available():

            route = MapboxClient.directions(
                origin,
                dest_coords,
                mode=mode,
            )

        used_mapbox = route is not None

        if route is None:

            route = generate_textual_itinerary(
                origin,
                dest_coords,
                destination.get("name", ""),
                mode,
            )

        transport_comparison = compare_transport_options(
            origin,
            dest_coords,
        )

        return {
            "route": route,
            "transport_comparison": transport_comparison,
            "mapbox_used": used_mapbox,
        }

    # ------------------------------------------------------------------
    # Generate itinerary preview
    # ------------------------------------------------------------------

    @staticmethod
    def generate(data: dict):

        try:
            validate_generate_request(data)

        except ValidationException as exc:
            return error(
                exc.message,
                400,
            )

        destination = DestinationClient.get_by_id(
            data["destination_id"]
        )

        if not destination:
            return error(
                "destination not found",
                404,
            )

        origin = (
            float(data["origin_lat"]),
            float(data["origin_lng"]),
        )

        mode = data.get(
            "mode",
            "walking",
        )

        built = ItineraryService._build_route(
            origin,
            destination,
            mode,
        )

        return success(
            data={
                "destination": destination,
                "origin": {
                    "latitude": origin[0],
                    "longitude": origin[1],
                },
                **built,
            },
            message="Itinerary generated successfully",
            status=200,
        )

    # ------------------------------------------------------------------
    # Persisted itineraries
    # ------------------------------------------------------------------

    @staticmethod
    def create(
        user_id: str,
        data: dict,
    ):

        try:
            validate_reached_data(data)

        except ValidationException as exc:
            return error(
                exc.message,
                400,
            )

        destination = DestinationClient.get_by_id(
            data["destination_id"]
        )

        if not destination:
            return error(
                "destination not found",
                404,
            )

        route_data = {}

        if (
            data.get("origin_lat") is not None
            and data.get("origin_lng") is not None
        ):

            origin = (
                float(data["origin_lat"]),
                float(data["origin_lng"]),
            )

            route_data = ItineraryService._build_route(
                origin,
                destination,
                data.get("mode", "walking"),
            )

        status = data.get(
            "status",
            "reached",
        )

        now_iso = datetime.now(
            timezone.utc
        ).isoformat()

        itinerary = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "reason": data.get("reason"),
            "destination_id": destination["id"],
            "destination_name": destination.get(
                "name",
                "",
            ),
            "status": status,
            "impression": data.get(
                "impression",
                "",
            ),
            "rating": data.get("rating"),
            "reached_at": (
                data.get("reached_at", now_iso)
                if status == "reached"
                else None
            ),
            "created_at": now_iso,
            **route_data,
        }

        ItineraryService.repository.save(
            itinerary
        )

        return success(
            data=itinerary,
            message="Itinerary saved successfully",
            status=201,
        )

    # ------------------------------------------------------------------
    # User itineraries
    # ------------------------------------------------------------------

    @staticmethod
    def list_for_user(user_id: str):

        itineraries = (
            ItineraryService.repository
            .get_by_user(user_id)
        )

        reached_count = sum(
            1
            for it in itineraries
            if it.get("status") == "reached"
        )

        return success(
            data={
                "count_reached": reached_count,
                "itineraries": itineraries,
            },
            message="Itineraries retrieved successfully",
            status=200,
        )

    # ------------------------------------------------------------------
    # Get itinerary
    # ------------------------------------------------------------------

    @staticmethod
    def get_one(
        user_id: str,
        itinerary_id: str,
    ):

        itinerary = (
            ItineraryService.repository
            .get_by_id(itinerary_id)
        )

        if (
            not itinerary
            or itinerary.get("user_id") != user_id
        ):
            return error(
                "itinerary not found",
                404,
            )

        return success(
            data=itinerary,
            message="Itinerary retrieved successfully",
            status=200,
        )

    # ------------------------------------------------------------------
    # WhatsApp sharing
    # ------------------------------------------------------------------

    @staticmethod
    def share_whatsapp(
        user_id: str,
        itinerary_id: str,
    ):

        itinerary = (
            ItineraryService.repository
            .get_by_id(itinerary_id)
        )

        if (
            not itinerary
            or itinerary.get("user_id") != user_id
        ):
            return error(
                "itinerary not found",
                404,
            )

        route = (
            itinerary.get("route", {})
            or {}
        )

        text_lines = [
            f"J'ai visité "
            f"{itinerary['destination_name']} "
            f"via GlobeTrotter !"
        ]

        if route.get("distance_km") is not None:
            text_lines.append(
                f"Distance : "
                f"{route['distance_km']} km"
            )

        if route.get("duration_min") is not None:
            text_lines.append(
                f"Durée : "
                f"{route['duration_min']} min"
            )

        if itinerary.get("impression"):
            text_lines.append(
                f"Impression : "
                f"{itinerary['impression']}"
            )

        text = "\n".join(text_lines)

        whatsapp_url = (
            "https://wa.me/?text="
            + urllib.parse.quote(text)
        )

        return success(
            data={
                "whatsapp_url": whatsapp_url,
                "shared_text": text,
            },
            message="Share link generated successfully",
            status=200,
        )

    # ------------------------------------------------------------------
    # Admin
    # ------------------------------------------------------------------

    @staticmethod
    def admin_list_all():

        itineraries = (
            ItineraryService.repository
            .get_all()
        )

        reached = [
            it
            for it in itineraries
            if it.get("status") == "reached"
        ]

        return success(
            data={
                "count_total": len(itineraries),
                "count_reached": len(reached),
                "itineraries": itineraries,
            },
            message="Itineraries retrieved successfully",
            status=200,
        )