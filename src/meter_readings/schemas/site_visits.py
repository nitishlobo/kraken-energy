"""Schemas related to site visit information."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

J0024_VALID_SET = {
    "01": "Site occupied",
    "02": "Site not occupied",
    "03": "Meter system energised",
    "04": "Meter system de-energised",
    "05": "Equipment/meter damage",
    "06": "Suspected tampering",
    "07": "Timeswitch stopped",
    "08": "Phase/fuse failure",
    "09": "Consumption detected on de-energised meter",
    "10": "Change of meter",
    "11": "Zero reading on MD register",
    "13": "MD register on full scale",
    "14": "More than 1 MD register reset",
    "15": "Meter stopped",
    "16": "Seals damaged",
    "17": "Seals missing",
    "18": "Unsafe premises",
    "19": "Call not made on routine visit",
    "20": "No access",
    "21": "Refused access",
    "22": "Meter blocked",
    "23": "Wiring dangerous or incomplete",
    "24": "Token Meter Reset",
    "25": "Token Meter Not Reset",
    "26": "Agent failed to keep appointment",
    "27": "Meter reading modified manually by NHHDC in accordance with BSCPs -site visit not required.",
    "28": "Unable to gain access due to Insufficient address details",
    "29": "Customer unable to provide access",
    "30": "Unable to gain access to HV environment",
    "31": "Interrogation port unavailable (HH only)",
    "32": "Wrong meter/outstation password (HH only)",
    "33": "Handheld failure (HH only)",
    "34": "Suspected demolished",
    "35": "Demolished",
    "36": "Change of occupier",
    "37": "Unmanned",
    "38": "Unable to gain access due to key/code being unavailable",
    "39": "Unable to locate meter at property",
    "40": "Suspected Energised",
    "41": "Suspected De-energised",
    "42": "Site capable of exporting energy",
    "43": "Supply remotely disabled",
    "44": "Supply remotely re-armed",
    "50": "Category A Network Defect Reported",
    "51": "Category B Network Defect Reported",
    "52": "Additional equipment required",
    "53": "Unable to establish WAN",
    "54": "Unable to establish HAN",
    "55": "Insufficient space for new meter installation",
    "56": "Unable to access due to parking restrictions",
    "57": "Unable to complete installation due to adverse weather conditions",
    "58": "Unable to complete installation due to height/position of meter",
    "88": "Request rejected",
    "89": "Fault resolution completion report",
}


class SiteVisit(BaseModel):
    """Site visit schema for J0024.

    Key attributes:
        code -- 027 encoding for site visits.
        visit_reason -- code identifying either nature of checks made/to be made on metering equipment
                        during a site visit or identifying reason for failure to obtain readings (J0024).
        additional_information -- free format character string for providing additional details (J0012).
    """

    code: Literal["027"]
    visit_reason: str = Field(max_length=2)
    additional_information: str = Field(max_length=200)

    @field_validator("visit_reason")
    def validate_visit_reason(cls, value: str) -> str:
        """Validate site visit reason."""
        if value not in J0024_VALID_SET:
            msg = f"Invalid site visit reason; must be one of {list(J0024_VALID_SET.keys())}"
            raise ValueError(msg)
        return value
