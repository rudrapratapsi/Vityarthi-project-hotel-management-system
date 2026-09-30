"""Bill calculation and receipt text."""


def calculate_total(price_per_day, days):
    """Total bill = price per day x number of days."""
    return price_per_day * days


def build_receipt(room, title):
    """Return the receipt as a list of text lines."""
    guest = room.guest
    total = calculate_total(room.price, guest.days)
    line = "-" * 38
    return [
        "=" * 38,
        title.center(38),
        "=" * 38,
        f"Room Number : {room.number}",
        f"Room Type   : {room.room_type}",
        f"Breakfast   : {room.breakfast_label}",
        f"Guest Name  : {guest.name}",
        f"Phone       : {guest.phone}",
        f"Aadhaar     : {guest.aadhaar_masked}",
        f"People      : {guest.people}",
        f"Days        : {guest.days}",
        f"Price/Day   : ₹{room.price}",
        line,
        f"Total Bill  : ₹{total}",
        "=" * 38,
    ]
