"""Test file for header schemas for flow files."""

import pytest

from meter_readings.schemas.headers import ZHVHeader


def test_validate_file_created_at_correct_format() -> None:
    """Test ZHV header with valid file_created_at."""
    header = ZHVHeader(
        header_format="ZHV",
        file_identifier="0000475656",
        data_flow_and_version_number="D0010002",
        from_market_participant_role_code="A",
        from_market_participant_id="1234",
        to_market_participant_role_code="B",
        to_market_participant_id="5678",
        file_created_at="20240101123456",
    )
    assert header.file_created_at == "20240101123456"


def test_validate_file_created_at_incorrect_format() -> None:
    """Test ZHV header with invalid file_created_at."""
    with pytest.raises(
        ValueError,
        match="String should have at most 14 characters",
    ):
        ZHVHeader(
            header_format="ZHV",
            file_identifier="0000475656",
            data_flow_and_version_number="D0010002",
            from_market_participant_role_code="A",
            from_market_participant_id="1234",
            to_market_participant_role_code="B",
            to_market_participant_id="5678",
            file_created_at="2024-01-01 12:34:56",
        )


def test_validate_data_flow_and_version_number_correct_format() -> None:
    """Test ZHV header with valid data flow and version number."""
    header = ZHVHeader(
        header_format="ZHV",
        file_identifier="0000475656",
        data_flow_and_version_number="D0010002",
        from_market_participant_role_code="A",
        from_market_participant_id="1234",
        to_market_participant_role_code="B",
        to_market_participant_id="5678",
        file_created_at="20230101123045",
    )
    assert header.data_flow_and_version_number == "D0010002"


def test_validate_data_flow_and_version_number_incorrect_format() -> None:
    """Test ZHV header with invalid data flow and version number."""
    with pytest.raises(ValueError, match="Invalid data flow format: D1234"):
        ZHVHeader(
            header_format="ZHV",
            file_identifier="0000475656",
            data_flow_and_version_number="D1234",
            from_market_participant_role_code="A",
            from_market_participant_id="1234",
            to_market_participant_role_code="B",
            to_market_participant_id="5678",
            file_created_at="20230101123045",
        )
