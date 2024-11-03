"""Schemas related to meter reading types."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

READING_TYPES = {
    "A": "Actual Change of Supplier Read",
    "C": "Customer own read",
    "D": "Deemed (Settlement Registers) or Estimated (Non-Settlement Registers)",
    "F": "Final",
    "I": "Initial",
    "M": "MAR",
    "O": "Old Supplier's Estimated CoS Reading",
    "P": "Electronically collected via PPMIP",
    "Q": "Meter Reading modified manually by DC",
    "R": "Routine",
    "S": "Special",
    "T": "Proving Test Reading",
    "U": "Forward Migration CoA",
    "V": "Forward Migration CoS",
    "W": "Withdrawn",
    "X": "Supplier Agreed Switch Read",
    "Y": "Reverse Migration CoS",
    "Z": "Actual Change of Tenancy Read",
}


class MeterReadingType(BaseModel):
    """Meter reading type schema.

    Key attributes:
        code -- 028 encoding for meter reading type.
        meter_id -- serial number stamped onto the meter nameplate at manufacture. Main identifier of a Meter (J0004).
        reading_type -- code identifying the type of reading (J0171).
    """

    code: Literal["028"]
    meter_id: str = Field(max_length=10)
    reading_type: str = Field(max_length=1)

    @field_validator("reading_type")
    def validate_reading_type(cls, value: str) -> str:
        """Validate reading type."""
        if value not in READING_TYPES:
            msg = f"Invalid reading type; must be one of {list(READING_TYPES.keys())}"
            raise ValueError(msg)
        return value
