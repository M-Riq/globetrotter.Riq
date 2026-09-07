"""
Destination Service.

Owns everything about the places GlobeTrotter knows about in
Yaoundé. Public search/filter for visitors, full CRUD for admins.
"""
import math
import uuid

from common.exceptions import ValidationException
from common.responses import error, success
from repositories.destination_repository import DestinationRepository
from validators.destination_validators import validate_destination_data


class DestinationService:
    repository = DestinationRepository()

    # ---- user-facing: search / filter / consult ----
    @staticmethod
    def search(params) -> tuple:
        q = (params.get("q") or "").strip().lower()
        category = (params.get("category") or "").strip().lower()
        tag = (params.get("tag") or "").strip().lower()
        max_budget_str = (params.get("max_budget") or "").strip()
        min_rating_str = (params.get("min_rating") or "").strip()
        lat_str = (params.get("lat") or "").strip()
        lng_str = (params.get("lng") or "").strip()

        max_budget = None
        if max_budget_str:
            try:
                max_budget = float(max_budget_str)
            except ValueError:
                return error("max_budget must be a number", 400)

        min_rating = None
        if min_rating_str:
            try:
                min_rating = float(min_rating_str)
            except ValueError:
                return error("min_rating must be a number", 400)

        origin = None
        if lat_str and lng_str:
            try:
                origin = (float(lat_str), float(lng_str))
            except ValueError:
                return error("lat/lng must be numbers", 400)

        destinations = DestinationService.repository.get_all()
        results = []
        for destination in destinations:
            if q:
                searchable = " ".join([
                    destination.get("name", ""),
                    destination.get("description", ""),
                ]).lower()
                if q not in searchable:
                    continue
            if category and category != destination.get("category", "").lower():
                continue
            if tag:
                tags = [t.lower() for t in destination.get("tags", [])]
                if tag not in tags:
                    continue
            if max_budget is not None:
                budget = destination.get("budget_estimate")
                if budget is not None and budget > max_budget:
                    continue
            if min_rating is not None:
                if (destination.get("rating") or 0) < min_rating:
                    continue

            item = dict(destination)
            if origin:
                item["distance_km"] = DestinationService._haversine_km(
                    origin, (destination.get("latitude"), destination.get("longitude"))
                )
            results.append(item)

        if origin:
            results.sort(key=lambda d: d.get("distance_km", math.inf))

        return success(data=results, message="Destinations retrieved successfully", status=200)

    @staticmethod
    def get_by_id(destination_id: str):
        destination = DestinationService.repository.get_by_id(destination_id)
        if not destination:
            return error("destination not found", 404)
        return success(data=destination, message="Destination retrieved successfully", status=200)

    @staticmethod
    def _haversine_km(origin, point):
        if point[0] is None or point[1] is None:
            return None
        lat1, lon1 = math.radians(origin[0]), math.radians(origin[1])
        lat2, lon2 = math.radians(point[0]), math.radians(point[1])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return round(6371 * 2 * math.asin(math.sqrt(a)), 2)

    # ---- admin-facing: create / update / delete / list ----
    @staticmethod
    def admin_list():
        return success(
            data=DestinationService.repository.get_all(),
            message="Destinations retrieved successfully",
            status=200,
        )

    @staticmethod
    def create(data: dict):
        try:
            validate_destination_data(data)
        except ValidationException as exc:
            return error(exc.message, 400)

        destination = {
            "id": f"dest-{uuid.uuid4().hex[:8]}",
            "name": data["name"].strip(),
            "description": data["description"].strip(),
            "category": data["category"],
            "latitude": float(data["latitude"]),
            "longitude": float(data["longitude"]),
            "images": data.get("images", []),
            "opening_hours": data.get("opening_hours", ""),
            "budget_estimate": data.get("budget_estimate", 0),
            "contact": data.get("contact", ""),
            "rating": data.get("rating", 0),
            "tags": data.get("tags", []),
            "popularity": data.get("popularity", 0),
            "carthier": data.get("carthier"),
            "video_url": data.get("video_url", "")
        }
        DestinationService.repository.save(destination)
        return success(data=destination, message="Destination created successfully", status=201)

    @staticmethod
    def update(destination_id: str, data: dict):
        try:
            validate_destination_data(data, partial=True)
        except ValidationException as exc:
            return error(exc.message, 400)

        if not DestinationService.repository.get_by_id(destination_id):
            return error("destination not found", 404)

        updated = DestinationService.repository.update(destination_id, data)
        return success(data=updated, message="Destination updated successfully", status=200)

    @staticmethod
    def delete(destination_id: str):
        deleted = DestinationService.repository.delete(destination_id)
        if not deleted:
            return error("destination not found", 404)
        return success(message="Destination deleted successfully", status=200)
