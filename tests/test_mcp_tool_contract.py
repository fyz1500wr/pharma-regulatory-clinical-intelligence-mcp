from src.mcp_server.server import TOOL_REGISTRY
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
