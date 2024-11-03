"""Schemas related to MPAN cores."""

from typing import Literal

from pydantic import BaseModel, Field


class MPANCore(BaseModel):
    """MPAN cores schema.

    Key attributes:
        code -- 026 encoding for MPAN cores.
        mpan_core -- unique national reference for a Metering System or an Asset Metering System (J0003).
        bsc_validation_status -- indicates whether readings or
                                Half Hourly advances have been validated, passed or failed BSC Validation.
                                F = Failed, U = Not validated, V = Validated.
    """

    code: Literal["026"]
    mpan_core: str = Field(max_length=13)
    bsc_validation_status: Literal["F", "U", "V"]
