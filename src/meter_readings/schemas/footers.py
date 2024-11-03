"""Footer schemas for flow files."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from meter_readings.utils.datetimes import parse_datetime
from meter_readings.utils.strings import coerce_string_to_int, validate_string_to_datetime


class ZPTFooter(BaseModel):
    """ZPT footer details.

    For more information refer to page 8:
    https://assets.elexon.co.uk/wp-content/uploads/2012/02/28171532/p116_req_spec.pdf
    """

    footer_format: Literal["ZPT"]
    file_identifier: str = Field(max_length=10)
    total_group_count: int
    checksum: int | None = Field(default=None)
    flow_count: int | None = Field(default=None)
    file_completed_at: str = Field(default="", max_length=14)

    # Validators
    coerce_checksum = field_validator("checksum", mode="before")(coerce_string_to_int)
    validate_file_completed_at = field_validator("file_completed_at")(validate_string_to_datetime)

    @property
    def file_completed_at_datetime(self) -> datetime | None:
        """Return file_completed_at as a datetime object."""
        return parse_datetime(self.file_completed_at)
