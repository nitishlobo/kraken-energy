"""Schemas for meter reading validation results."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

METER_READING_REASON_CODES = {
    "01": "MSID Incorrect",
    "02": "Reading Dates",
    "03": "Negative Consumption",
    "04": "Inconsistent with slave register advance",
    "05": "Consumption exceeds twice expected advance",
    "06": "Meter incorrectly energised",
    "07": "Meter incorrectly de-energised",
    "08": "Full Scale MD",
    "09": "Zero MD",
    "10": "Number of MD resets >1",
    "11": "Number of register digits incorrect",
    "12": "Inconsistent register read date",
    "13": "Faulty Meter",
    "14": "Hand Held Read Failure",
    "15": "Meter Not on Site/Metering protocol not approved",
    "16": "Standing Data incorrect",
    "17": "No access to meter",
    "18": "Meter Time/Date reset",
    "19": "Outstation reset",
    "20": "Meter Change/Meter Maintenance",
    "21": "Phase Failure",
    "22": "Meters Recording Zeros",
    "23": "Test Data Recorded",
    "24": "Data Lapse",
    "25": "Actual Data Manually Keyed",
    "26": "Invalid Zero Advances",
    "27": "Zero Consumption",
}


class MeterReadingValidationResult(BaseModel):
    """Meter reading validation result schema.

    Key attributes:
        code -- 032 encoding for meter reading.
        reason -- code indicating the reason why meter reading data has failed validation.
                    A Reason Code exists for each validation failure type.
                    If the Meter Reading Flag is set to False then Meter Reading Reason Code
                    is set to one of a pre-determined set of codes.
        meter_reading_status -- indicates whether register reading is valid or suspect.
                            If meter readings are flagged as suspectthey are checked.
                            T = Valid, F = Suspect
    """

    code: Literal["032"]
    reason: str = Field(max_length=2)
    status: Literal["T", "F"]

    @field_validator("reason")
    def validate_reason(cls, value: str) -> str:
        """Validate meter reading reason code."""
        if value not in METER_READING_REASON_CODES:
            msg = f"Invalid site visit reason; must be one of {list(METER_READING_REASON_CODES.keys())}"
            raise ValueError(msg)
        return value
