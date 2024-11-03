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
                        # Get list of header fields in the order they are defined in the model
                        zhv_header_fields = list(ZHVHeader.model_fields.keys())
                        # Match header fields with values
                        zhv_header_data = dict(zip(zhv_header_fields, row, strict=False))
                        # Parse and validate data
                        zhv_header = ZHVHeader.model_validate(zhv_header_data)

                    if row[0] == "ZPT":
                        footer_present = True
                        # Get list of header fields in the order they are defined in the model
                        zpt_footer_fields = list(ZPTFooter.model_fields.keys())
                        # Match header fields with values
                        zpt_footer_data = dict(zip(zpt_footer_fields, row, strict=False))
                        # Parse and validate data
                        zpt_footer = ZPTFooter.model_validate(zpt_footer_data)

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
