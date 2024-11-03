"""Admin registered models."""

from django.contrib import admin
from django.db.models import Model
from django.http import HttpRequest

from meter_readings.models.flow_files import FlowFile, FlowFileMetadata


class ReadOnlyAdminMixin:
    """Create model as view only."""

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Return False to forbid admin user from adding data."""
        return False

    def has_change_permission(self, request: HttpRequest, obj: Model | None = None) -> bool:
        """Return False to forbid admin user from modifying data."""
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Model | None = None) -> bool:
        """Return False to forbid admin user from deleting data."""
        return False


@admin.register(FlowFile)
class FlowFileAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    """Admin view for FlowFile."""

    list_display = ("name", "extension", "imported_at")
    search_fields = ("name",)
    list_filter = ("extension", "imported_at")


@admin.register(FlowFileMetadata)
class FlowFileMetadataAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    """Admin view for FlowFileMetadata."""

    # Display these fields in the list view
    list_display = (
        "flow_file",
        "header_format",
        "footer_format",
        "file_identifier",
        "data_flow",
        "data_flow_version",
        "from_market_participant_role_code",
        "from_market_participant_id",
        "to_market_participant_role_code",
        "to_market_participant_id",
        "sending_application_id",
        "receiving_application_id",
        "broadcast",
        "test_data_flag",
        "total_group_count",
        "footer_checksum",
        "flow_count",
        "file_created_at",
        "file_completed_at",
    )

    # Fields that can be searched
    search_fields = (
        "flow_file",
        "file_identifier",
        "data_flow",
        "from_market_participant_id",
        "to_market_participant_id",
        "sending_application_id",
        "receiving_application_id",
    )

    # Filters for the sidebar
    list_filter = (
        "data_flow",
        "data_flow_version",
        "from_market_participant_role_code",
        "to_market_participant_role_code",
        "broadcast",
        "test_data_flag",
    )

    # Date hierarchy to make it easier to navigate by dates
    date_hierarchy = "file_created_at"
