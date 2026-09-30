"""Custom exceptions so every layer can report problems in a consistent way."""


class HotelError(Exception):
    """Base class for all errors raised by this application."""


class ValidationError(HotelError):
    """Raised when user input does not meet the rules."""


class BookingError(HotelError):
    """Raised when a booking or checkout cannot be completed."""
