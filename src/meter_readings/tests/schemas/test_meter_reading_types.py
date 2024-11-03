"""Test meter reading types schema."""

import pytest

from meter_readings.schemas.meter_reading_types import READING_TYPES, MeterReadingType


@pytest.mark.parametrize("reading_type_code", READING_TYPES.keys())
def test_valid_meter_reading_type(reading_type_code: str) -> None:
    """Test valid reading types with all READING_TYPES values."""
    meter_reading = MeterReadingType(
        code="028",
        meter_id="1234567890",
        reading_type=reading_type_code,
    )
    assert meter_reading.reading_type == reading_type_code


def test_invalid_meter_reading_type_when_type_is_too_long() -> None:
    """Test invalid meter reading type when type is too long."""
    with pytest.raises(ValueError, match="1 validation error for MeterReadingType\nreading_type"):
        MeterReadingType(
            code="028",
            meter_id="1234567890",
            # Reading type code exceeds max. length of 1.
            reading_type="Z1",
        )


def test_invalid_meter_reading_type_when_type_is_wrong() -> None:
    """Test invalid meter reading type when type is wrong."""
    with pytest.raises(ValueError, match="1 validation error for MeterReadingType\nreading_type"):
        MeterReadingType(
            code="028",
            meter_id="1234567890",
            # Reading type code does not exist in READING_TYPES.
            reading_type="E",
        )
