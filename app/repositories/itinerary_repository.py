import os

from app.data.json_storage import (
    read_json,
    write_json,
)
from app.config import ITINERARIES_FILE

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# ITINERARIES_FILE = os.path.join(
#     BASE_DIR,
#     "data",
#     "itineraries.json",
# )


class ItineraryRepository:

    @staticmethod
    def get_all():

        return read_json(
            ITINERARIES_FILE
        )

    @staticmethod
    def get_by_user(username):

        itineraries = ItineraryRepository.get_all()

        return [
            itinerary
            for itinerary in itineraries
            if itinerary["username"] == username
        ]

    @staticmethod
    def save(itinerary):

        itineraries = ItineraryRepository.get_all()

        itineraries.append(itinerary)

        write_json(
            ITINERARIES_FILE,
            itineraries,
        )