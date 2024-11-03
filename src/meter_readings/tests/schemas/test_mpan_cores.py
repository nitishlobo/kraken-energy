"""Test MPAN cores schema."""

import pytest
from pydantic import ValidationError

from meter_readings.schemas.mpan_cores import MPANCore


@pytest.mark.parametrize("bsc_validation_status", ["F", "U", "V"])
def test_valid_mpan_core(bsc_validation_status: str) -> None:
    """Test valid MPAN core."""
    mpan = MPANCore(
        code="026",
        mpan_core="1200023305967",
        bsc_validation_status=bsc_validation_status,
    )
    assert mpan.code == "026"
    assert mpan.mpan_core == "1200023305967"
    assert mpan.bsc_validation_status == bsc_validation_status


def test_invalid_mpan_core_length() -> None:
    """Test invalid MPAN core length."""
    with pytest.raises(ValidationError):
        MPANCore(
            code="026",
            mpan_core="12345678901234",  # 14 characters instead of 13
            bsc_validation_status="V",
        )


def test_invalid_bsc_validation_status() -> None:
    """Test invalid BSC validation status."""
    with pytest.raises(ValidationError):
        MPANCore(
            code="026",
            mpan_core="1200023305967",
            # Invalid status
            bsc_validation_status="X",
        )
