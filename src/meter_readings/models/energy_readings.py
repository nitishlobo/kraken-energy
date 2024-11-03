"""Database models related to energy readings."""

from django.db import models

from meter_readings.models.flow_files import FlowFile


class EnergyReading(models.Model):
    """Energy reading model."""

    flow_file = models.ForeignKey(FlowFile, on_delete=models.CASCADE)
    mpan_core = models.CharField(max_length=13)
    bsc_validation_status = models.CharField(max_length=1)
    mpan_site_visit_reason = models.CharField(max_length=2)
    mpan_site_visit_additional_information = models.CharField(max_length=200)
    meter_id = models.CharField(max_length=10)
    meter_reading_type = models.CharField(max_length=1)
    meter_reading_site_visit_reason = models.CharField(max_length=2)
    meter_reading_site_visit_additional_information = models.CharField(max_length=200)
    meter_register_id = models.CharField(max_length=2)
    reading_at = models.DateTimeField(null=True)
    register_reading = models.FloatField(null=True)
    md_reset_at = models.DateTimeField(null=True)
    number_of_md_resets = models.PositiveSmallIntegerField(null=True)
    meter_reading_flag = models.CharField(max_length=1)
    reading_method = models.CharField(max_length=1)
    meter_reading_validation_result_reason = models.CharField(max_length=2)
    meter_reading_validation_result_status = models.CharField(max_length=1)
    register_reading_site_visit_reason = models.CharField(max_length=2)
    register_reading_site_visit_additional_information = models.CharField(max_length=200)

    def __str__(self) -> str:
        """Return string representation of model."""
        return f"{self.mpan_core}"
