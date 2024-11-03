"""Flow file database model."""

from django.db import models


class FlowFile(models.Model):
    """Flow file details."""

    name = models.CharField(max_length=255)
    extension = models.CharField(max_length=10)
    imported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return string representation of model."""
        return f"{self.name}{self.extension}"


class FlowFileMetadata(models.Model):
    """Flow file metadata (header and footer details).

    For information on header and footer refer to page 8:
    https://assets.elexon.co.uk/wp-content/uploads/2012/02/28171532/p116_req_spec.pdf
    """

    flow_file = models.ForeignKey(FlowFile, on_delete=models.CASCADE)
    header_format = models.CharField(max_length=3)
    footer_format = models.CharField(max_length=3)
    file_identifier = models.CharField(max_length=10)
    data_flow = models.CharField(max_length=5)
    data_flow_version = models.SmallIntegerField()
    from_market_participant_role_code = models.CharField(max_length=1)
    from_market_participant_id = models.CharField(max_length=4)
    to_market_participant_role_code = models.CharField(max_length=1)
    to_market_participant_id = models.CharField(max_length=4)
    sending_application_id = models.CharField(max_length=5)
    receiving_application_id = models.CharField(max_length=5)
    broadcast = models.CharField(max_length=1)
    test_data_flag = models.CharField(max_length=4)
    total_group_count = models.CharField(max_length=5)
    footer_checksum = models.SmallIntegerField(null=True, blank=True)
    flow_count = models.CharField(max_length=1)
    file_created_at = models.DateTimeField()
    file_completed_at = models.DateTimeField()

    def __str__(self) -> str:
        """Return string representation of model."""
        return f"{self.file_identifier}"
