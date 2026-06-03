from __future__ import annotations

from src.mcp_server import tools_regulatory


def test_search_regulatory_updates_agencies_tfda_does_not_call_fda(monkeypatch) -> None:
    captured = {}

    class FailingFDAClient:
        def __init__(self) -> None:
            raise AssertionError("FDA client should not be constructed for agencies=['TFDA']")

    class FakeTFDAClient:
        def search_updates(self, *, query, source_types, limit):
            captured["query"] = query
            captured["source_types"] = source_types
            captured["limit"] = limit
            return [
                {
                    "id": "tfda-001",
                    "title": "藥品查驗登記公告",
                    "publication_date": "2026-01-01",
                    "last_update_date": "2026-01-02",
                    "official_url": "https://www.fda.gov.tw/tc/newsContent.aspx?id=tfda-001",
                    "source_type": "TFDA_HTML",
                    "document_type": "regulatory_update",
                    "document_status": "published",
                    "product_modality": ["requires_manual_review"],
                    "topics": ["submission"],
                    "summary": "藥品查驗登記測試資料",
                }
            ]

    monkeypatch.setattr(tools_regulatory, "FDAUpdatesClient", FailingFDAClient)
    monkeypatch.setattr(tools_regulatory, "TFDAUpdatesClient", FakeTFDAClient)

    result = tools_regulatory.search_regulatory_updates(
        query="藥品 查驗登記",
        agencies=["TFDA"],
        date_range="1y",
        limit=5,
    )

    assert "error" not in result
    assert result["query_metadata"]["agency_searched"] == ["TFDA"]
    assert result["query_metadata"]["filters_applied"]["query"] == "藥品 查驗登記"
    assert result["query_metadata"]["filters_applied"]["limit"] == 5
    assert captured == {
        "query": "藥品 查驗登記",
        "source_types": ["TFDA_HTML"],
        "limit": 5,
    }
    assert len(result["records"]) == 1
    assert result["records"][0]["agency"] == "TFDA"


def test_search_regulatory_updates_rejects_multi_agency_list() -> None:
    result = tools_regulatory.search_regulatory_updates(
        query="oncology",
        agencies=["FDA", "TFDA"],
        limit=5,
    )

    assert result["error"]["code"] == "INVALID_PARAMETER"
    assert "exactly one agency" in result["error"]["message"]
    assert "compare_regulatory_updates" in result["error"]["suggested_next_action"]
