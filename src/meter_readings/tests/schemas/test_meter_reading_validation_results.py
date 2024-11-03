"""Tests for the MeterReadingValidationResult schema."""

import pytest
from pydantic import ValidationError

from meter_readings.schemas.meter_reading_validation_results import MeterReadingValidationResult


def test_valid_meter_reading():
    """Test that a valid MeterReadingValidationResult instance is created successfully."""
    result = MeterReadingValidationResult(code="032", reason="01", status="T")
    assert result.code == "032"
    assert result.reason == "01"
    assert result.status == "T"


@pytest.mark.parametrize("reason", ["99", "AA", ""])
def test_invalid_reason_code(reason: str) -> None:
    """Test that an invalid reason code raises a ValidationError."""
    with pytest.raises(ValidationError, match="Invalid site visit reason"):
        MeterReadingValidationResult(code="032", reason=reason, status="T")


def test_invalid_status() -> None:
    """Test that an invalid status value raises a ValidationError."""
    with pytest.raises(ValidationError, match="1 validation error for MeterReadingValidationResult\nstatus"):
        MeterReadingValidationResult(code="032", reason="01", status="X")  # type: ignore [reportArgumentType]


def test_invalid_code():
    """Test that an invalid code raises a ValidationError."""
    with pytest.raises(ValidationError, match="1 validation error for MeterReadingValidationResult\ncode"):
        MeterReadingValidationResult(code="999", reason="01", status="T")  # type: ignore [reportArgumentType]
