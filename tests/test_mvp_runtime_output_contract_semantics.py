"""MVP runtime output contract semantics tests.

These tests characterize the current MVP MCP tool output semantics that future
renderers must not collapse into ambiguous dashboard states. They are test-only
contract coverage and intentionally avoid runtime, connector, dashboard, docs,
and workflow changes.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.core.errors import ErrorCode
from src.mcp_server import tools_clinical_trials, tools_digest
from src.mcp_server.server import TOOL_REGISTRY


_APPROVED_MVP_TOOLS = {
    "search_regulatory_updates",
    "get_regulatory_document_detail",
    "compare_regulatory_updates",
    "search_clinical_trials_by_indication",
    "compare_companies_by_indication",
    "check_source_health",
    "list_source_failures",
    "generate_regulatory_digest",
}

_NON_INFERENCE_FIELDS = {
    "approval_probability",
    "clinical_success",
    "clinical_success_score",
    "commercial_strength",
    "commercial_strength_score",
    "company_superiority",
    "product_ownership",
    "company_alias",
    "corporate_family",
    "ownership_inference",
}


def _regulatory_record(*, record_id: str, agency: str) -> dict[str, Any]:
    source_type = "FDA_GUIDANCE" if agency == "FDA" else "TFDA_HTML"
    official_url = (
        f"https://www.fda.gov/regulatory-information/search-fda-guidance-documents/{record_id}"
        if agency == "FDA"
        else f"https://www.fda.gov.tw/TC/newsContent.aspx?id={record_id}"
    )
    return {
        "id": record_id,
        "title": f"{agency} MVP runtime contract update",
        "official_url": official_url,
        "publication_date": "2026-01-15",
        "last_update_date": "2026-01-16",
        "source_type": source_type,
        "document_type": "guidance" if agency == "FDA" else "regulatory_update",
        "document_status": "final" if agency == "FDA" else "published",
        "product_modality": ["unknown"],
        "topics": ["quality"],
        "summary": "Runtime output contract fixture.",
        "known_limitations": [],
    }


def _clinical_study() -> dict[str, Any]:
    return {
        "protocolSection": {
            "identificationModule": {
                "nctId": "NCT12345678",
                "briefTitle": "MVP runtime output contract trial",
            },
            "sponsorCollaboratorsModule": {"leadSponsor": {"name": "Acme Pharma"}},
            "statusModule": {
                "overallStatus": "RECRUITING",
                "hasResults": False,
                "lastUpdateSubmitDateStruct": {"date": "2026-01-20"},
            },
            "designModule": {"phases": ["PHASE2"]},
            "armsInterventionsModule": {"interventions": [{"name": "contract test drug"}]},
            "conditionsModule": {"conditions": ["gastric cancer"]},
            "descriptionModule": {"briefSummary": "Fixture trial for output contract semantics."},
        }
    }


def _source_unavailable(message: str = "upstream unavailable") -> dict[str, Any]:
    return {
        "error": {
            "code": ErrorCode.SOURCE_UNAVAILABLE.value,
            "message": message,
        }
    }


def _assert_no_inference_field_keys(value: Any, *, path: str = "result") -> None:
    if isinstance(value, Mapping):
        forbidden = sorted(set(value) & _NON_INFERENCE_FIELDS)
        assert not forbidden, f"{path} exposes non-MVP inference field keys: {forbidden}"
        for key, child in value.items():
            _assert_no_inference_field_keys(child, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _assert_no_inference_field_keys(child, path=f"{path}[{index}]")


def test_current_tool_registry_is_exactly_the_approved_8_mvp_tools():
    assert set(TOOL_REGISTRY) == _APPROVED_MVP_TOOLS


def test_search_regulatory_updates_no_match_is_explicit_not_source_unavailable(monkeypatch):
    class EmptyFDAClient:
        def search_updates(self, **kwargs):
            return []

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: EmptyFDAClient())

    result = TOOL_REGISTRY["search_regulatory_updates"](agency="FDA", query="no matching contract fixture")

    assert "error" not in result
    assert result["records"] == []
    assert result["no_result_reason"] == "NO_MATCHING_RECORDS"
    assert result.get("error", {}).get("code") != ErrorCode.SOURCE_UNAVAILABLE.value


def test_search_regulatory_updates_source_unavailable_is_error_not_empty_records(monkeypatch):
    class FailingFDAClient:
        def search_updates(self, **kwargs):
            return _source_unavailable("FDA source unavailable")

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FailingFDAClient())

    result = TOOL_REGISTRY["search_regulatory_updates"](agency="FDA")

    assert result["error"]["code"] == ErrorCode.SOURCE_UNAVAILABLE.value
    assert "records" not in result
    assert result.get("no_result_reason") != "NO_MATCHING_RECORDS"


def test_search_clinical_trials_no_match_is_explicit_not_source_unavailable(monkeypatch):
    class EmptyClinicalTrialsClient:
        def search_studies(self, **kwargs):
            return {"studies": []}

    monkeypatch.setattr(
        "src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient",
        lambda: EmptyClinicalTrialsClient(),
    )

    result = TOOL_REGISTRY["search_clinical_trials_by_indication"]("no matching indication")

    assert "error" not in result
    assert result["trials"] == []
    assert result["no_result_reason"] == "NO_MATCHING_RECORDS"
    assert result.get("error", {}).get("code") != ErrorCode.SOURCE_UNAVAILABLE.value


def test_search_clinical_trials_source_unavailable_is_error_not_empty_trials(monkeypatch):
    class FailingClinicalTrialsClient:
        def search_studies(self, **kwargs):
            return _source_unavailable("ClinicalTrials.gov unavailable")

    monkeypatch.setattr(
        "src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient",
        lambda: FailingClinicalTrialsClient(),
    )

    result = TOOL_REGISTRY["search_clinical_trials_by_indication"]("gastric cancer")

    assert result["error"]["code"] == ErrorCode.SOURCE_UNAVAILABLE.value
    assert "trials" not in result
    assert result.get("no_result_reason") != "NO_MATCHING_RECORDS"


def test_compare_regulatory_updates_preserves_partial_agency_failure_metadata(monkeypatch):
    class SuccessfulFDAClient:
        def search_updates(self, **kwargs):
            return [_regulatory_record(record_id="fda-partial-1", agency="FDA")]

    class FailingTFDAClient:
        def search_updates(self, **kwargs):
            return _source_unavailable("TFDA source unavailable")

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: SuccessfulFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FailingTFDAClient())

    result = TOOL_REGISTRY["compare_regulatory_updates"](agencies=["FDA", "TFDA"], comparison_axis="agency")

    assert "error" not in result
    assert result["query_metadata"]["successful_agencies"] == ["FDA"]
    failures = result["query_metadata"]["partial_lookup_failures"]
    assert failures == [
        {
            "agency": "TFDA",
            "code": ErrorCode.SOURCE_UNAVAILABLE.value,
            "message": "TFDA source unavailable",
            "details": "",
            "suggested_next_action": "",
        }
    ]


def test_get_regulatory_document_detail_all_source_failure_returns_source_unavailable(monkeypatch):
    class FailingFDAClient:
        def search_updates(self, **kwargs):
            return _source_unavailable("FDA detail unavailable")

    class FailingTFDAClient:
        def search_updates(self, **kwargs):
            return _source_unavailable("TFDA detail unavailable")

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FailingFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FailingTFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"]("missing-doc")

    assert result["error"]["code"] == ErrorCode.SOURCE_UNAVAILABLE.value
    failures = result["error"]["details"]["partial_lookup_failures"]
    assert {failure["agency"] for failure in failures} == {"FDA", "TFDA"}
    assert {failure["code"] for failure in failures} == {ErrorCode.SOURCE_UNAVAILABLE.value}


def test_get_regulatory_document_detail_partial_failure_not_found_preserves_partial_results(monkeypatch):
    class FailingFDAClient:
        def search_updates(self, **kwargs):
            return _source_unavailable("FDA detail unavailable")

    class EmptyTFDAClient:
        def search_updates(self, **kwargs):
            return []

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FailingFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: EmptyTFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"]("missing-doc")

    assert result["error"]["code"] == ErrorCode.PARTIAL_RESULTS.value
    failures = result["error"]["details"]["partial_lookup_failures"]
    assert failures[0]["agency"] == "FDA"
    assert failures[0]["code"] == ErrorCode.SOURCE_UNAVAILABLE.value


def test_compare_companies_source_unavailable_is_not_evaluable_not_zero_activity(monkeypatch):
    def fake_search_clinical_trials_by_indication(indication, **kwargs):
        return _source_unavailable("ClinicalTrials.gov sponsor search unavailable")

    monkeypatch.setattr(
        tools_clinical_trials,
        "search_clinical_trials_by_indication",
        fake_search_clinical_trials_by_indication,
    )

    result = TOOL_REGISTRY["compare_companies_by_indication"](
        indication="gastric cancer",
        companies=["Acme Pharma"],
    )

    company = result["company_comparison"][0]
    assert company["activity_evaluable"] is False
    assert company["source_status"] == "unavailable"
    assert company["source_error_code"] == ErrorCode.SOURCE_UNAVAILABLE.value
    assert company["trial_count"] is None
    assert company["active_trial_count"] is None
    limitation_text = " ".join(company["known_limitations"] + result["landscape_summary"]["data_gaps"] + [company["summary"]])
    assert "must not be interpreted as zero" in limitation_text


def test_generate_regulatory_digest_preserves_source_errors_and_zero_update_limitation(monkeypatch):
    def fake_search_regulatory_updates(**kwargs):
        if kwargs["agency"] == "FDA":
            return {"records": [_regulatory_record(record_id="fda-digest-1", agency="FDA")], "known_limitations": []}
        return _source_unavailable("TFDA digest unavailable")

    def fake_check_source_health(**kwargs):
        return {"overall_status": "available", "known_limitations": []}

    def fake_list_source_failures(**kwargs):
        return {"summary": {"open_failure_count": 0, "known_limitations": []}}

    monkeypatch.setattr(tools_digest, "search_regulatory_updates", fake_search_regulatory_updates)
    monkeypatch.setattr(tools_digest, "check_source_health", fake_check_source_health)
    monkeypatch.setattr(tools_digest, "list_source_failures", fake_list_source_failures)

    result = TOOL_REGISTRY["generate_regulatory_digest"](
        digest_type="regulatory_update",
        agencies=["FDA", "TFDA"],
        limit=5,
    )

    assert "error" not in result
    source_errors = result["query_metadata"]["source_errors"]
    assert source_errors[0]["source"] == "TFDA"
    assert source_errors[0]["error"]["code"] == ErrorCode.SOURCE_UNAVAILABLE.value
    limitation_text = " ".join(result["digest"]["known_limitations"] + [result["digest"]["executive_summary"]])
    assert "must not be interpreted as no updates" in limitation_text


def test_clinical_company_and_digest_outputs_do_not_expose_non_mvp_inference_fields(monkeypatch):
    class SuccessfulClinicalTrialsClient:
        def search_studies(self, **kwargs):
            return {"studies": [_clinical_study()]}

    def fake_digest_search_regulatory_updates(**kwargs):
        return {"records": [_regulatory_record(record_id="fda-digest-clean-1", agency="FDA")], "known_limitations": []}

    def fake_check_source_health(**kwargs):
        return {"overall_status": "available", "known_limitations": []}

    def fake_list_source_failures(**kwargs):
        return {"summary": {"open_failure_count": 0, "known_limitations": []}}

    monkeypatch.setattr(
        "src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient",
        lambda: SuccessfulClinicalTrialsClient(),
    )
    monkeypatch.setattr(tools_digest, "search_regulatory_updates", fake_digest_search_regulatory_updates)
    monkeypatch.setattr(tools_digest, "check_source_health", fake_check_source_health)
    monkeypatch.setattr(tools_digest, "list_source_failures", fake_list_source_failures)

    clinical_search = TOOL_REGISTRY["search_clinical_trials_by_indication"]("gastric cancer")
    company_comparison = TOOL_REGISTRY["compare_companies_by_indication"](
        indication="gastric cancer",
        companies=["Acme Pharma"],
    )
    digest = TOOL_REGISTRY["generate_regulatory_digest"](
        digest_type="combined",
        agencies=["FDA"],
        registries=["ClinicalTrials.gov"],
        indications=["gastric cancer"],
        companies=["Acme Pharma"],
        limit=5,
    )

    assert "error" not in clinical_search
    assert "error" not in company_comparison
    assert "error" not in digest
    _assert_no_inference_field_keys(clinical_search, path="clinical_search")
    _assert_no_inference_field_keys(company_comparison, path="company_comparison")
    _assert_no_inference_field_keys(digest, path="digest")
