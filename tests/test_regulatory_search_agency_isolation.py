from __future__ import annotations

from src.core.errors import ErrorCode, build_error
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


def test_compare_regulatory_updates_preserves_fda_blocked_source_as_limitation(monkeypatch) -> None:
    def fake_search_regulatory_updates(**kwargs):
        agency = kwargs["agency"]
        if agency == "FDA":
            return build_error(
                ErrorCode.SOURCE_UNAVAILABLE,
                "FDA search failed: BLOCKED_SOURCE runtime egress policy prevented validation",
                details={"status": "BLOCKED_SOURCE", "source": "FDA"},
                suggested_next_action="Run check_source_health before interpreting FDA coverage.",
            )
        if agency == "TFDA":
            return {
                "records": [],
                "no_result_reason": "NO_MATCHING_RECORDS",
                "query_metadata": {
                    "agency_searched": ["TFDA"],
                    "filters_applied": {"query": kwargs.get("query")},
                },
                "known_limitations": ["TFDA returned no normalized records for the selected filters."],
            }
        raise AssertionError(f"Unexpected agency: {agency}")

    monkeypatch.setattr(tools_regulatory, "search_regulatory_updates", fake_search_regulatory_updates)

    result = tools_regulatory.compare_regulatory_updates(
        agencies=["FDA", "TFDA"],
        query="oncology",
        date_range="1y",
        limit=5,
    )

    assert "error" not in result
    assert result["query_metadata"]["agencies_checked"] == ["FDA", "TFDA"]
    assert result["query_metadata"]["successful_agencies"] == ["TFDA"]

    failures = result["query_metadata"]["partial_lookup_failures"]
    assert len(failures) == 1
    assert failures[0]["agency"] == "FDA"
    assert failures[0]["code"] == ErrorCode.SOURCE_UNAVAILABLE.value
    assert "BLOCKED_SOURCE" in failures[0]["message"]
    assert failures[0]["details"]["status"] == "BLOCKED_SOURCE"

    assert [entry["comparison_value"] for entry in result["comparison"]] == ["TFDA"]
    assert result["comparison"][0]["record_count"] == 0
    assert "no matching normalized updates" in result["comparison"][0]["agency_specific_notes"][0]

    major_differences = " ".join(result["comparison_summary"]["major_differences"])
    assert "TFDA: 0 matching update(s)" in major_differences
    assert "FDA: 0 matching update(s)" not in major_differences

    follow_up = " ".join(result["comparison_summary"]["recommended_follow_up"])
    assert "source failure" in follow_up
    assert "manual regulatory review" in follow_up
