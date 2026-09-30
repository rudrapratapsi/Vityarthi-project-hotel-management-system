"""JSON file storage so that data survives after the program closes."""
import json
import logging
import os
import tempfile
from pathlib import Path

from . import config
from .models import Room

logger = logging.getLogger(__name__)


def default_rooms():
    """Build the starting set of rooms from the configuration."""
    return {
        number: Room(number, room_type, breakfast, price)
        for number, room_type, breakfast, price in config.DEFAULT_ROOMS
    }


class JsonStorage:
    """Load and save the room dictionary as a JSON file."""

    def __init__(self, path=None):
        self.path = Path(path) if path else config.DATA_FILE

    def load(self):
        """Return {room_number: Room}. Falls back to defaults if needed."""
        if not self.path.exists():
            logger.info("No data file found. Starting with default rooms.")
            return default_rooms()
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            rooms = {}
            for item in raw["rooms"]:
                room = Room.from_dict(item)
                rooms[room.number] = room
            logger.info("Loaded %d rooms from %s", len(rooms), self.path)
            return rooms
        except (OSError, ValueError, KeyError, TypeError) as error:
            logger.error("Could not read data file (%s). Using defaults.", error)
            return default_rooms()

    def save(self, rooms):
        """Write all rooms to disk safely (temp file, then replace)."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"rooms": [r.to_dict() for r in rooms.values()]}
        fd, temp_name = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            os.replace(temp_name, self.path)
            logger.debug("Saved %d rooms to %s", len(rooms), self.path)
        except OSError:
            logger.exception("Failed to save data")
            if os.path.exists(temp_name):
                os.remove(temp_name)
            raise
