"""
Itinerary Repository
"""

from app.config import ITINERARIES_FILE
from app.repositories.base_repository import BaseRepository


class ItineraryRepository(BaseRepository):

    def __init__(self):
        super().__init__(ITINERARIES_FILE)

    def get_by_username(self, username):

        itineraries = self.get_all()

        return [
            itinerary
            for itinerary in itineraries
            if itinerary["username"] == username
        ]

    def save(self, itinerary):

        self.append(itinerary)