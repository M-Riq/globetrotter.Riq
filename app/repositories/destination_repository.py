import os

from app.data.json_storage import read_json
from app.config import DESTINATIONS_FILE

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# DESTINATIONS_FILE = os.path.join(
#     BASE_DIR,
#     "data",
#     "destinations.json",
# )


class DestinationRepository:

    @staticmethod
    def get_all():

        return read_json(
            DESTINATIONS_FILE
        )