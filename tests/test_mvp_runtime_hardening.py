"""MVP v1 runtime hardening contract tests.

These tests assert MVP v1 contract guarantees that the existing suite touches
only indirectly:

1. Source-unavailable failures are NOT rendered as "no records".
2. Non-MVP source parameters are rejected with INVALID_PARAMETER for every
   tool that accepts a source/agency/registry argument.
3. generate_regulatory_digest preserves source_errors and known_limitations
   when every requested agency fails.
4. Clinical trial tools never expose approval-probability / clinical-success /
   commercial-strength / corporate-family / product-ownership / alias fields.
5. compare_companies_by_indication carries the conservative known-limitations
   that distinguish MVP query results from confirmed company activity.
"""

from __future__ import annotations

from src.core.errors import ErrorCode
from src.mcp_server import tools_clinical_trials, tools_digest
from src.mcp_server.server import TOOL_REGISTRY


_INFERENCE_FIELDS = (
    "approval_probability",
    "clinical_success",
    "commercial_strength",
    "corporate_family",
    "product_ownership",
    "company_alias",
    "alias",
    "licensing_relationship",
)


_NON_MVP_AGENCIES = ["EMA", "NMPA", "CDE", "PMDA"]
_NON_MVP_REGISTRIES = ["EU_CTIS", "WHO_ICTRP"]
_NON_MVP_HEALTH_SOURCES = ["EMA", "NMPA", "PMDA", "EU_CTIS", "WHO_ICTRP"]


# ---------------------------------------------------------------------------
# 1. Source-unavailable must not be rendered as "no records"
# ---------------------------------------------------------------------------


def test_search_clinical_trials_source_unavailable_returns_error_not_empty_records(monkeypatch):
    class FailingClient:
        def search_studies(self, **kwargs):
            return {"error": {"code": "SOURCE_UNAVAILABLE", "message": "proxy unreachable"}}

    monkeypatch.setattr(
        "src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient",
        lambda: FailingClient(),
    )

    result = TOOL_REGISTRY["search_clinical_trials_by_indication"]("gastric cancer")

    assert "error" in result
    assert result["error"]["code"] == ErrorCode.SOURCE_UNAVAILABLE.value
    assert "trials" not in result
    assert result.get("no_result_reason") != "NO_MATCHING_RECORDS"


def test_search_regulatory_updates_fda_source_unavailable_returns_error_not_empty_records(monkeypatch):
    class FailingFDA:
        def search_updates(self, **kwargs):
            raise RuntimeError("FDA upstream timeout")

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FailingFDA())

    result = TOOL_REGISTRY["search_regulatory_updates"](agency="FDA")

    assert "error" in result
    assert result["error"]["code"] == ErrorCode.SOURCE_UNAVAILABLE.value
    assert "records" not in result
    assert result.get("no_result_reason") != "NO_MATCHING_RECORDS"


def test_search_regulatory_updates_tfda_source_unavailable_returns_error_not_empty_records(monkeypatch):
    class FailingTFDA:
        def search_updates(self, **kwargs):
            raise RuntimeError("TFDA upstream timeout")

    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FailingTFDA())

    result = TOOL_REGISTRY["search_regulatory_updates"](agency="TFDA")

    assert "error" in result
    assert result["error"]["code"] == ErrorCode.SOURCE_UNAVAILABLE.value
    assert "records" not in result


def test_compare_regulatory_updates_all_sources_unavailable_returns_error(monkeypatch):
    class FailingFDA:
        def search_updates(self, **kwargs):
            raise RuntimeError("FDA down")

    class FailingTFDA:
        def search_updates(self, **kwargs):
            raise RuntimeError("TFDA down")

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FailingFDA())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FailingTFDA())

    result = TOOL_REGISTRY["compare_regulatory_updates"](agencies=["FDA", "TFDA"])

    assert "error" in result
    assert result["error"]["code"] == ErrorCode.SOURCE_UNAVAILABLE.value
    assert "comparison" not in result


def test_get_regulatory_document_detail_all_sources_unavailable_returns_error(monkeypatch):
    class FailingFDA:
        def search_updates(self, **kwargs):
            raise RuntimeError("FDA down")

    class FailingTFDA:
        def search_updates(self, **kwargs):
            raise RuntimeError("TFDA down")

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FailingFDA())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FailingTFDA())

    result = TOOL_REGISTRY["get_regulatory_document_detail"](document_id="some-doc")

    assert "error" in result
    assert result["error"]["code"] == ErrorCode.SOURCE_UNAVAILABLE.value
    assert "document" not in result


def test_compare_companies_marks_source_unavailable_distinct_from_zero_records(monkeypatch):
    class FailingClient:
        def search_studies(self, **kwargs):
            return {"error": {"code": "SOURCE_UNAVAILABLE", "message": "proxy unreachable"}}

    monkeypatch.setattr(
        "src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient",
        lambda: FailingClient(),
    )

    result = TOOL_REGISTRY["compare_companies_by_indication"](
        indication="NSCLC",
        companies=["Acme Pharma"],
    )

    assert "error" not in result
    item = result["company_comparison"][0]
    assert item["activity_evaluable"] is False
    assert item["trial_count"] is None
    assert item["association_mode"] == "not_evaluable_source_unavailable"
    assert item["source_status"] == "unavailable"


# ---------------------------------------------------------------------------
# 2. ClinicalTrials.gov query parameters are normalized before client calls
# ---------------------------------------------------------------------------


def _run_clinical_search_with_capture(monkeypatch, **kwargs):
    seen = {}

    class CapturingClient:
        def search_studies(self, **client_kwargs):
            seen.update(client_kwargs)
            return {"studies": []}

    monkeypatch.setattr(
        "src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient",
        lambda: CapturingClient(),
    )

    result = TOOL_REGISTRY["search_clinical_trials_by_indication"]("NSCLC", **kwargs)
    return result, seen


def _assert_invalid_clinical_search_parameter(monkeypatch, **kwargs):
    class UnexpectedClient:
        def search_studies(self, **client_kwargs):
            raise AssertionError(
                "ClinicalTrials.gov client should not be called for invalid parameters"
            )

    monkeypatch.setattr(
        "src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient",
        lambda: UnexpectedClient(),
    )

    result = TOOL_REGISTRY["search_clinical_trials_by_indication"]("NSCLC", **kwargs)
    assert "error" in result
    assert result["error"]["code"] == ErrorCode.INVALID_PARAMETER.value


def test_search_clinical_trials_normalizes_phase_string_to_single_item_list(monkeypatch):
    result, seen = _run_clinical_search_with_capture(monkeypatch, phase="PHASE2")

    assert "error" not in result
    assert seen["phase"] == ["PHASE2"]


def test_search_clinical_trials_normalizes_status_string_to_single_item_list(monkeypatch):
    result, seen = _run_clinical_search_with_capture(monkeypatch, status="RECRUITING")

    assert "error" not in result
    assert seen["status"] == ["RECRUITING"]


def test_search_clinical_trials_preserves_phase_list(monkeypatch):
    result, seen = _run_clinical_search_with_capture(monkeypatch, phase=["PHASE2", "PHASE3"])

    assert "error" not in result
    assert seen["phase"] == ["PHASE2", "PHASE3"]


def test_search_clinical_trials_preserves_status_list(monkeypatch):
    result, seen = _run_clinical_search_with_capture(monkeypatch, status=["RECRUITING", "COMPLETED"])

    assert "error" not in result
    assert seen["status"] == ["RECRUITING", "COMPLETED"]


def test_search_clinical_trials_rejects_zero_page_size(monkeypatch):
    _assert_invalid_clinical_search_parameter(monkeypatch, page_size=0)


def test_search_clinical_trials_rejects_boolean_page_size(monkeypatch):
    _assert_invalid_clinical_search_parameter(monkeypatch, page_size=True)


def test_search_clinical_trials_rejects_non_numeric_page_size_string(monkeypatch):
    _assert_invalid_clinical_search_parameter(monkeypatch, page_size="abc")


def test_search_clinical_trials_rejects_page_size_above_mvp_limit(monkeypatch):
    _assert_invalid_clinical_search_parameter(monkeypatch, page_size=101)


def test_search_clinical_trials_rejects_non_string_phase(monkeypatch):
    _assert_invalid_clinical_search_parameter(monkeypatch, phase=123)


def test_search_clinical_trials_rejects_non_string_status_mapping(monkeypatch):
    _assert_invalid_clinical_search_parameter(monkeypatch, status={"status": "RECRUITING"})


# ---------------------------------------------------------------------------
# 3. Invalid / non-MVP source parameters return INVALID_PARAMETER
# ---------------------------------------------------------------------------


def test_search_regulatory_updates_rejects_non_mvp_agencies():
    for agency in _NON_MVP_AGENCIES:
        result = TOOL_REGISTRY["search_regulatory_updates"](agency=agency)
        assert "error" in result, agency
        assert result["error"]["code"] == ErrorCode.INVALID_PARAMETER.value, agency


def test_compare_regulatory_updates_rejects_non_mvp_agencies():
    for agency in _NON_MVP_AGENCIES:
        result = TOOL_REGISTRY["compare_regulatory_updates"](agencies=["FDA", agency])
        assert "error" in result, agency
        assert result["error"]["code"] == ErrorCode.INVALID_PARAMETER.value, agency


def test_generate_regulatory_digest_rejects_non_mvp_agencies():
    for agency in _NON_MVP_AGENCIES:
        result = TOOL_REGISTRY["generate_regulatory_digest"](agencies=[agency])
        assert "error" in result, agency
        assert result["error"]["code"] == ErrorCode.INVALID_PARAMETER.value, agency


def test_generate_regulatory_digest_rejects_non_mvp_registries():
    for registry in _NON_MVP_REGISTRIES:
        result = TOOL_REGISTRY["generate_regulatory_digest"](registries=[registry])
        assert "error" in result, registry
        assert result["error"]["code"] == ErrorCode.INVALID_PARAMETER.value, registry


def test_compare_companies_by_indication_rejects_non_mvp_registries():
    for registry in _NON_MVP_REGISTRIES:
        result = TOOL_REGISTRY["compare_companies_by_indication"](
            indication="NSCLC",
            companies=["Acme Pharma"],
            registries=[registry],
        )
        assert "error" in result, registry
        assert result["error"]["code"] == ErrorCode.INVALID_PARAMETER.value, registry


def test_check_source_health_rejects_non_mvp_sources():
    for source in _NON_MVP_HEALTH_SOURCES:
        result = TOOL_REGISTRY["check_source_health"](source=source)
        assert "error" in result, source
        assert result["error"]["code"] == ErrorCode.INVALID_PARAMETER.value, source


def test_list_source_failures_rejects_non_mvp_sources():
    for source in _NON_MVP_HEALTH_SOURCES:
        result = TOOL_REGISTRY["list_source_failures"](sources=[source])
        assert "error" in result, source
        assert result["error"]["code"] == ErrorCode.INVALID_PARAMETER.value, source


# ---------------------------------------------------------------------------
# 3. generate_regulatory_digest preserves source_errors / known_limitations
# ---------------------------------------------------------------------------


def test_generate_regulatory_digest_regulatory_only_preserves_all_agency_source_errors(monkeypatch):
    def fake_search_regulatory_updates(**kwargs):
        agency = kwargs["agency"]
        return {
            "error": {
                "code": ErrorCode.SOURCE_UNAVAILABLE.value,
                "message": f"{agency} source unavailable",
            }
        }

    def fake_check_source_health(**kwargs):
        return {"overall_status": "degraded", "known_limitations": []}

    def fake_list_source_failures(**kwargs):
        return {"summary": {"open_failure_count": 2, "known_limitations": []}}

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
    sources_in_errors = sorted(item["source"] for item in source_errors)
    assert sources_in_errors == ["FDA", "TFDA"]
    assert result["digest"]["key_regulatory_updates"] == []

    known_limitations = result["digest"]["known_limitations"]
    joined = " ".join(known_limitations)
    assert "Coverage is partial" in joined
    assert "FDA" in joined and "TFDA" in joined
    assert "must not be interpreted as no updates" in joined

    executive_summary = result["digest"]["executive_summary"]
    assert "Coverage is partial for requested source(s)" in executive_summary
    assert "FDA" in executive_summary and "TFDA" in executive_summary


def test_generate_regulatory_digest_combined_propagates_clinical_source_errors(monkeypatch):
    def fake_search_regulatory_updates(**kwargs):
        return {"records": [], "known_limitations": []}

    def fake_search_clinical_trials_by_indication(indication, **kwargs):
        return {
            "error": {
                "code": ErrorCode.SOURCE_UNAVAILABLE.value,
                "message": "ClinicalTrials.gov sponsor search failed",
            }
        }

    def fake_check_source_health(**kwargs):
        return {"overall_status": "degraded", "known_limitations": []}

    def fake_list_source_failures(**kwargs):
        return {"summary": {"open_failure_count": 1, "known_limitations": []}}

    monkeypatch.setattr(tools_digest, "search_regulatory_updates", fake_search_regulatory_updates)
    monkeypatch.setattr(
        tools_digest, "search_clinical_trials_by_indication", fake_search_clinical_trials_by_indication
    )
    monkeypatch.setattr(tools_digest, "check_source_health", fake_check_source_health)
    monkeypatch.setattr(tools_digest, "list_source_failures", fake_list_source_failures)

    result = TOOL_REGISTRY["generate_regulatory_digest"](
        digest_type="combined",
        agencies=["FDA"],
        registries=["ClinicalTrials.gov"],
        indications=["gastric cancer"],
        companies=["Acme Pharma"],
        limit=5,
    )

    assert "error" not in result
    source_errors = result["query_metadata"]["source_errors"]
    assert any(item["source"].startswith("ClinicalTrials.gov:") for item in source_errors)
    assert result["digest"]["key_clinical_trial_updates"] == []
    assert "must not be interpreted as no updates" in " ".join(result["digest"]["known_limitations"])


# ---------------------------------------------------------------------------
# 4. Clinical trial tools must not expose inference fields
# ---------------------------------------------------------------------------


def _assert_no_inference_fields(mapping: dict, *, label: str) -> None:
    present = [key for key in _INFERENCE_FIELDS if key in mapping]
    assert not present, f"{label} unexpectedly exposes inference fields: {present}"


def test_search_clinical_trials_records_do_not_expose_inference_fields(monkeypatch):
    class FakeClient:
        def search_studies(self, **kwargs):
            return {
                "studies": [
                    {
                        "protocolSection": {
                            "identificationModule": {"nctId": "NCT9999", "briefTitle": "Trial"},
                            "sponsorCollaboratorsModule": {"leadSponsor": {"name": "Acme Pharma"}},
                            "statusModule": {"overallStatus": "RECRUITING", "hasResults": False},
                            "designModule": {"phases": ["PHASE2"]},
                            "armsInterventionsModule": {"interventions": [{"name": "test drug"}]},
                            "conditionsModule": {"conditions": ["NSCLC"]},
                        }
                    }
                ]
            }

    monkeypatch.setattr(
        "src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient",
        lambda: FakeClient(),
    )

    result = TOOL_REGISTRY["search_clinical_trials_by_indication"]("NSCLC")

    assert "error" not in result
    assert result["trials"]
    trial = result["trials"][0]
    _assert_no_inference_fields(trial, label="clinical trial record")
    _assert_no_inference_fields(result["query_metadata"], label="search_clinical_trials_by_indication.query_metadata")


def test_compare_companies_by_indication_does_not_expose_inference_fields(monkeypatch):
    def fake_search_clinical_trials_by_indication(indication, **kwargs):
        sponsor = kwargs.get("sponsor")
        return {
            "trials": [
                {
                    "trial_id": "NCT00000001",
                    "title": "Mock trial",
                    "sponsor": sponsor or "Acme Pharma",
                    "phase": "PHASE2",
                    "status": "RECRUITING",
                    "last_update_date": "2026-01-02",
                    "official_url": "https://clinicaltrials.gov/study/NCT00000001",
                    "intervention_names": ["test drug"],
                    "product_modality": ["small_molecule"],
                    "results_available": False,
                }
            ],
            "query_metadata": {"known_limitations": []},
        }

    monkeypatch.setattr(
        tools_clinical_trials,
        "search_clinical_trials_by_indication",
        fake_search_clinical_trials_by_indication,
    )

    result = TOOL_REGISTRY["compare_companies_by_indication"](
        indication="NSCLC",
        companies=["Acme Pharma"],
    )

    assert "error" not in result
    item = result["company_comparison"][0]
    _assert_no_inference_fields(item, label="company_comparison item")
    _assert_no_inference_fields(item["phase_distribution"], label="phase_distribution")
    _assert_no_inference_fields(item["status_distribution"], label="status_distribution")
    _assert_no_inference_fields(result["query_metadata"], label="compare_companies_by_indication.query_metadata")
    _assert_no_inference_fields(
        result["landscape_summary"], label="compare_companies_by_indication.landscape_summary"
    )

    for key_trial in item["key_trials"]:
        _assert_no_inference_fields(key_trial, label="key_trials entry")
        assert key_trial["association_basis"] in {
            "sponsor_name_match",
            "returned_by_clinicaltrials_gov_query_requires_manual_review",
        }


# ---------------------------------------------------------------------------
# 5. Conservative known-limitation language on compare_companies_by_indication
# ---------------------------------------------------------------------------


def test_compare_companies_by_indication_carries_conservative_limitations(monkeypatch):
    def fake_search_clinical_trials_by_indication(indication, **kwargs):
        sponsor = kwargs.get("sponsor")
        return {
            "trials": [
                {
                    "trial_id": "NCT-A",
                    "title": "Sponsor match",
                    "sponsor": sponsor,
                    "phase": "PHASE3",
                    "status": "COMPLETED",
                    "last_update_date": "2026-01-02",
                    "official_url": "https://clinicaltrials.gov/study/NCT-A",
                    "intervention_names": ["test drug"],
                    "product_modality": ["small_molecule"],
                    "results_available": False,
                },
                {
                    "trial_id": "NCT-B",
                    "title": "Manual review record",
                    "sponsor": "Other Sponsor",
                    "phase": "PHASE2",
                    "status": "RECRUITING",
                    "last_update_date": "2026-01-03",
                    "official_url": "https://clinicaltrials.gov/study/NCT-B",
                    "intervention_names": ["test drug"],
                    "product_modality": ["small_molecule"],
                    "results_available": False,
                },
            ],
            "query_metadata": {"known_limitations": []},
        }

    monkeypatch.setattr(
        tools_clinical_trials,
        "search_clinical_trials_by_indication",
        fake_search_clinical_trials_by_indication,
    )

    result = TOOL_REGISTRY["compare_companies_by_indication"](
        indication="NSCLC",
        companies=["Acme Pharma"],
    )

    assert "error" not in result
    item = result["company_comparison"][0]
    company_limitations = " ".join(item["known_limitations"])
    data_gaps = " ".join(result["landscape_summary"]["data_gaps"])

    assert "clinical success" in company_limitations
    assert "regulatory approval probability" in company_limitations
    assert "commercial strength" in company_limitations
    assert "confirmed product ownership" in company_limitations

    assert "does not infer corporate family relationships" in data_gaps
    assert "sponsor identity and product ownership require manual review" in data_gaps
    assert "does not rank company superiority" in data_gaps

    summary = item["summary"]
    assert "should not be interpreted as clinical superiority" in summary
    assert "approval probability" in summary
    assert "confirmed product ownership" in summary
