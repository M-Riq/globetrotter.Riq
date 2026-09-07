"""
Itinerary Repository.

Stores generated itineraries, whether merely planned or marked as
"reached" (with impression, rating and the date/route used).
"""
from common.base_repository import BaseRepository
from common.storage.json_storage import JSONStorage

import config


class ItineraryRepository(BaseRepository):
    def __init__(self):
        super().__init__(JSONStorage(config.ITINERARIES_FILE))

    def get_by_user(self, user_id: str):
        return [it for it in self.get_all() if it.get("user_id") == user_id]
