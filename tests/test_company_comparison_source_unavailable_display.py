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
        assert item["association_mode"] == "not_evaluable_source_unavailable"
        assert item["sponsor_name_match_count"] is None
        assert item["non_sponsor_record_count"] is None
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
    assert item["association_mode"] == "clinicaltrials_gov_query_result_mvp"
    assert item["sponsor_name_match_count"] == 0
    assert item["non_sponsor_record_count"] == 0
    assert item["trial_count"] == 0
    assert item["display_trial_count"] == "0"
    assert result["query_metadata"]["source_errors"] == []
    assert "0 matching ClinicalTrials.gov trial record(s) included among 1 evaluable company query/queries" in result["landscape_summary"]["overall_trends"][1]


def test_company_comparison_marks_returned_records_requiring_manual_association_review(monkeypatch) -> None:
    def fake_search_clinical_trials_by_indication(indication, *, sponsor=None, page_size=20):
        return {
            "trials": [
                {
                    "trial_id": "NCT-SPONSOR",
                    "title": "Sponsor matched study",
                    "phase": "PHASE3",
                    "status": "COMPLETED",
                    "sponsor": sponsor,
                    "intervention_names": ["Example drug"],
                    "product_modality": ["small_molecule"],
                    "official_url": "https://clinicaltrials.gov/study/NCT-SPONSOR",
                },
                {
                    "trial_id": "NCT-OTHER",
                    "title": "Returned study requiring manual review",
                    "phase": "PHASE2",
                    "status": "RECRUITING",
                    "sponsor": "Other Sponsor Inc.",
                    "intervention_names": ["Example drug"],
                    "product_modality": ["small_molecule"],
                    "official_url": "https://clinicaltrials.gov/study/NCT-OTHER",
                },
            ],
            "query_metadata": {"indication": indication, "registries_searched": ["ClinicalTrials.gov"]},
        }

    monkeypatch.setattr(
        tools_clinical_trials,
        "search_clinical_trials_by_indication",
        fake_search_clinical_trials_by_indication,
    )

    result = tools_clinical_trials.compare_companies_by_indication(
        indication="gastric cancer",
        companies=["Merck"],
        registries=["ClinicalTrials.gov"],
        page_size=5,
    )

    assert "error" not in result
    item = result["company_comparison"][0]
    assert item["company"] == "Merck"
    assert item["association_mode"] == "clinicaltrials_gov_query_result_mvp"
    assert item["sponsor_name_match_count"] == 1
    assert item["non_sponsor_record_count"] == 1
    assert "returned 2 trial record(s)" in item["summary"]
    assert "1 record(s) have sponsor names matching" in item["summary"]
    assert "1 record(s) require manual review" in item["summary"]
    assert "confirmed product ownership" in item["summary"]

    sponsor_matched = item["key_trials"][0]
    manual_review = item["key_trials"][1]
    assert sponsor_matched["requested_company"] == "Merck"
    assert sponsor_matched["record_sponsor"] == "Merck"
    assert sponsor_matched["sponsor_matches_requested_company"] is True
    assert sponsor_matched["association_basis"] == "sponsor_name_match"
    assert manual_review["requested_company"] == "Merck"
    assert manual_review["record_sponsor"] == "Other Sponsor Inc."
    assert manual_review["sponsor_matches_requested_company"] is False
    assert manual_review["association_basis"] == "returned_by_clinicaltrials_gov_query_requires_manual_review"

    overall_trends = result["landscape_summary"]["overall_trends"]
    assert "1 returned record(s) do not have sponsor names matching" in overall_trends[2]
    assert any("product ownership require manual review" in gap for gap in result["landscape_summary"]["data_gaps"])
    assert result["query_metadata"]["association_mode"] == "clinicaltrials_gov_query_result_mvp"
