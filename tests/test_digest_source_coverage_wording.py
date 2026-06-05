from __future__ import annotations

from src.core.errors import ErrorCode
from src.mcp_server import tools_digest


def _empty_regulatory_result() -> dict:
    return {"records": [], "known_limitations": []}


def _trial_result() -> dict:
    return {
        "trials": [
            {
                "trial_id": "NCT00000001",
                "title": "Gastric cancer study",
                "sponsor": "Example Sponsor",
                "phase": "PHASE2",
                "status": "RECRUITING",
                "last_update_date": "2026-01-01",
                "official_url": "https://clinicaltrials.gov/study/NCT00000001",
                "indications": ["gastric cancer"],
            }
        ],
        "query_metadata": {"known_limitations": []},
    }


def _warning_health() -> dict:
    return {"overall_status": "degraded", "known_limitations": []}


def _one_open_failure() -> dict:
    return {
        "summary": {
            "open_failure_count": 1,
            "known_limitations": ["source health limitation"],
        }
    }


def test_digest_distinguishes_global_open_failure_from_requested_source_error(monkeypatch) -> None:
    monkeypatch.setattr(tools_digest, "search_regulatory_updates", lambda **kwargs: _empty_regulatory_result())
    monkeypatch.setattr(tools_digest, "search_clinical_trials_by_indication", lambda *args, **kwargs: _trial_result())
    monkeypatch.setattr(tools_digest, "check_source_health", lambda: _warning_health())
    monkeypatch.setattr(tools_digest, "list_source_failures", lambda: _one_open_failure())

    digest = tools_digest.generate_regulatory_digest(
        digest_type="combined",
        agencies=["TFDA"],
        registries=["ClinicalTrials.gov"],
        indications=["gastric cancer"],
        companies=["AstraZeneca"],
        topics=["submission"],
        date_range="1y",
        limit=5,
        include_source_health_summary=True,
    )

    summary = digest["digest"]["executive_summary"]
    limitations = digest["digest"]["known_limitations"]

    assert digest["query_metadata"]["source_errors"] == []
    assert "no source query errors occurred for the requested sources" in summary
    assert "source health tools" in summary
    assert any("outside the requested digest source set" in item for item in limitations)


def test_digest_marks_partial_coverage_for_requested_source_error(monkeypatch) -> None:
    def fake_regulatory(**kwargs):
        if kwargs.get("agency") == "FDA":
            return {
                "error": {
                    "code": ErrorCode.SOURCE_UNAVAILABLE.value,
                    "message": "All requested FDA sources are unavailable",
                }
            }
        return _empty_regulatory_result()

    monkeypatch.setattr(tools_digest, "search_regulatory_updates", fake_regulatory)
    monkeypatch.setattr(tools_digest, "search_clinical_trials_by_indication", lambda *args, **kwargs: _trial_result())
    monkeypatch.setattr(tools_digest, "check_source_health", lambda: _warning_health())
    monkeypatch.setattr(tools_digest, "list_source_failures", lambda: _one_open_failure())

    digest = tools_digest.generate_regulatory_digest(
        digest_type="combined",
        agencies=["FDA", "TFDA"],
        registries=["ClinicalTrials.gov"],
        indications=["gastric cancer"],
        companies=["AstraZeneca"],
        topics=["submission"],
        date_range="1y",
        limit=5,
        include_source_health_summary=True,
    )

    summary = digest["digest"]["executive_summary"]
    limitations = digest["digest"]["known_limitations"]
    source_errors = digest["query_metadata"]["source_errors"]

    assert len(source_errors) == 1
    assert source_errors[0]["source"] == "FDA"
    assert "Coverage is partial for requested source(s): FDA" in summary
    assert "must not be interpreted as no updates for unavailable sources" in summary
    assert any("Coverage is partial" in item and "FDA" in item for item in limitations)
