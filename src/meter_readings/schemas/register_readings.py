"""Schemas related to register readings."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, conint, field_validator

from meter_readings.utils.datetimes import parse_datetime
from meter_readings.utils.strings import coerce_string_to_int, validate_string_to_datetime


class RegisterReading(BaseModel):
    """Register reading schema.

    Key attributes:
        code -- 030 encoding for register reading.
        meter_register_id -- reference Id for a Meter Register within a meter (J0010).
        reading_at -- date and time at which a meter register reading was taken.
                        The time is always midnight for Non-Half Hourly readings with the exception ofspecial
                        reads where the absolute reading time must be given (J0016).
        register_reading -- value of a reading from a meter register at a specified date and time (J0040).
        md_reset_at -- date and time at which a Maximum Demand Meter is reset to zero (J0044).
        number_of_md_resets -- number of times that the Maximum Demand Indicator has been reset (J1013).
        meter_reading_flag -- indicates whether register reading is valid or suspect (J0045).
                                T = Valid, F = Suspect.
        reading_method -- indicates how the meter reading was obtained (J1888).
                            N = Not viewed by an Agent or Non Site Visit, P = Viewed by an Agent or Site Visit.
    """

    code: Literal["030"]
    meter_register_id: str = Field(max_length=2)
    reading_at: str = Field(max_length=14)
    register_reading: float
    md_reset_at: str = Field(default="", max_length=14)
    number_of_md_resets: conint(lt=999) | None = Field(default=None)  # type: ignore[reportInvalidTypeForm]
    meter_reading_flag: Literal["T", "F", ""] = Field(default="")
    reading_method: Literal["N", "P"]

    # Validators
    validate_reading_at = field_validator("reading_at")(validate_string_to_datetime)
    coerce_number_of_md_resets = field_validator("number_of_md_resets", mode="before")(coerce_string_to_int)

    @field_validator("register_reading", mode="before")
    def coerce_register_reading(cls, value: str) -> float:
        """Convert register reading to float."""
        return float(value)

    @property
    def reading_at_datetime(self) -> datetime | None:
        """Return reading_at as a datetime object."""
        return parse_datetime(self.reading_at)

    @property
    def md_reset_at_datetime(self) -> datetime | None:
        """Return md_reset_at as a datetime object."""
        return parse_datetime(self.md_reset_at)
