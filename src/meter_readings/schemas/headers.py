"""Header schemas for flow files."""

import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from meter_readings.utils.datetime_ import parse_datetime


class ZHVHeader(BaseModel):
    """ZHV/ZHF header details.

    For more information refer to page 8:
    https://assets.elexon.co.uk/wp-content/uploads/2012/02/28171532/p116_req_spec.pdf
    """

    header_format: Literal["ZHV", "ZHF"]
    file_identifier: str = Field(max_length=10)
    data_flow_and_version_number: str = Field(max_length=8)
    from_market_participant_role_code: str = Field(max_length=1)
    from_market_participant_id: str = Field(max_length=4)
    to_market_participant_role_code: str = Field(max_length=1)
    to_market_participant_id: str = Field(max_length=4)
    file_created_at: str = Field(max_length=14)
    sending_application_id: str | None = Field(default="", max_length=5)
    receiving_application_id: str | None = Field(default="", max_length=5)
    broadcast: str | None = Field(default="", max_length=1)
    test_data_flag: str | None = Field(default="", max_length=4)

    @field_validator("file_created_at")
    def validate_file_created_at(cls, value: str) -> str:
        """Validate that file_created_at is the correct format: YYYYMMDDHHMMSS."""
        try:
            datetime.strptime(value, "%Y%m%d%H%M%S")  # noqa: DTZ007
        except ValueError as error:
            msg = f"file_created_at must be in the format 'YYYYMMDDHHMMSS' but is instead {value}."
            raise ValueError(msg) from error

        return value

    @field_validator("data_flow_and_version_number")
    def validate_data_flow_and_version_number(cls, value: str) -> str:
        """Validate the data flow and the version number."""
        # Validate data flow reference and version number
        data_flow_pattern = r"^D\w{4}\d{3}$"

        if not re.match(data_flow_pattern, value):
            msg = f"Invalid data flow format: {value}"
            raise ValueError(msg)

        return value

    @property
    def file_created_at_datetime(self) -> datetime | None:
        """Return file_created_at as a datetime object."""
        return parse_datetime(self.file_created_at)

    @property
    def data_flow(self) -> str:
        """Return the data flow part of data_flow_and_version_number."""
        return self.data_flow_and_version_number[:5]

    @property
    def data_flow_version(self) -> int:
        """Return the version number part of data_flow_and_version_number as an integer."""
        return int(self.data_flow_and_version_number[5:])
