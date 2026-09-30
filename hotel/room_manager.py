"""Room inventory: searching and listing rooms."""
from .exceptions import BookingError


class RoomManager:
    """Holds the rooms and answers questions about them."""

    def __init__(self, rooms):
        self.rooms = rooms

    def get(self, room_number):
        if room_number not in self.rooms:
            raise BookingError("Room does not exist.")
        return self.rooms[room_number]

    def available_rooms(self):
        return [r for r in self.rooms.values() if r.is_available()]

    def booked_rooms(self):
        return [r for r in self.rooms.values() if not r.is_available()]

    def find_available(self, room_type, breakfast):
        """Return the first free room that matches, or None."""
        for room in self.rooms.values():
            if (
                room.room_type == room_type
                and room.breakfast == breakfast
                and room.is_available()
            ):
                return room
        return None
