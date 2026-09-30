"""Data models: Guest and Room."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Guest:
    """A guest staying in a room. Only the masked Aadhaar is kept."""
    name: str
    phone: str
    aadhaar_masked: str
    people: int
    days: int

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "aadhaar_masked": self.aadhaar_masked,
            "people": self.people,
            "days": self.days,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            phone=data["phone"],
            aadhaar_masked=data["aadhaar_masked"],
            people=int(data["people"]),
            days=int(data["days"]),
        )


@dataclass
class Room:
    """A hotel room and (optionally) the guest staying in it."""
    number: int
    room_type: str
    breakfast: bool
    price: int
    status: str = "Available"
    guest: Optional[Guest] = None

    @property
    def breakfast_label(self):
        return "With Breakfast" if self.breakfast else "Without Breakfast"

    def is_available(self):
        return self.status == "Available"

    def to_dict(self):
        return {
            "number": self.number,
            "room_type": self.room_type,
            "breakfast": self.breakfast,
            "price": self.price,
            "status": self.status,
            "guest": self.guest.to_dict() if self.guest else None,
        }

    @classmethod
    def from_dict(cls, data):
        guest_data = data.get("guest")
        return cls(
            number=int(data["number"]),
            room_type=data["room_type"],
            breakfast=bool(data["breakfast"]),
            price=int(data["price"]),
            status=data["status"],
            guest=Guest.from_dict(guest_data) if guest_data else None,
        )
