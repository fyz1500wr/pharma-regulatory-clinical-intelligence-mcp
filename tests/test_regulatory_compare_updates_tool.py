from src.mcp_server.server import TOOL_REGISTRY


def _fda_record(record_id="fda-compare-1", title="FDA Quality Guidance", topics=None, product_modality=None):
    return {
        "id": record_id,
        "title": title,
        "official_url": f"https://www.fda.gov/regulatory-information/search-fda-guidance-documents/{record_id}",
        "publication_date": "2026-01-01",
        "last_update_date": None,
        "source_type": "FDA_GUIDANCE",
        "document_type": "guidance",
        "document_status": "final",
        "product_modality": product_modality or ["drug"],
        "topics": topics or ["quality"],
        "summary": f"{title} summary.",
        "known_limitations": [],
    }


def _tfda_record(record_id="tfda-compare-1", title="TFDA Quality Update", topics=None, product_modality=None):
    return {
        "id": record_id,
        "title": title,
        "official_url": f"https://www.fda.gov.tw/TC/newsContent.aspx?id={record_id}",
        "publication_date": "2026-01-15",
        "last_update_date": None,
        "source_type": "TFDA_HTML",
        "document_type": "regulatory_update",
        "document_status": "published",
        "product_modality": product_modality or ["drug"],
        "topics": topics or ["quality"],
        "summary": f"{title} summary.",
        "known_limitations": [],
    }


def test_compare_regulatory_updates_by_agency_summarizes_fda_and_tfda(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            assert kwargs["query"] == "quality"
            return [_fda_record()]

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            assert kwargs["query"] == "quality"
            return [_tfda_record()]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = TOOL_REGISTRY["compare_regulatory_updates"](
        agencies=["FDA", "TFDA"],
        comparison_axis="agency",
        query="quality",
    )

    assert "comparison" in result
    assert "comparison_summary" in result
    by_agency = {entry["agency"]: entry for entry in result["comparison"]}
    assert by_agency["FDA"]["record_count"] == 1
    assert by_agency["TFDA"]["record_count"] == 1
    assert by_agency["FDA"]["key_updates"][0]["id"] == "fda-compare-1"
    assert by_agency["TFDA"]["key_updates"][0]["id"] == "tfda-compare-1"
    assert result["query_metadata"]["comparison_axis"] == "agency"


def test_compare_regulatory_updates_rejects_out_of_scope_agency():
    result = TOOL_REGISTRY["compare_regulatory_updates"](
        agencies=["FDA", "EMA"],
        comparison_axis="agency",
    )

    assert result["error"]["code"] == "INVALID_PARAMETER"
    assert "EMA" in result["error"]["message"]


def test_compare_regulatory_updates_rejects_unsupported_axis():
    result = TOOL_REGISTRY["compare_regulatory_updates"](
        agencies=["FDA"],
        comparison_axis="region",
    )

    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_compare_regulatory_updates_filters_by_topic_and_groups_by_topic(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return [
                _fda_record(record_id="fda-quality", title="FDA Quality Guidance", topics=["quality"]),
                _fda_record(record_id="fda-clinical", title="FDA Clinical Guidance", topics=["clinical"]),
            ]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())

    result = TOOL_REGISTRY["compare_regulatory_updates"](
        agencies=["FDA"],
        comparison_axis="topic",
        topics=["quality"],
    )

    assert len(result["comparison"]) == 1
    assert result["comparison"][0]["comparison_value"] == "quality"
    assert result["comparison"][0]["record_count"] == 1
    assert result["comparison"][0]["key_updates"][0]["id"] == "fda-quality"


def test_compare_regulatory_updates_continues_after_partial_source_failure(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            raise RuntimeError("FDA transient failure")

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return [_tfda_record(record_id="tfda-after-failure")]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = TOOL_REGISTRY["compare_regulatory_updates"](
        agencies=["FDA", "TFDA"],
        comparison_axis="agency",
    )

    assert "comparison" in result
    assert result["query_metadata"]["successful_agencies"] == ["TFDA"]
    assert result["query_metadata"]["partial_lookup_failures"][0]["agency"] == "FDA"
    assert result["comparison"][0]["agency"] == "TFDA"
    assert result["comparison"][0]["record_count"] == 1


def test_compare_regulatory_updates_returns_source_unavailable_when_all_sources_fail(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            raise RuntimeError("FDA transient failure")

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            raise RuntimeError("TFDA transient failure")

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = TOOL_REGISTRY["compare_regulatory_updates"](
        agencies=["FDA", "TFDA"],
    )

    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"


def test_compare_regulatory_updates_preserves_internal_error_when_all_sources_return_unexpected_shapes(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return {"unexpected": "fda"}

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return {"unexpected": "tfda"}

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = TOOL_REGISTRY["compare_regulatory_updates"](
        agencies=["FDA", "TFDA"],
    )

    assert result["error"]["code"] == "INTERNAL_ERROR"


def test_compare_regulatory_updates_returns_zero_count_entries_when_no_records_match(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return []

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return []

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = TOOL_REGISTRY["compare_regulatory_updates"](
        agencies=["FDA", "TFDA"],
        comparison_axis="agency",
        topics=["quality"],
    )

    assert [entry["agency"] for entry in result["comparison"]] == ["FDA", "TFDA"]
    assert [entry["record_count"] for entry in result["comparison"]] == [0, 0]
    assert "Relax filters" in result["comparison_summary"]["recommended_follow_up"][0]
