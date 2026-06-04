from __future__ import annotations

from src.core.errors import ErrorCode, build_error
from src.mcp_server import tools_digest


def test_generate_regulatory_digest_preserves_fda_blocked_source_error(monkeypatch) -> None:
    def fake_search_regulatory_updates(**kwargs):
        agency = kwargs["agency"]
        if agency == "FDA":
            return build_error(
                ErrorCode.SOURCE_UNAVAILABLE,
                "FDA search failed: BLOCKED_SOURCE runtime egress policy prevented validation",
                details={"status": "BLOCKED_SOURCE", "source": "FDA"},
                suggested_next_action="Check FDA source health before interpreting FDA coverage.",
            )
        if agency == "TFDA":
            return {
                "records": [],
                "no_result_reason": "NO_MATCHING_RECORDS",
                "query_metadata": {
                    "agency_searched": ["TFDA"],
                    "filters_applied": {"query": kwargs.get("query")},
                },
                "known_limitations": ["TFDA returned no normalized records for the selected filters."],
            }
        raise AssertionError(f"Unexpected agency: {agency}")

    def fake_search_clinical_trials_by_indication(indication, *, sponsor=None, page_size=10):
        return {
            "trials": [
                {
                    "trial_id": "NCT00000000",
                    "title": "Mock gastric cancer study",
                    "sponsor": sponsor or "Mock Sponsor",
                    "phase": "Phase 2",
                    "status": "Recruiting",
                    "last_update_date": "2026-01-01",
                    "official_url": "https://clinicaltrials.gov/study/NCT00000000",
                    "indications": [indication],
                }
            ],
            "query_metadata": {"known_limitations": ["Mock ClinicalTrials.gov response for offline regression."]},
        }

    def fake_check_source_health():
        return {
            "overall_status": "degraded",
            "known_limitations": [
                "FDA BLOCKED_SOURCE is a source-health limitation and must not be interpreted as zero FDA regulatory updates."
            ],
        }

    def fake_list_source_failures():
        return {
            "summary": {
                "open_failure_count": 1,
                "known_limitations": ["FDA source failure remains visible in source-health summary."],
            }
        }

    monkeypatch.setattr(tools_digest, "search_regulatory_updates", fake_search_regulatory_updates)
    monkeypatch.setattr(tools_digest, "search_clinical_trials_by_indication", fake_search_clinical_trials_by_indication)
    monkeypatch.setattr(tools_digest, "check_source_health", fake_check_source_health)
    monkeypatch.setattr(tools_digest, "list_source_failures", fake_list_source_failures)

    result = tools_digest.generate_regulatory_digest(
        digest_type="combined",
        agencies=["FDA", "TFDA"],
        registries=["ClinicalTrials.gov"],
        indications=["gastric cancer"],
        companies=["Mock Sponsor"],
        topics=["submission"],
        date_range="1y",
        limit=5,
        include_impact_matrix=True,
        include_source_health_summary=True,
    )

    assert "error" not in result
    digest = result["digest"]
    metadata = result["query_metadata"]

    assert digest["sources_searched"] == ["FDA", "TFDA", "ClinicalTrials.gov"]
    assert digest["key_regulatory_updates"] == []
    assert len(digest["key_clinical_trial_updates"]) == 1

    source_errors = metadata["source_errors"]
    assert len(source_errors) == 1
    assert source_errors[0]["source"] == "FDA"
    assert source_errors[0]["error"]["code"] == ErrorCode.SOURCE_UNAVAILABLE.value
    assert "BLOCKED_SOURCE" in source_errors[0]["error"]["message"]
    assert source_errors[0]["error"]["details"]["status"] == "BLOCKED_SOURCE"

    assert digest["source_health_summary"]["status"] == "warning"
    assert digest["source_health_summary"]["open_failures"] == 1
    assert any("FDA BLOCKED_SOURCE" in item for item in digest["known_limitations"])

    executive_summary = digest["executive_summary"]
    assert "source query error" in executive_summary
    assert "not a final regulatory or clinical assessment" in executive_summary
    assert "Included 0 regulatory update(s)" in executive_summary
