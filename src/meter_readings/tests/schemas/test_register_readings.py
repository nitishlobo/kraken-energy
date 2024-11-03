"""Test register reading schema."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from meter_readings.schemas.register_readings import RegisterReading


def test_valid_register_reading() -> None:
    """Test a valid register reading schema."""
    register_reading = RegisterReading(
        code="030",
        meter_register_id="01",
        reading_at="20231101000000",
        # String format to test conversion to float
        register_reading="12345.67",  # type: ignore[reportArgumentType]
        md_reset_at="20231001000000",
        # String format to test conversion to int
        number_of_md_resets="10",
        meter_reading_flag="T",
        reading_method="N",
    )
    assert register_reading.code == "030"
    assert register_reading.meter_register_id == "01"
    assert register_reading.register_reading == 12345.67
    assert register_reading.number_of_md_resets == 10
    assert register_reading.meter_reading_flag == "T"
    assert register_reading.reading_method == "N"
    assert isinstance(register_reading.reading_at_datetime, datetime)
    assert register_reading.reading_at_datetime == datetime(2023, 11, 1, 0, 0, tzinfo=timezone.utc)


def test_invalid_reading_at_format() -> None:
    """Test invalid date format for reading_at."""
    with pytest.raises(
        ValidationError,
        match="Datetime string must be in the format 'YYYYMMDDHHMMSS' but is instead 20231101.",
    ):
        RegisterReading(
            code="030",
            meter_register_id="01",
            # Incorrect format, should be 14 characters
            reading_at="20231101",
            register_reading="12345.67",  # type: ignore[reportArgumentType]
            md_reset_at="20231001000000",
            number_of_md_resets="10",
            meter_reading_flag="T",
            reading_method="N",
        )


def test_invalid_register_reading_value() -> None:
    """Test invalid register reading value."""
    with pytest.raises(ValueError, match="could not convert string to float"):
        RegisterReading(
            code="030",
            meter_register_id="01",
            reading_at="20231101000000",
            # Not a valid float
            register_reading="invalid_float",  # type: ignore[reportArgumentType]
            md_reset_at="20231001000000",
            number_of_md_resets="10",
            meter_reading_flag="T",
            reading_method="N",
        )


def test_invalid_number_of_md_resets() -> None:
    """Test invalid number of MD resets."""
    with pytest.raises(ValidationError, match="1 validation error for RegisterReading\nnumber_of_md_resets"):
        RegisterReading(
            code="030",
            meter_register_id="01",
            reading_at="20231101000000",
            register_reading="12345.67",  # type: ignore[reportArgumentType]
            md_reset_at="20231001000000",
            # Maximum limit is 999
            number_of_md_resets="1000",
            meter_reading_flag="T",
            reading_method="N",
        )


def test_invalid_meter_reading_flag() -> None:
    """Test invalid meter reading flag."""
    with pytest.raises(ValidationError, match="1 validation error for RegisterReading\nmeter_reading_flag"):
        RegisterReading(
            code="030",
            meter_register_id="01",
            reading_at="20231101000000",
            register_reading="12345.67",  # type: ignore[reportArgumentType]
            md_reset_at="20231001000000",
            number_of_md_resets="10",
            # Invalid flag
            meter_reading_flag="X",  # type: ignore[reportArgumentType]
            reading_method="N",
        )


def test_invalid_reading_method() -> None:
    """Test invalid reading method."""
    with pytest.raises(ValidationError, match="1 validation error for RegisterReading\nreading_method"):
        RegisterReading(
            code="030",
            meter_register_id="01",
            reading_at="20231101000000",
            register_reading="12345.67",  # type: ignore[reportArgumentType]
            md_reset_at="20231001000000",
            number_of_md_resets="10",
            meter_reading_flag="T",
            # Invalid reading method
            reading_method="X",  # type: ignore[reportArgumentType]
        )
