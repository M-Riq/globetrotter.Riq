"""
Itinerary Service

Contains all business logic related to itineraries.
"""

import uuid
import datetime

from app.repositories.itinerary_repository import ItineraryRepository
from app.utils.responses import success
from app.utils.responses import error


class ItineraryService:

    repository = ItineraryRepository()

    @staticmethod
    def create(username: str, data: dict):

        title = data.get("title", "").strip()
        destinations = data.get("destinations", [])

        if not title:
            return error(
                "title is required",
                400,
            )

        if not isinstance(destinations, list):
            return error(
                "destinations must be a list",
                400,
            )

        itinerary = {
            "id": str(uuid.uuid4()),
            "username": username,
            "title": title,
            "destinations": destinations,
            "start_date": data.get("start_date", ""),
            "end_date": data.get("end_date", ""),
            "notes": data.get("notes", ""),
            "created_at": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat(),
        }

        ItineraryService.repository.save(
            itinerary
        )

        return success(
            data=itinerary,
            message="Itinerary created successfully",
            status=201,
        )

    @staticmethod
    def get_all(username: str):

        itineraries = (
            ItineraryService
            .repository
            .get_by_username(username)
        )

        return success(
            data=itineraries,
            message="Itineraries retrieved successfully",
            status=200,
        )