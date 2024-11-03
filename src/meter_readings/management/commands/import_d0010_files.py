"""Import data from D0010 flow files and record it into the database."""

import csv
from pathlib import Path
from typing import Any

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandParser
from pydantic import ValidationError as PydanticValidationError

from meter_readings.models.flow_files import FlowFile, FlowFileMetadata
from meter_readings.schemas.footers import ZPTFooter
from meter_readings.schemas.headers import ZHVHeader
from meter_readings.schemas.meter_reading_types import MeterReadingType
from meter_readings.schemas.meter_reading_validation_results import MeterReadingValidationResult
from meter_readings.schemas.mpan_cores import MPANCore
from meter_readings.schemas.register_readings import RegisterReading
from meter_readings.schemas.site_visits import SiteVisit


def parse_zhv_header(row: list[str]) -> ZHVHeader:
    """Parse and validate ZHV header data."""
    # Get list of header fields in the order they are defined in the model
    zhv_header_fields = list(ZHVHeader.model_fields.keys())
    # Match header fields with values
    zhv_header_data = dict(zip(zhv_header_fields, row, strict=False))
    # Parse and validate data
    return ZHVHeader.model_validate(zhv_header_data)


def parse_mpan_core(row: list[str]) -> MPANCore:
    """Parse and validate MPAN core data."""
    mpan_core_fields = list(MPANCore.model_fields.keys())
    mpan_core_data = dict(zip(mpan_core_fields, row, strict=False))
    return MPANCore.model_validate(mpan_core_data)


def parse_site_visit(row: list[str]) -> SiteVisit:
    """Parse and validate site visit data."""
    site_visit_fields = list(SiteVisit.model_fields.keys())
    site_visit_data = dict(zip(site_visit_fields, row, strict=False))
    return SiteVisit.model_validate(site_visit_data)


def parse_meter_reading_type(row: list[str]) -> MeterReadingType:
    """Parse and validate meter reading type data."""
    meter_reading_type_fields = list(MeterReadingType.model_fields.keys())
    meter_reading_type_data = dict(zip(meter_reading_type_fields, row, strict=False))
    return MeterReadingType.model_validate(meter_reading_type_data)


def parse_register_reading(row: list[str]) -> RegisterReading:
    """Parse and validate register reading data."""
    register_reading_fields = list(RegisterReading.model_fields.keys())
    register_reading_data = dict(zip(register_reading_fields, row, strict=False))
    return RegisterReading.model_validate(register_reading_data)


def parse_meter_reading_validation_result(row: list[str]) -> MeterReadingValidationResult:
    """Parse and validate meter reading validation result data."""
    meter_reading_validation_result_fields = list(MeterReadingValidationResult.model_fields.keys())
    meter_reading_validation_result_data = dict(zip(meter_reading_validation_result_fields, row, strict=False))
    return MeterReadingValidationResult.model_validate(meter_reading_validation_result_data)


def parse_zpt_footer(row: list[str]) -> ZPTFooter:
    """Parse and validate ZPT footer data."""
    zpt_footer_fields = list(ZPTFooter.model_fields.keys())
    zpt_footer_data = dict(zip(zpt_footer_fields, row, strict=False))
    return ZPTFooter.model_validate(zpt_footer_data)


class Command(BaseCommand):
    """Import data from D0010 flow files into database."""

    help = "Import data from D0010 files."

    def add_arguments(self, parser: CommandParser) -> None:
        """Arguments for importing D0010 file command."""
        parser.add_argument("file_path", type=str, help="Path to the D0010 file")

    def handle(self, *args: Any, **kwargs: dict[str, Any]) -> None:  # noqa: ANN401
        """Import, process and record data read from D0010 flow files."""
        file_path = Path(kwargs["file_path"])  # type: ignore[arg-type]

        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"No valid file or directory found at {file_path}"))
            return

        # File path is a directory
        if file_path.is_dir():
            # Iterate through all files in directory
            for file in file_path.iterdir():
                # Only import files, not any subdirectories
                if file.is_file():
                    self.import_file(file)
        # File path is a single file
        elif file_path.is_file():
            self.import_file(file_path)

    def import_file(self, file_path: Path) -> None:
        """Import data from a single D0010 file."""
        self.stdout.write(f"Processing file: {file_path}")

        error_found = False
        header_present = False
        footer_present = False
        with file_path.open(mode="r") as file:
            reader = csv.reader(file, delimiter="|")
            for row in reader:
                try:
                    # Process file header
                    if row[0] == "ZHV" or row[0] == "ZHF":
                        header_present = True
                        zhv_header = parse_zhv_header(row)

                    # Process MPAN core data
                    if row[0] == "026":
                        entry = {}
                        mpan_core = parse_mpan_core(row)
                        entry["mpan_core"] = mpan_core

                    # Process site visit data for MPAN core
                    if row[0] == "027":
                        mpan_site_visit = parse_site_visit(row)
                        entry["mpan_site_visit"] = mpan_site_visit

                    # Process meter reading data
                    if row[0] == "028":
                        meter_reading_types = parse_meter_reading_type(row)
                        entry["meter_reading_types"] = meter_reading_types

                    # Process site visit data for meter readings
                    if row[0] == "029":
                        meter_reading_site_visit = parse_site_visit(row)
                        entry["meter_reading_site_visit"] = meter_reading_site_visit

                    # Process register reading data
                    if row[0] == "030":
                        register_reading = parse_register_reading(row)
                        entry["register_reading"] = register_reading

                    # Process meter reading validation result data
                    if row[0] == "032":
                        meter_reading_validation_result = parse_meter_reading_validation_result(row)
                        entry["meter_reading_validation_result"] = meter_reading_validation_result

                    # Process site visit data for register readings
                    if row[0] == "033":
                        register_reading_site_visit = parse_site_visit(row)
                        entry["register_reading_site_visit"] = register_reading_site_visit

                    # Process file footer
                    if row[0] == "ZPT":
                        footer_present = True
                        zpt_footer = parse_zpt_footer(row)

                        # Exit reading file as we have read the footer
                        # Assumption: any data after file footer is either a blank line or invalid data
                        break

                except (IndexError, ValueError, ValidationError, PydanticValidationError) as e:
                    error_found = True
                    self.stdout.write(self.style.ERROR(f"Error processing row: {row} - {e}"))

        if error_found:
            self.stdout.write(self.style.ERROR(f"No data from this file will be written to the database: {file_path}."))
            return

        # Only write data to database if no errors have been found
        flow_file = FlowFile.objects.create(name=file_path.stem, extension=file_path.suffix)

        # Save metadata (from header and footer) to database
        if header_present and footer_present:
            FlowFileMetadata.objects.create(
                flow_file=flow_file,
                header_format=zhv_header.header_format,
                footer_format=zpt_footer.footer_format,
                file_identifier=zpt_footer.file_identifier,
                data_flow=zhv_header.data_flow,
                data_flow_version=zhv_header.data_flow_version,
                from_market_participant_role_code=zhv_header.from_market_participant_role_code,
                from_market_participant_id=zhv_header.from_market_participant_id,
                to_market_participant_role_code=zhv_header.to_market_participant_role_code,
                to_market_participant_id=zhv_header.to_market_participant_id,
                sending_application_id=zhv_header.sending_application_id,
                receiving_application_id=zhv_header.receiving_application_id,
                broadcast=zhv_header.broadcast,
                test_data_flag=zhv_header.test_data_flag,
                total_group_count=zpt_footer.total_group_count,
                footer_checksum=zpt_footer.checksum,
                flow_count=zpt_footer.flow_count,
                file_created_at=zhv_header.file_created_at_datetime,
                file_completed_at=zpt_footer.file_completed_at_datetime,
            )

        self.stdout.write(self.style.SUCCESS(f"Data imported successfully from {file_path}"))
