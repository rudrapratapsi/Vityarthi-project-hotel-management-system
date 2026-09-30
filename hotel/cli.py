"""Command-line menu. All user interaction (input/print) lives here."""
from . import config, validators
from .billing import build_receipt
from .booking_service import BookingService
from .exceptions import BookingError, HotelError, ValidationError
from .room_manager import RoomManager


# ---------- small input helpers ----------

def ask_until_valid(message, checker):
    """Keep asking until checker(text) returns a value without an error."""
    while True:
        try:
            return checker(input(message))
        except ValidationError as error:
            print(f"  {error}")


def ask_number(message, minimum, maximum, label):
    return ask_until_valid(
        message,
        lambda text: validators.check_int_in_range(text, minimum, maximum, label),
    )


def choose_room_type():
    print("\nSelect Room Type")
    print("1. Single")
    print("2. Double")
    print("3. Deluxe")
    while True:
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            return "Single"
        elif choice == "2":
            return "Double"
        elif choice == "3":
            return "Deluxe"
        else:
            print("  Invalid room type. Please enter 1, 2 or 3.")


def choose_breakfast():
    print("\nBreakfast Option")
    print("1. Without Breakfast")
    print("2. With Breakfast")
    while True:
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            return False
        elif choice == "2":
            return True
        else:
            print("  Invalid breakfast option. Please enter 1 or 2.")


# ---------- menu actions ----------

def show_rooms(manager):
    print("\n========== AVAILABLE ROOMS ==========")
    rooms = manager.available_rooms()
    for room in rooms:
        print(
            f"Room {room.number} | {room.room_type} | "
            f"{room.breakfast_label} | ₹{room.price}/day"
        )
    if not rooms:
        print("No rooms are currently available.")


def book_room(manager, service):
    """Guide the user through a booking. Returns True if it succeeded."""
    print("\n========== ROOM BOOKING ==========")
    room_type = choose_room_type()
    breakfast = choose_breakfast()
    people = ask_number(
        "\nHow many people are staying? ",
        config.MIN_PEOPLE, config.MAX_PEOPLE, "Number of people",
    )

    if manager.find_available(room_type, breakfast) is None:
        print("\nSorry, this type of room is not available.")
        return False

    print("\n========== GUEST DETAILS ==========")
    name = ask_until_valid("Enter guest name: ", validators.check_name)
    phone = ask_until_valid("Enter 10-digit phone number: ", validators.check_phone)
    aadhaar = ask_until_valid("Enter 12-digit Aadhaar number: ", validators.check_aadhaar)
    days = ask_number(
        "How many days will you stay? ",
        config.MIN_DAYS, config.MAX_DAYS, "Number of days",
    )

    try:
        room = service.book(room_type, breakfast, people, name, phone, aadhaar, days)
    except HotelError as error:
        print(f"\n{error}")
        return False

    print()
    for line in build_receipt(room, "BOOKING SUCCESSFUL"):
        print(line)
    return True


def checkout(service):
    print("\n========== CHECKOUT ==========")
    try:
        room_no = validators.check_int_in_range(
            input("Enter room number: "), 100, 9999, "Room number"
        )
        receipt = service.checkout(room_no)
    except HotelError as error:
        print(error)
        return
    print()
    for line in receipt:
        print(line)
    print("\nCheckout completed successfully!")


def guest_details(manager):
    print("\n========== CURRENT GUESTS ==========")
    booked = manager.booked_rooms()
    for room in booked:
        guest = room.guest
        print("\n--------------------------------")
        print(f"Room       : {room.number}")
        print(f"Type       : {room.room_type}")
        print(f"Breakfast  : {room.breakfast_label}")
        print(f"Name       : {guest.name}")
        print(f"Phone      : {guest.phone}")
        print(f"Aadhaar    : {guest.aadhaar_masked}")
        print(f"People     : {guest.people}")
        print(f"Days       : {guest.days}")
    if not booked:
        print("No guests are currently staying.")


def ask_book_another(manager, service):
    """After a successful booking, offer to book more rooms."""
    while True:
        answer = input("\nDo you want to book another room? (yes/no): ").lower().strip()
        if answer in ("yes", "y"):
            book_room(manager, service)
        elif answer in ("no", "n"):
            print("\nReturning to main menu...")
            break
        else:
            print("Please enter yes or no.")


# ---------- main menu ----------

def run(storage):
    """Show the main menu until the user chooses Exit."""
    manager = RoomManager(storage.load())
    service = BookingService(manager, storage)

    while True:
        print("\n======================================")
        print("       HOTEL MANAGEMENT SYSTEM")
        print("======================================")
        print("1. Show Available Rooms")
        print("2. Book Room")
        print("3. Checkout")
        print("4. Guest Details")
        print("5. Exit")
        print("======================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_rooms(manager)
        elif choice == "2":
            if book_room(manager, service):
                ask_book_another(manager, service)
        elif choice == "3":
            checkout(service)
        elif choice == "4":
            guest_details(manager)
        elif choice == "5":
            print("\nThank you for using the Hotel Management System!")
            break
        else:
            print("Invalid choice. Please try again.")
