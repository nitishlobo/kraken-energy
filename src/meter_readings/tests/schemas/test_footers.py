"""Tests for footer schemas for flow files."""

from datetime import datetime, timezone

import pytest

from meter_readings.schemas.footers import ZPTFooter


def test_zpt_footer_valid_data() -> None:
    """Test ZPT footer with valid data."""
    footer = ZPTFooter(
        footer_format="ZPT",
        file_identifier="0000475656",
        total_group_count=5,
        # Deliberately using a string, instead of an int for the checksum
        checksum="123",
        flow_count=10,
        file_completed_at="20160302154650",
    )
    # Validate each field
    assert footer.footer_format == "ZPT"
    assert footer.file_identifier == "0000475656"
    assert footer.total_group_count == 5
    assert footer.checksum == 123
    assert footer.flow_count == 10
    assert footer.file_completed_at == "20160302154650"
    assert footer.file_completed_at_datetime == datetime(2016, 3, 2, 15, 46, 50, tzinfo=timezone.utc)


def test_zpt_footer_optional_fields() -> None:
    """Test ZPT footer with optional fields."""
    footer = ZPTFooter(
        footer_format="ZPT",
        file_identifier="0000475656",
        total_group_count=5,
        checksum="",
        flow_count=None,
        file_completed_at="",
    )
    # Optional fields
    assert footer.checksum is None
    assert footer.flow_count is None
    assert footer.file_completed_at == ""
    # Property field from an optional field
    assert footer.file_completed_at_datetime is None


def test_zpt_footer_invalid_file_completed_at() -> None:
    """Test ZPT footer with invalid file_completed_at."""
    with pytest.raises(
        ValueError,
        match="String should have at most 14 characters",
    ):
        ZPTFooter(
            footer_format="ZPT",
            file_identifier="0000475656",
            total_group_count=5,
            checksum="123",
            flow_count=10,
            file_completed_at="2024-01-01 12:34:56",
        )


def test_zpt_footer_invalid_checksum() -> None:
    """Test ZPT footer with invalid checksum."""
    with pytest.raises(ValueError, match="1 validation error for ZPTFooter\nchecksum"):
        ZPTFooter(
            footer_format="ZPT",
            file_identifier="0000475656",
            total_group_count=5,
            checksum="invalid",
            flow_count=10,
            file_completed_at="20160302154650",
        )
