"""
Destination Repository.
"""
from common.base_repository import BaseRepository
from common.storage.json_storage import JSONStorage

import config


class DestinationRepository(BaseRepository):
    def __init__(self):
        super().__init__(JSONStorage(config.DESTINATIONS_FILE))
