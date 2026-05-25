from src.mcp_server.server import TOOL_REGISTRY
from src.mcp_server.tools_clinical_trials import search_clinical_trials_by_indication
from src.mcp_server.tools_regulatory import compare_regulatory_updates


def test_required_tool_names_exist():
    required = {
        "search_regulatory_updates", "get_regulatory_document_detail", "search_clinical_trials_by_indication",
        "check_source_health", "list_source_failures", "generate_regulatory_digest",
        "compare_regulatory_updates", "compare_companies_by_indication",
    }
    assert required.issubset(set(TOOL_REGISTRY.keys()))


def test_compare_regulatory_updates_structured_error():
    result = compare_regulatory_updates()
    assert "error" in result
    assert result["error"]["code"] == "DATA_NOT_INGESTED"


def test_mcp_search_clinical_trials_by_indication_handles_empty_results(monkeypatch):
    class FakeClient:
        def search_studies(self, **kwargs):
            return {"studies": []}

    monkeypatch.setattr("src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient", lambda: FakeClient())
    result = search_clinical_trials_by_indication("NSCLC")
    assert result["trials"] == []
    assert result["no_result_reason"] == "NO_MATCHING_RECORDS"


def test_mcp_search_clinical_trials_by_indication_trims_indication(monkeypatch):
    captured = {}

    class FakeClient:
        def search_studies(self, **kwargs):
            captured["indication"] = kwargs["indication"]
            return {"studies": []}

    monkeypatch.setattr("src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient", lambda: FakeClient())
    result = search_clinical_trials_by_indication("  NSCLC  ")
    assert captured["indication"] == "NSCLC"
    assert result["query_metadata"]["indication"] == "NSCLC"
