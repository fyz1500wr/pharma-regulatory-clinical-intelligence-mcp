import hashlib

from src.mcp_server.server import TOOL_REGISTRY


def test_get_regulatory_document_detail_fda_by_record_id(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return [
                {
                    "id": "fda-detail-1",
                    "title": "FDA Detail Guidance",
                    "official_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/fda-detail-guidance",
                    "publication_date": "2026-01-01",
                    "last_update_date": None,
                    "source_type": "FDA_GUIDANCE",
                    "document_type": "guidance",
                    "document_status": "final",
                    "product_modality": ["drug"],
                    "topics": ["quality"],
                    "summary": "FDA detail test record.",
                    "known_limitations": [],
                }
            ]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"](document_id="fda-detail-1", agency="FDA")

    assert "document" in result
    assert "query_metadata" in result
    assert result["document"]["id"] == "fda-detail-1"
    assert result["document"]["agency"] == "FDA"
    assert result["document"]["title"] == "FDA Detail Guidance"
    assert result["document"]["document_type"] == "guidance"
    assert result["document"]["document_status"] == "final"
    assert result["document"]["official_url"].startswith("https://www.fda.gov/")
    assert result["document"]["impact_assessment"]["impact_level"] == "unknown"
    assert result["query_metadata"]["lookup_mode"] == "skeleton_backed_search_metadata"


def test_get_regulatory_document_detail_tfda_by_official_url(monkeypatch):
    official_url = "https://www.fda.gov.tw/TC/newsContent.aspx?id=100"

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return [
                {
                    "id": "tfda-detail-1",
                    "title": "TFDA Detail Update",
                    "official_url": official_url,
                    "publication_date": "2026-01-15",
                    "last_update_date": None,
                    "source_type": "TFDA_HTML",
                    "document_type": "regulatory_update",
                    "document_status": "published",
                    "product_modality": ["drug"],
                    "topics": ["藥品公告"],
                    "summary": "TFDA detail test record.",
                    "known_limitations": [],
                }
            ]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"](document_id=official_url, agency="TFDA")

    assert result["document"]["id"] == "tfda-detail-1"
    assert result["document"]["agency"] == "TFDA"
    assert result["document"]["official_url"] == official_url
    assert result["document"]["source_type"] == "TFDA_HTML"
    assert result["query_metadata"]["agencies_checked"] == ["TFDA"]


def test_get_regulatory_document_detail_searches_all_mvp_v1_agencies(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return []

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return [
                {
                    "id": "tfda-all-agencies-1",
                    "title": "TFDA All Agencies Detail",
                    "official_url": "https://www.fda.gov.tw/TC/newsContent.aspx?id=200",
                    "publication_date": "2026-02-01",
                    "last_update_date": None,
                    "source_type": "TFDA_HTML",
                    "document_type": "regulatory_update",
                    "document_status": "published",
                    "product_modality": ["drug"],
                    "topics": ["藥品公告"],
                    "summary": "TFDA all-agencies detail test record.",
                    "known_limitations": [],
                }
            ]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"](document_id="tfda-all-agencies-1")

    assert result["document"]["id"] == "tfda-all-agencies-1"
    assert result["document"]["agency"] == "TFDA"
    assert result["query_metadata"]["agencies_checked"] == ["FDA", "TFDA"]


def test_get_regulatory_document_detail_not_found_returns_structured_error(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return []

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"](
        document_id="missing-document",
        agency="FDA",
    )

    assert result["error"]["code"] == "NO_RESULTS"
    assert "missing-document" in result["error"]["message"]
    assert "suggested_next_action" in result["error"]


def test_get_regulatory_document_detail_rejects_missing_document_id():
    result = TOOL_REGISTRY["get_regulatory_document_detail"](document_id="")

    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_get_regulatory_document_detail_rejects_unsupported_agency():
    result = TOOL_REGISTRY["get_regulatory_document_detail"](
        document_id="demo",
        agency="EMA",
    )

    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_get_regulatory_document_detail_rejects_source_types_without_agency():
    result = TOOL_REGISTRY["get_regulatory_document_detail"](
        document_id="demo",
        source_types=["FDA_GUIDANCE"],
    )

    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_get_regulatory_document_detail_handles_source_unavailable(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            raise RuntimeError("FDA timeout")

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"](
        document_id="fda-detail-1",
        agency="FDA",
    )

    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"
    assert "FDA timeout" in result["error"]["message"]


def test_get_regulatory_document_detail_handles_unexpected_connector_shape(monkeypatch):
    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return {"unexpected": []}

    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"](
        document_id="tfda-detail-1",
        agency="TFDA",
    )

    assert result["error"]["code"] == "INTERNAL_ERROR"

def test_get_regulatory_document_detail_content_hash_lookup_does_not_filter_by_document_id_query(monkeypatch):
    title = "FDA Hash Detail Guidance"
    official_url = "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/fda-hash-detail-guidance"
    publication_date = "2026-03-01"
    expected_hash = hashlib.sha1(f"{title}|{official_url}|{publication_date}".encode("utf-8")).hexdigest()

    class FakeFDAClient:
        def search_updates(self, **kwargs):
            assert kwargs["query"] is None
            return [
                {
                    "id": "fda-hash-detail-1",
                    "title": title,
                    "official_url": official_url,
                    "publication_date": publication_date,
                    "last_update_date": None,
                    "source_type": "FDA_GUIDANCE",
                    "document_type": "guidance",
                    "document_status": "final",
                    "product_modality": ["drug"],
                    "topics": ["quality"],
                    "summary": "FDA hash detail test record.",
                    "known_limitations": [],
                }
            ]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"](
        document_id=expected_hash,
        agency="FDA",
    )

    assert result["document"]["id"] == "fda-hash-detail-1"
    assert result["document"]["content_hash"] == expected_hash
    assert result["query_metadata"]["lookup_mode"] == "skeleton_backed_search_metadata"


def test_get_regulatory_document_detail_all_agency_lookup_continues_after_fda_failure(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            raise RuntimeError("FDA transient failure")

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return [
                {
                    "id": "tfda-after-fda-failure-1",
                    "title": "TFDA After FDA Failure Detail",
                    "official_url": "https://www.fda.gov.tw/TC/newsContent.aspx?id=300",
                    "publication_date": "2026-03-15",
                    "last_update_date": None,
                    "source_type": "TFDA_HTML",
                    "document_type": "regulatory_update",
                    "document_status": "published",
                    "product_modality": ["drug"],
                    "topics": ["藥品公告"],
                    "summary": "TFDA detail found after FDA failure.",
                    "known_limitations": [],
                }
            ]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"](
        document_id="tfda-after-fda-failure-1",
    )

    assert result["document"]["id"] == "tfda-after-fda-failure-1"
    assert result["document"]["agency"] == "TFDA"
    assert result["query_metadata"]["agencies_checked"] == ["FDA", "TFDA"]
    assert result["query_metadata"]["partial_lookup_failures"][0]["agency"] == "FDA"
    assert result["query_metadata"]["partial_lookup_failures"][0]["code"] == "SOURCE_UNAVAILABLE"


def test_get_regulatory_document_detail_all_agency_lookup_returns_partial_results_when_one_source_fails_and_no_match(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            raise RuntimeError("FDA transient failure")

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return []

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"](
        document_id="missing-after-partial-failure",
    )

    assert result["error"]["code"] == "PARTIAL_RESULTS"
    assert result["error"]["details"]["partial_lookup_failures"][0]["agency"] == "FDA"


def test_get_regulatory_document_detail_all_agency_lookup_returns_source_unavailable_when_all_sources_fail(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            raise RuntimeError("FDA transient failure")

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            raise RuntimeError("TFDA transient failure")

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"](
        document_id="missing-after-total-failure",
    )

    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"
    assert len(result["error"]["details"]["partial_lookup_failures"]) == 2

def test_get_regulatory_document_detail_all_agency_lookup_preserves_internal_error_when_all_sources_return_unexpected_shapes(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return {"unexpected": "fda-shape"}

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return {"unexpected": "tfda-shape"}

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"](
        document_id="missing-after-internal-errors",
    )

    assert result["error"]["code"] == "INTERNAL_ERROR"
    assert len(result["error"]["details"]["partial_lookup_failures"]) == 2
    assert {failure["code"] for failure in result["error"]["details"]["partial_lookup_failures"]} == {"INTERNAL_ERROR"}


def test_get_regulatory_document_detail_all_agency_lookup_preserves_internal_error_when_failures_are_mixed(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return {"unexpected": "fda-shape"}

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            raise RuntimeError("TFDA transient failure")

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"](
        document_id="missing-after-mixed-failures",
    )

    assert result["error"]["code"] == "INTERNAL_ERROR"
    assert {failure["code"] for failure in result["error"]["details"]["partial_lookup_failures"]} == {
        "INTERNAL_ERROR",
        "SOURCE_UNAVAILABLE",
    }
