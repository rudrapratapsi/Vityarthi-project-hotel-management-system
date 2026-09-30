import unittest

from hotel import validators
from hotel.exceptions import ValidationError


class ValidatorTests(unittest.TestCase):
    def test_valid_aadhaar(self):
        self.assertTrue(validators.validate_aadhaar("123456789012"))

    def test_invalid_aadhaar_length_and_letters(self):
        self.assertFalse(validators.validate_aadhaar("12345"))
        self.assertFalse(validators.validate_aadhaar("12345678901a"))

    def test_mask_aadhaar_keeps_last_four(self):
        self.assertEqual(validators.mask_aadhaar("123456789012"), "XXXX-XXXX-9012")

    def test_phone_rules(self):
        self.assertEqual(validators.check_phone(" 9876543210 "), "9876543210")
        with self.assertRaises(ValidationError):
            validators.check_phone("12345")

    def test_name_rules(self):
        self.assertEqual(validators.check_name("  Rahul Sharma "), "Rahul Sharma")
        with self.assertRaises(ValidationError):
            validators.check_name("   ")
        with self.assertRaises(ValidationError):
            validators.check_name("R@hul123")

    def test_int_in_range(self):
        self.assertEqual(validators.check_int_in_range("3", 1, 3, "People"), 3)
        for bad in ("0", "4", "abc", ""):
            with self.assertRaises(ValidationError):
                validators.check_int_in_range(bad, 1, 3, "People")


if __name__ == "__main__":
    unittest.main()
