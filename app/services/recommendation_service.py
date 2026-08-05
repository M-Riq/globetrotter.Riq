"""
Recommendation Service

Contains all business logic related to recommendations.
"""

from app.repositories.user_repository import UserRepository
from app.repositories.destination_repository import DestinationRepository
from app.utils.responses import success
from app.utils.responses import error


class RecommendationService:

    user_repository = UserRepository()
    destination_repository = DestinationRepository()

    @staticmethod
    def get_recommendations(username, limit=5):

        user = RecommendationService.user_repository.get_by_username(
            username
        )

        if not user:
            return error(
                "user not found",
                404,
            )

        preferences = [
            preference.lower()
            for preference in user.get(
                "preferences",
                [],
            )
        ]

        destinations = (
            RecommendationService
            .destination_repository
            .get_all()
        )

        scored = []

        for destination in destinations:

            tags = [
                tag.lower()
                for tag in destination.get(
                    "tags",
                    [],
                )
            ]

            score = sum(
                1
                for preference in preferences
                if preference in tags
            )

            scored.append(
                (
                    score,
                    destination,
                )
            )

        scored.sort(
            key=lambda item: (
                -item[0],
                item[1].get("name", ""),
            )
        )

        results = []

        for score, destination in scored[:limit]:

            item = dict(destination)

            item["match_score"] = score

            results.append(item)

        return success(
            data=results,
            message="Recommendations retrieved successfully",
            status=200,
        )