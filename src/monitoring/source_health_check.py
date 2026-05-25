from datetime import datetime, timezone
from src.core.models import SourceHealthEvent

VALID_FAILURE_TYPES = {
    "api_status", "schema_validation", "rss_status", "html_selector", "attachment_download",
    "empty_result", "date_parsing", "encoding", "data_volume_anomaly", "duplicate_anomaly", "unknown"
}


def create_source_health_event(*, failure_id: str, source_id: str, agency_or_registry: str, source_type: str,
                               endpoint_url: str, failure_type: str, severity: str, error_message: str,
                               suggested_fix: str, suggested_connector_file: str | None = None) -> SourceHealthEvent:
    ft = failure_type if failure_type in VALID_FAILURE_TYPES else "unknown"
    return SourceHealthEvent(
        failure_id=failure_id, source_id=source_id, agency_or_registry=agency_or_registry, source_type=source_type,
        endpoint_url=endpoint_url, status="open", failure_type=ft, severity=severity,
        detected_at=datetime.now(timezone.utc).isoformat(), error_message=error_message,
        suggested_fix=suggested_fix, suggested_connector_file=suggested_connector_file)
