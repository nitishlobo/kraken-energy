"""Footer schemas for flow files."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from meter_readings.utils.datetime_ import parse_datetime


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
    file_completed_at: str | None = Field(default="", max_length=14)

    @field_validator("checksum", mode="before")
    def validate_checksum(cls, value: str) -> int | None:
        """Coerce empty string to None and validate as int if non-empty."""
        if value == "":
            return None
        return int(value)

    @field_validator("file_completed_at")
    def validate_file_completed_at(cls, value: str) -> str:
        """Validate that file_completed_at is the correct format: YYYYMMDDHHMMSS."""
        # Return empty string if value is empty as it is an optional field.
        if value == "":
            return value

        try:
            datetime.strptime(value, "%Y%m%d%H%M%S")  # noqa: DTZ007
        except ValueError as error:
            msg = f"file_completed_at must be in the format 'YYYYMMDDHHMMSS' but is instead {value}."
            raise ValueError(msg) from error

        return value

    @property
    def file_completed_at_datetime(self) -> datetime | None:
        """Return file_completed_at as a datetime object."""
        return parse_datetime(self.file_completed_at)
