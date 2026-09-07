"""
User (profile) Service.

Business logic for preferences, favorites, and the visited-
destinations history ("les destinations qu'il a atteint, comptabiliser
le nombre de destinations, noter les impressions... la date où il a
atteint ses destinations").
"""
import datetime

from common.exceptions import ValidationException
from common.responses import error, success
from repositories.user_profile_repository import UserProfileRepository
from validators.user_validators import validate_favorite_data, validate_profile_update


class UserService:
    repository = UserProfileRepository()

    @staticmethod
    def _get_or_create(user_id: str, username: str = "", preferences=None):
        profile = UserService.repository.get_by_user_id(user_id)
        if profile:
            return profile
        profile = {
            "user_id": user_id,
            "username": username,
            "preferences": preferences or [],
            "favorites": [],
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        UserService.repository.save(profile)
        return profile

    # -- internal (service-to-service, called by Auth Service on register) --
    @staticmethod
    def init_profile(data: dict):
        user_id = data.get("user_id")
        if not user_id:
            return error("user_id is required", 400)
        profile = UserService._get_or_create(
            user_id, data.get("username", ""), data.get("preferences", [])
        )
        return success(data=profile, message="Profile initialized", status=201)

    # -- user-facing --
    @staticmethod
    def get_profile(current_user: dict):
        profile = UserService._get_or_create(current_user["sub"], current_user.get("username", ""))
        return success(data=profile, message="Profile retrieved successfully", status=200)

    @staticmethod
    def update_profile(current_user: dict, data: dict):
        try:
            validate_profile_update(data)
        except ValidationException as exc:
            return error(exc.message, 400)

        profile = UserService._get_or_create(current_user["sub"], current_user.get("username", ""))
        updates = {}
        if "preferences" in data:
            updates["preferences"] = data["preferences"]
        if updates:
            profile = UserService.repository.upsert({**profile, **updates})
        return success(data=profile, message="Profile updated successfully", status=200)

    @staticmethod
    def list_favorites(current_user: dict):
        profile = UserService._get_or_create(current_user["sub"], current_user.get("username", ""))
        return success(data=profile.get("favorites", []), message="Favorites retrieved successfully", status=200)

    @staticmethod
    def add_favorite(current_user: dict, data: dict):
        try:
            validate_favorite_data(data)
        except ValidationException as exc:
            return error(exc.message, 400)

        profile = UserService._get_or_create(current_user["sub"], current_user.get("username", ""))
        destination_id = data["destination_id"]
        favorites = profile.get("favorites", [])
        if destination_id not in favorites:
            favorites.append(destination_id)
            profile = UserService.repository.upsert({**profile, "favorites": favorites})
        return success(data=profile["favorites"], message="Destination added to favorites", status=201)

    @staticmethod
    def remove_favorite(current_user: dict, destination_id: str):
        profile = UserService._get_or_create(current_user["sub"], current_user.get("username", ""))
        favorites = [d for d in profile.get("favorites", []) if d != destination_id]
        profile = UserService.repository.upsert({**profile, "favorites": favorites})
        return success(data=profile["favorites"], message="Destination removed from favorites", status=200)

    # -- admin --
    @staticmethod
    def list_all_profiles():
        profiles = UserService.repository.get_all()
        return success(data=profiles, message="Users retrieved successfully", status=200)

    @staticmethod
    def get_profile_by_id(user_id: str):
        profile = UserService.repository.get_by_user_id(user_id)
        if not profile:
            return error("user not found", 404)
        return success(data=profile, message="User retrieved successfully", status=200)

    @staticmethod
    def delete_profile(user_id: str):
        deleted = UserService.repository.storage.delete(user_id, id_field="user_id")
        if not deleted:
            return error("user not found", 404)
        return success(message="User deleted successfully", status=200)
