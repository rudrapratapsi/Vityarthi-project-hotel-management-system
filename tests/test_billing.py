import unittest

from hotel import billing
from hotel.models import Guest, Room


class BillingTests(unittest.TestCase):
    def test_total_is_price_times_days(self):
        self.assertEqual(billing.calculate_total(3000, 3), 9000)

    def test_receipt_contains_total_and_masked_aadhaar(self):
        room = Room(104, "Double", True, 3000, "Booked",
                    Guest("Rahul", "9876543210", "XXXX-XXXX-9012", 2, 3))
        text = "\n".join(billing.build_receipt(room, "FINAL BILL"))
        self.assertIn("9000", text)
        self.assertIn("XXXX-XXXX-9012", text)


if __name__ == "__main__":
    unittest.main()
