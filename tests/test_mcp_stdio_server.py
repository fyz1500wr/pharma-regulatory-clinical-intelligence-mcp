from src.mcp_server import stdio_server
from src.mcp_server.server import TOOL_REGISTRY


EXPECTED_MVP_V1_TOOLS = {
    "search_regulatory_updates",
    "get_regulatory_document_detail",
    "compare_regulatory_updates",
    "search_clinical_trials_by_indication",
    "compare_companies_by_indication",
    "check_source_health",
    "list_source_failures",
    "generate_regulatory_digest",
}


def test_stdio_server_imports_without_running_transport():
    assert stdio_server.MCP_SERVER is not None
    assert callable(stdio_server.main)


def test_stdio_server_tool_names_match_registry():
    assert set(stdio_server.MCP_TOOL_NAMES) == set(TOOL_REGISTRY)
    assert set(stdio_server.MCP_TOOL_NAMES) == EXPECTED_MVP_V1_TOOLS


def test_stdio_wrapper_delegates_to_tool_registry(monkeypatch):
    calls = {}

    def fake_tool(**kwargs):
        calls["kwargs"] = kwargs
        return {"ok": True, "received": kwargs}

    monkeypatch.setitem(stdio_server.TOOL_REGISTRY, "search_regulatory_updates", fake_tool)

    result = stdio_server.search_regulatory_updates(
        agency="TFDA",
        query="cell therapy",
        limit=3,
    )

    assert result["ok"] is True
    assert calls["kwargs"]["agency"] == "TFDA"
    assert calls["kwargs"]["query"] == "cell therapy"
    assert calls["kwargs"]["limit"] == 3


def test_stdio_wrapper_check_source_health_delegates_to_tool_registry(monkeypatch):
    calls = {}

    def fake_tool(**kwargs):
        calls["kwargs"] = kwargs
        return {"overall_status": "available"}

    monkeypatch.setitem(stdio_server.TOOL_REGISTRY, "check_source_health", fake_tool)

    result = stdio_server.check_source_health(sources=["TFDA_DataAction"])

    assert result["overall_status"] == "available"
    assert calls["kwargs"]["sources"] == ["TFDA_DataAction"]
