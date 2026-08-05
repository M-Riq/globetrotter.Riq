"""
Destination Repository
"""

from app.config import DESTINATIONS_FILE
from app.repositories.base_repository import BaseRepository


class DestinationRepository(BaseRepository):

    def __init__(self):
        super().__init__(DESTINATIONS_FILE)