from src.monitoring.source_health_check import create_source_health_event


def test_source_health_event_creation():
    ev = create_source_health_event(
        failure_id="x", source_id="ClinicalTrialsGov_API", agency_or_registry="ClinicalTrials.gov", source_type="API",
        endpoint_url="https://clinicaltrials.gov/api/v2/studies", failure_type="schema_validation", severity="high",
        error_message="missing field", suggested_fix="update mapper")
    assert ev.failure_type == "schema_validation"
    assert ev.status == "open"
