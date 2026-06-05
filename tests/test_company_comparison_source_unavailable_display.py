from __future__ import annotations

from src.core.errors import ErrorCode, build_error
from src.mcp_server import tools_clinical_trials


def test_company_comparison_marks_source_unavailable_as_not_evaluable(monkeypatch) -> None:
    def fake_search_clinical_trials_by_indication(indication, *, sponsor=None, page_size=20):
        return build_error(
            ErrorCode.SOURCE_UNAVAILABLE,
            "ClinicalTrials.gov search failed",
            details={"source": "ClinicalTrials.gov", "reason": "proxy unavailable"},
            suggested_next_action="Retry later and check source health for ClinicalTrials.gov API v2.",
        )

    monkeypatch.setattr(
        tools_clinical_trials,
        "search_clinical_trials_by_indication",
        fake_search_clinical_trials_by_indication,
    )

    result = tools_clinical_trials.compare_companies_by_indication(
        indication="gastric cancer",
        companies=["AstraZeneca", "Merck"],
        registries=["ClinicalTrials.gov"],
        date_range="3y",
        include_completed_trials=True,
        include_results=True,
        page_size=5,
    )

    assert "error" not in result
    comparisons = result["company_comparison"]
    assert len(comparisons) == 2

    for item in comparisons:
        assert item["activity_evaluable"] is False
        assert item["source_status"] == "unavailable"
        assert item["source_error_code"] == ErrorCode.SOURCE_UNAVAILABLE.value
        assert item["trial_count"] is None
        assert item["active_trial_count"] is None
        assert item["completed_trial_count"] is None
        assert item["display_trial_count"] == "Not evaluable — ClinicalTrials.gov source unavailable"
        assert item["display_active_trial_count"] == "Not evaluable"
        assert item["display_completed_trial_count"] == "Not evaluable"
        assert item["modalities"] == ["unknown"]
        assert "must not be interpreted as zero trial activity" in item["summary"]
        assert any("not evaluable" in limitation.lower() for limitation in item["known_limitations"])

    assert len(result["query_metadata"]["source_errors"]) == 2
    overall_trends = result["landscape_summary"]["overall_trends"]
    assert "No company-level ClinicalTrials.gov trial activity total is reported" in overall_trends[1]
    assert "0 matching ClinicalTrials.gov trial record(s)" not in "\n".join(overall_trends)
    assert "2 company(ies) not evaluable" in overall_trends[2]
    assert any("not evaluable must not be interpreted as zero trial activity" in gap for gap in result["landscape_summary"]["data_gaps"])


def test_company_comparison_keeps_zero_records_evaluable_when_source_succeeds(monkeypatch) -> None:
    def fake_search_clinical_trials_by_indication(indication, *, sponsor=None, page_size=20):
        return {
            "trials": [],
            "no_result_reason": "NO_MATCHING_RECORDS",
            "query_metadata": {
                "indication": indication,
                "registries_searched": ["ClinicalTrials.gov"],
            },
        }

    monkeypatch.setattr(
        tools_clinical_trials,
        "search_clinical_trials_by_indication",
        fake_search_clinical_trials_by_indication,
    )

    result = tools_clinical_trials.compare_companies_by_indication(
        indication="gastric cancer",
        companies=["AstraZeneca"],
        registries=["ClinicalTrials.gov"],
        page_size=5,
    )

    assert "error" not in result
    item = result["company_comparison"][0]
    assert item["activity_evaluable"] is True
    assert item["source_status"] == "available"
    assert item["source_error_code"] is None
    assert item["trial_count"] == 0
    assert item["display_trial_count"] == "0"
    assert result["query_metadata"]["source_errors"] == []
    assert "0 matching ClinicalTrials.gov trial record(s) included among 1 evaluable company(ies)" in result["landscape_summary"]["overall_trends"][1]
