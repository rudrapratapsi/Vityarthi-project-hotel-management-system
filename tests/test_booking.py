import tempfile
import unittest
from pathlib import Path

from hotel.booking_service import BookingService
from hotel.exceptions import BookingError, ValidationError
from hotel.room_manager import RoomManager
from hotel.storage import JsonStorage


def make_service(folder):
    storage = JsonStorage(Path(folder) / "data.json")
    manager = RoomManager(storage.load())
    return BookingService(manager, storage), manager, storage


GOOD = dict(people=2, name="Rahul Sharma", phone="9876543210",
            aadhaar="123456789012", days=3)


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.service, self.manager, self.storage = make_service(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_successful_booking_marks_room_booked(self):
        room = self.service.book("Double", True, **GOOD)
        self.assertEqual(room.number, 104)
        self.assertFalse(room.is_available())
        self.assertEqual(room.guest.aadhaar_masked, "XXXX-XXXX-9012")

    def test_full_aadhaar_is_never_saved(self):
        self.service.book("Single", False, **GOOD)
        saved = self.storage.path.read_text(encoding="utf-8")
        self.assertNotIn("123456789012", saved)

    def test_too_many_people_rejected(self):
        with self.assertRaises(ValidationError):
            self.service.book("Single", False, **{**GOOD, "people": 4})

    def test_too_many_days_rejected(self):
        with self.assertRaises(ValidationError):
            self.service.book("Single", False, **{**GOOD, "days": 31})

    def test_bad_aadhaar_rejected(self):
        with self.assertRaises(ValidationError):
            self.service.book("Single", False, **{**GOOD, "aadhaar": "123"})

    def test_no_room_left_raises_booking_error(self):
        self.service.book("Deluxe", True, **GOOD)
        with self.assertRaises(BookingError):
            self.service.book("Deluxe", True, **GOOD)

    def test_checkout_frees_room_and_returns_receipt(self):
        room = self.service.book("Single", False, **GOOD)
        receipt = self.service.checkout(room.number)
        self.assertIn("Total Bill  : ₹4500", receipt)
        self.assertTrue(room.is_available())
        self.assertIsNone(room.guest)

    def test_checkout_errors(self):
        with self.assertRaises(BookingError):
            self.service.checkout(101)      # not booked
        with self.assertRaises(BookingError):
            self.service.checkout(999)      # does not exist

    def test_data_survives_restart(self):
        self.service.book("Double", False, **GOOD)
        _, manager2, _ = make_service(self.tmp.name)
        self.assertEqual(len(manager2.booked_rooms()), 1)
        self.assertEqual(manager2.booked_rooms()[0].guest.name, "Rahul Sharma")

    def test_corrupt_file_falls_back_to_defaults(self):
        self.storage.path.write_text("{ not valid json", encoding="utf-8")
        rooms = JsonStorage(self.storage.path).load()
        self.assertEqual(len(rooms), 6)


if __name__ == "__main__":
    unittest.main()
