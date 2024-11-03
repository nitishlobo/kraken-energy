"""Truncate all database tables."""

from typing import Any

from django.core.management.base import BaseCommand

from meter_readings.models.flow_files import FlowFile, FlowFileMetadata


class Command(BaseCommand):
    """Truncate all database tables."""

    help = "Truncate all database tables."

    def handle(self, *args: Any, **kwargs: dict[str, Any]) -> None:  # pylint: disable=unused-argument, # noqa: ANN401
        """Truncate all database records."""
        FlowFile.objects.all().delete()
        FlowFileMetadata.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Successfully truncated all tables"))  # pylint: disable=no-member
