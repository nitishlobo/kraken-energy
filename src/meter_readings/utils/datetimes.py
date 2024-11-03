"""Datetime utility functions."""

from datetime import datetime


def parse_datetime(value: str | None) -> datetime | None:
    """Convert a YYYYMMDDHHMMSS string to a datetime object."""
    if value:
        return datetime.strptime(value, "%Y%m%d%H%M%S")  # noqa: DTZ007
    return None
