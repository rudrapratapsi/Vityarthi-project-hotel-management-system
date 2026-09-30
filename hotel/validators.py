"""Input validation helpers. Each check_* function raises ValidationError on bad input."""
from . import config
from .exceptions import ValidationError


def validate_aadhaar(aadhaar):
    """Return True if the Aadhaar is exactly 12 digits."""
    return len(aadhaar) == config.AADHAAR_LENGTH and aadhaar.isdigit()


def mask_aadhaar(aadhaar):
    """Hide everything except the last 4 digits."""
    return "XXXX-XXXX-" + aadhaar[-4:]


def check_aadhaar(aadhaar):
    aadhaar = aadhaar.strip()
    if not validate_aadhaar(aadhaar):
        raise ValidationError(
            f"Aadhaar must be exactly {config.AADHAAR_LENGTH} digits."
        )
    return aadhaar


def check_phone(phone):
    phone = phone.strip()
    if len(phone) != config.PHONE_LENGTH or not phone.isdigit():
        raise ValidationError(
            f"Phone number must be exactly {config.PHONE_LENGTH} digits."
        )
    return phone


def check_name(name):
    name = name.strip()
    if not name:
        raise ValidationError("Name cannot be empty.")
    if not all(ch.isalpha() or ch in " .'-" for ch in name):
        raise ValidationError("Name can contain only letters and spaces.")
    return name


def check_int_in_range(value, minimum, maximum, label):
    """Convert value to int and make sure minimum <= value <= maximum."""
    try:
        number = int(str(value).strip())
    except ValueError:
        raise ValidationError(f"{label} must be a whole number.")
    if number < minimum or number > maximum:
        raise ValidationError(
            f"{label} must be between {minimum} and {maximum}."
        )
    return number
