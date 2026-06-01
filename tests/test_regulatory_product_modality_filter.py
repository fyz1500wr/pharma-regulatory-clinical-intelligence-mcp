from __future__ import annotations

import inspect


def _fda_records():
    return [
        {
            "id": "fda-antibody-1",
            "title": "Monoclonal antibody development guidance",
            "publication_date": "2026-01-10",
            "last_update_date": "2026-01-10",
            "official_url": "https://www.fda.gov/example-antibody",
            "source_type": "FDA_GUIDANCE",
            "document_type": "guidance",
            "document_status": "final",
            "product_modality": ["antibody"],
            "topics": ["CMC"],
            "summary": "Guidance for monoclonal antibody development.",
        },
        {
            "id": "fda-gene-therapy-1",
            "title": "Gene therapy CMC guidance",
            "publication_date": "2026-01-15",
            "last_update_date": "2026-01-15",
            "official_url": "https://www.fda.gov/example-gene-therapy",
            "source_type": "FDA_GUIDANCE",
            "document_type": "guidance",
            "document_status": "final",
            "product_modality": ["gene_therapy"],
            "topics": ["CMC"],
            "summary": "Guidance for gene therapy products.",
        },
    ]


class _FDAClient:
    def search_updates(self, query=None, source_types=None, limit=20):
        return _fda_records()[:limit]


def test_search_regulatory_updates_accepts_product_modality_string(monkeypatch):
    from src.mcp_server import tools_regulatory

    monkeypatch.setattr(tools_regulatory, "FDAUpdatesClient", lambda: _FDAClient())

    result = tools_regulatory.search_regulatory_updates(
        agency="FDA",
        product_modality="antibody",
        limit=10,
    )

    assert "error" not in result
    assert [record["id"] for record in result["records"]] == ["fda-antibody-1"]
    assert result["query_metadata"]["filters_applied"]["product_modality"] == ["antibody"]
    assert any("Product modality filtering is based on MVP" in item for item in result["known_limitations"])


def test_search_regulatory_updates_accepts_product_modality_list(monkeypatch):
    from src.mcp_server import tools_regulatory

    monkeypatch.setattr(tools_regulatory, "FDAUpdatesClient", lambda: _FDAClient())

    result = tools_regulatory.search_regulatory_updates(
        agency="FDA",
        product_modality=["antibody", "gene_therapy"],
        limit=10,
    )

    assert "error" not in result
    assert {record["id"] for record in result["records"]} == {"fda-antibody-1", "fda-gene-therapy-1"}
    assert result["query_metadata"]["filters_applied"]["product_modality"] == ["antibody", "gene_therapy"]


def test_search_regulatory_updates_rejects_invalid_product_modality():
    from src.mcp_server import tools_regulatory

    result = tools_regulatory.search_regulatory_updates(
        agency="FDA",
        product_modality="biologic_type",
    )

    assert result["error"]["code"] == "INVALID_PARAMETER"
    assert "Unsupported product_modality" in result["error"]["message"]


def test_search_regulatory_updates_product_modality_no_result(monkeypatch):
    from src.mcp_server import tools_regulatory

    monkeypatch.setattr(tools_regulatory, "FDAUpdatesClient", lambda: _FDAClient())

    result = tools_regulatory.search_regulatory_updates(
        agency="FDA",
        product_modality="cell_therapy",
        limit=10,
    )

    assert result["records"] == []
    assert result["no_result_reason"] == "NO_MATCHING_RECORDS"
    assert result["query_metadata"]["filters_applied"]["product_modality"] == ["cell_therapy"]
    assert any("manual verification" in item for item in result["known_limitations"])


def test_stdio_search_regulatory_updates_exposes_and_forwards_product_modality(monkeypatch):
    from src.mcp_server import stdio_server

    calls = {}

    def fake_call_tool(tool_name, **kwargs):
        calls["tool_name"] = tool_name
        calls["kwargs"] = kwargs
        return {"records": [], "query_metadata": {"filters_applied": kwargs}}

    monkeypatch.setattr(stdio_server, "_call_tool", fake_call_tool)

    signature = inspect.signature(stdio_server.search_regulatory_updates)
    assert "product_modality" in signature.parameters

    result = stdio_server.search_regulatory_updates(
        agency="FDA",
        query="guidance",
        product_modality=["antibody"],
    )

    assert result["records"] == []
    assert calls["tool_name"] == "search_regulatory_updates"
    assert calls["kwargs"]["product_modality"] == ["antibody"]
