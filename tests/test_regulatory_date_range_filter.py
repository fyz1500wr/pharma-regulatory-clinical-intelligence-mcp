from __future__ import annotations

import inspect
from datetime import datetime as real_datetime
from datetime import timezone


def _records():
    return [
        {
            "id": "recent-antibody",
            "title": "Recent antibody guidance",
            "publication_date": "2026-05-01",
            "last_update_date": "2026-05-01",
            "official_url": "https://www.fda.gov/recent-antibody",
            "source_type": "FDA_GUIDANCE",
            "document_type": "guidance",
            "document_status": "final",
            "product_modality": ["antibody"],
            "topics": ["CMC"],
            "summary": "Recent antibody record.",
        },
        {
            "id": "old-antibody",
            "title": "Old antibody guidance",
            "publication_date": "2024-01-01",
            "last_update_date": "2024-01-01",
            "official_url": "https://www.fda.gov/old-antibody",
            "source_type": "FDA_GUIDANCE",
            "document_type": "guidance",
            "document_status": "final",
            "product_modality": ["antibody"],
            "topics": ["CMC"],
            "summary": "Old antibody record.",
        },
    ]


class _FDAClient:
    def search_updates(self, query=None, source_types=None, limit=20):
        return _records()[:limit]


class _FixedDateTime:
    @staticmethod
    def now(tz=None):
        return real_datetime(2026, 6, 1, tzinfo=timezone.utc)

    @staticmethod
    def fromisoformat(value):
        return real_datetime.fromisoformat(value)


def test_search_regulatory_updates_date_range_1y(monkeypatch):
    from src.mcp_server import tools_regulatory

    monkeypatch.setattr(tools_regulatory, "FDAUpdatesClient", lambda: _FDAClient())
    monkeypatch.setattr(tools_regulatory, "datetime", _FixedDateTime)

    result = tools_regulatory.search_regulatory_updates(
        agency="FDA",
        date_range="1y",
        limit=10,
    )

    assert "error" not in result
    assert [record["id"] for record in result["records"]] == ["recent-antibody"]

    filters = result["query_metadata"]["filters_applied"]
    assert filters["date_range"] == "1y"
    assert filters["date_from"] == "2025-06-01"
    assert filters["date_to"] == "2026-06-01"


def test_search_regulatory_updates_custom_date_range(monkeypatch):
    from src.mcp_server import tools_regulatory

    monkeypatch.setattr(tools_regulatory, "FDAUpdatesClient", lambda: _FDAClient())

    result = tools_regulatory.search_regulatory_updates(
        agency="FDA",
        date_range="custom",
        custom_date_range={"start_date": "2023-12-31", "end_date": "2024-01-02"},
        limit=10,
    )

    assert "error" not in result
    assert [record["id"] for record in result["records"]] == ["old-antibody"]

    filters = result["query_metadata"]["filters_applied"]
    assert filters["date_range"] == "custom"
    assert filters["custom_date_range"] == {"start_date": "2023-12-31", "end_date": "2024-01-02"}
    assert filters["date_from"] == "2023-12-31"
    assert filters["date_to"] == "2024-01-02"


def test_search_regulatory_updates_explicit_date_from_to_remain_supported(monkeypatch):
    from src.mcp_server import tools_regulatory

    monkeypatch.setattr(tools_regulatory, "FDAUpdatesClient", lambda: _FDAClient())

    result = tools_regulatory.search_regulatory_updates(
        agency="FDA",
        date_from="2024-01-01",
        date_to="2024-01-01",
        limit=10,
    )

    assert "error" not in result
    assert [record["id"] for record in result["records"]] == ["old-antibody"]

    filters = result["query_metadata"]["filters_applied"]
    assert filters["date_range"] is None
    assert filters["date_from"] == "2024-01-01"
    assert filters["date_to"] == "2024-01-01"


def test_search_regulatory_updates_rejects_invalid_date_range():
    from src.mcp_server import tools_regulatory

    result = tools_regulatory.search_regulatory_updates(
        agency="FDA",
        date_range="2y",
        limit=10,
    )

    assert result["error"]["code"] == "INVALID_PARAMETER"
    assert "date_range must be one of" in result["error"]["message"]


def test_search_regulatory_updates_rejects_ambiguous_date_inputs():
    from src.mcp_server import tools_regulatory

    result = tools_regulatory.search_regulatory_updates(
        agency="FDA",
        date_range="1y",
        date_from="2025-01-01",
        limit=10,
    )

    assert result["error"]["code"] == "INVALID_PARAMETER"
    assert "cannot be combined" in result["error"]["message"]


def test_stdio_search_regulatory_updates_exposes_and_forwards_date_range(monkeypatch):
    from src.mcp_server import stdio_server

    calls = {}

    def fake_call_tool(tool_name, **kwargs):
        calls["tool_name"] = tool_name
        calls["kwargs"] = kwargs
        return {"records": [], "query_metadata": {"filters_applied": kwargs}}

    monkeypatch.setattr(stdio_server, "_call_tool", fake_call_tool)

    signature = inspect.signature(stdio_server.search_regulatory_updates)
    assert "date_range" in signature.parameters
    assert "custom_date_range" in signature.parameters

    result = stdio_server.search_regulatory_updates(
        agency="FDA",
        query="guidance",
        product_modality=["antibody"],
        date_range="custom",
        custom_date_range={"start_date": "2026-01-01", "end_date": "2026-06-01"},
    )

    assert result["records"] == []
    assert calls["tool_name"] == "search_regulatory_updates"
    assert calls["kwargs"]["date_range"] == "custom"
    assert calls["kwargs"]["custom_date_range"] == {"start_date": "2026-01-01", "end_date": "2026-06-01"}
