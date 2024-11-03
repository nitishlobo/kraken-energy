"""String utilities."""

from datetime import datetime


def coerce_string_to_int(value: str) -> int | None:
    """Return None if string is empty, else coerce to an int."""
    if value == "":
        return None
    return int(value)


def validate_string_to_datetime(value: str) -> str:
    """Validate string can be converted to a datetime.

    Return empty string, if string is empty.
    """
    # Return empty string if value is empty as it is an optional field.
    if value == "":
        return value

    try:
        datetime.strptime(value, "%Y%m%d%H%M%S")  # noqa: DTZ007
    except ValueError as error:
        msg = f"Datetime string must be in the format 'YYYYMMDDHHMMSS' but is instead {value}."
        raise ValueError(msg) from error

    return value
