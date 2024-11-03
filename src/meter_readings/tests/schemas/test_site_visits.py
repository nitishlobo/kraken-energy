"""Test site visits schema."""

import pytest

from meter_readings.schemas.site_visits import J0024_VALID_SET, SiteVisit


@pytest.mark.parametrize("site_visit_reason", J0024_VALID_SET.keys())
def test_valid_site_visit_reason(site_visit_reason: str) -> None:
    """Test valid site visit reason with all J0024_VALID_SET values."""
    site_visit = SiteVisit(
        code="027",
        visit_reason=site_visit_reason,
        additional_information="Example additional information",
    )
    assert site_visit.visit_reason == site_visit_reason


def test_invalid_site_visit_reason() -> None:
    """Test invalid site visit reason."""
    with pytest.raises(ValueError, match="Invalid site visit reason; must be one of"):
        SiteVisit(
            code="027",
            visit_reason="99",
            additional_information="Invalid reason code.",
        )
