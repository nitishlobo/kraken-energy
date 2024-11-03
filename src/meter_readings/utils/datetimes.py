"""Datetime utility functions."""

from datetime import datetime, timezone

from django.utils.timezone import make_aware


def parse_datetime(value: str | None) -> datetime | None:
    """Convert a YYYYMMDDHHMMSS string to a datetime object."""
    if value:
        naive_datetime = datetime.strptime(value, "%Y%m%d%H%M%S")  # noqa: DTZ007
        return make_aware(naive_datetime, timezone.utc)
    return None
