"""
Destination Service

Contains all business logic related to destinations.
"""

from app.repositories.destination_repository import DestinationRepository
from app.utils.responses import success
from app.utils.responses import error


class DestinationService:

    repository = DestinationRepository()

    @staticmethod
    def search(params: dict):

        q = params.get("q", "").strip().lower()
        tag = params.get("tag", "").strip().lower()
        continent = params.get("continent", "").strip().lower()
        max_cost_str = params.get("max_cost", "").strip()

        max_cost = None

        if max_cost_str:
            try:
                max_cost = int(max_cost_str)
            except ValueError:
                return error(
                    "max_cost must be an integer",
                    400,
                )

        destinations = DestinationService.repository.get_all()

        results = []

        for destination in destinations:

            if q:

                searchable = " ".join([
                    destination.get("name", ""),
                    destination.get("country", ""),
                    destination.get("description", ""),
                ]).lower()

                if q not in searchable:
                    continue

            if tag:

                tags = [
                    t.lower()
                    for t in destination.get("tags", [])
                ]

                if tag not in tags:
                    continue

            if continent:

                if continent != destination.get(
                    "continent",
                    "",
                ).lower():
                    continue

            if max_cost is not None:

                cost = destination.get(
                    "avg_cost_per_day"
                )

                if cost is None or cost > max_cost:
                    continue

            results.append(destination)

        return success(
            data=results,
            message="Destinations retrieved successfully",
            status=200,
        )