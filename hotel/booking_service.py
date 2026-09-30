"""Business logic for booking a room and checking a guest out."""
import logging

from . import billing, config, validators
from .exceptions import BookingError
from .models import Guest

logger = logging.getLogger(__name__)


class BookingService:
    """Coordinates the room manager, validators and storage."""

    def __init__(self, manager, storage):
        self.manager = manager
        self.storage = storage

    def book(self, room_type, breakfast, people, name, phone, aadhaar, days):
        """Book the first matching free room and return it."""
        if room_type not in config.ROOM_TYPES:
            raise BookingError("Invalid room type.")
        people = validators.check_int_in_range(
            people, config.MIN_PEOPLE, config.MAX_PEOPLE, "Number of people"
        )
        days = validators.check_int_in_range(
            days, config.MIN_DAYS, config.MAX_DAYS, "Number of days"
        )
        name = validators.check_name(name)
        phone = validators.check_phone(phone)
        aadhaar = validators.check_aadhaar(aadhaar)

        room = self.manager.find_available(room_type, breakfast)
        if room is None:
            logger.warning("No %s room available (breakfast=%s)", room_type, breakfast)
            raise BookingError("Sorry, this type of room is not available.")

        room.guest = Guest(
            name=name,
            phone=phone,
            aadhaar_masked=validators.mask_aadhaar(aadhaar),
            people=people,
            days=days,
        )
        room.status = "Booked"
        self.storage.save(self.manager.rooms)
        logger.info("Room %d booked for %s (%d days)", room.number, name, days)
        return room

    def checkout(self, room_number):
        """Free the room and return the receipt lines."""
        room = self.manager.get(room_number)
        if room.is_available():
            raise BookingError("This room is not currently booked.")
        receipt = billing.build_receipt(room, "FINAL BILL")
        guest_name = room.guest.name
        room.guest = None
        room.status = "Available"
        self.storage.save(self.manager.rooms)
        logger.info("Room %d checked out (%s)", room_number, guest_name)
        return receipt
