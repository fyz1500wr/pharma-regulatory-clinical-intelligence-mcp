from src.core.models import RegulatoryUpdate, ClinicalTrialRecord, SourceHealthEvent, DigestRecord


def test_model_creation():
    reg = RegulatoryUpdate(id="1", agency="FDA", region="US", title="T", retrieved_at="2026-01-01T00:00:00Z", official_url="https://x", source_type="API")
    trial = ClinicalTrialRecord(trial_id="NCT1", registry="ClinicalTrials.gov", official_url="https://ct", title="Study", sponsor="S", retrieved_at="2026-01-01T00:00:00Z")
    health = SourceHealthEvent(failure_id="f1", source_id="FDA_openFDA", agency_or_registry="FDA", source_type="API", endpoint_url="https://api.fda.gov", status="open", failure_type="api_status", severity="medium", detected_at="2026-01-01T00:00:00Z", error_message="err", suggested_fix="retry")
    digest = DigestRecord(digest_id="d1", digest_type="combined", date_range="1m", generated_at="2026-01-01T00:00:00Z", sources_searched=["FDA"], search_criteria={})
    assert reg.agency == "FDA" and trial.registry == "ClinicalTrials.gov" and health.failure_type == "api_status" and digest.digest_type == "combined"
