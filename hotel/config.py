"""Central configuration and constants for the Hotel Management System."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "hotel_data.json"
LOG_FILE = BASE_DIR / "logs" / "hotel.log"

MIN_PEOPLE = 1
MAX_PEOPLE = 3
MIN_DAYS = 1
MAX_DAYS = 30
AADHAAR_LENGTH = 12
PHONE_LENGTH = 10

ROOM_TYPES = ("Single", "Double", "Deluxe")

# (room number, type, breakfast included, price per day in rupees)
DEFAULT_ROOMS = [
    (101, "Single", False, 1500),
    (102, "Single", True, 1800),
    (103, "Double", False, 2500),
    (104, "Double", True, 3000),
    (105, "Deluxe", False, 4000),
    (106, "Deluxe", True, 4500),
]
