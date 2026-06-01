from src.mcp_server.server import TOOL_REGISTRY


def _check_source_health(**kwargs):
    return TOOL_REGISTRY["check_source_health"](**kwargs)


def test_check_source_health_all_sources_available_through_registry(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return [{"id": "fda-ok"}]

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return [{"id": "tfda-ok"}]

    class FakeClinicalTrialsGovClient:
        def search_studies(self, **kwargs):
            return {"studies": [{"protocolSection": {}}]}

    monkeypatch.setattr("src.mcp_server.tools_source_health.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_source_health.TFDAUpdatesClient", lambda: FakeTFDAClient())
    monkeypatch.setattr(
        "src.mcp_server.tools_source_health.ClinicalTrialsGovClient",
        lambda: FakeClinicalTrialsGovClient(),
    )

    result = _check_source_health()

    assert result["overall_status"] == "available"
    assert result["query_metadata"]["sources_checked"] == [
        "FDA_openFDA",
        "TFDA_DataAction",
        "ClinicalTrialsGov_API",
    ]
    assert result["query_metadata"]["internal_sources_checked"] == ["FDA", "TFDA", "ClinicalTrials.gov"]
    assert len(result["sources"]) == 3
    assert len(result["source_health"]) == 3
    assert all(item["status"] == "pass" for item in result["source_health"])
    assert all(item["source_type"] == "API" for item in result["source_health"])


def test_check_source_health_accepts_contract_source_ids_list(monkeypatch):
    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return [{"id": "tfda-ok"}]

    class FakeClinicalTrialsGovClient:
        def search_studies(self, **kwargs):
            return {"studies": [{"protocolSection": {}}]}

    monkeypatch.setattr("src.mcp_server.tools_source_health.TFDAUpdatesClient", lambda: FakeTFDAClient())
    monkeypatch.setattr(
        "src.mcp_server.tools_source_health.ClinicalTrialsGovClient",
        lambda: FakeClinicalTrialsGovClient(),
    )

    result = _check_source_health(sources=["TFDA_DataAction", "ClinicalTrialsGov_API"])

    assert result["overall_status"] == "available"
    assert result["query_metadata"]["sources_checked"] == ["TFDA_DataAction", "ClinicalTrialsGov_API"]
    assert result["query_metadata"]["internal_sources_checked"] == ["TFDA", "ClinicalTrials.gov"]
    assert [item["source_id"] for item in result["source_health"]] == ["TFDA_DataAction", "ClinicalTrialsGov_API"]
    assert [item["agency_or_registry"] for item in result["source_health"]] == ["TFDA", "ClinicalTrials.gov"]
    assert all(item["source_type"] == "API" for item in result["source_health"])


def test_check_source_health_accepts_legacy_sources_list(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return [{"id": "fda-ok"}]

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return [{"id": "tfda-ok"}]

    monkeypatch.setattr("src.mcp_server.tools_source_health.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_source_health.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = _check_source_health(sources=["FDA", "TFDA"])

    assert result["overall_status"] == "available"
    assert result["query_metadata"]["sources_checked"] == ["FDA_openFDA", "TFDA_DataAction"]
    assert result["query_metadata"]["internal_sources_checked"] == ["FDA", "TFDA"]
    assert [item["source_id"] for item in result["source_health"]] == ["FDA_openFDA", "TFDA_DataAction"]


def test_check_source_health_single_tfda_available_legacy_source_param(monkeypatch):
    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return [{"id": "tfda-ok"}]

    monkeypatch.setattr("src.mcp_server.tools_source_health.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = _check_source_health(source="TFDA")

    assert result["overall_status"] == "available"
    assert result["query_metadata"]["sources_checked"] == ["TFDA_DataAction"]
    assert result["query_metadata"]["internal_sources_checked"] == ["TFDA"]
    assert result["sources"][0]["source"] == "TFDA"
    assert result["source_health"][0]["source_id"] == "TFDA_DataAction"
    assert result["source_health"][0]["source_type"] == "API"
    assert result["source_health"][0]["status"] == "pass"


def test_check_source_health_single_fda_contract_id(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return [{"id": "fda-ok"}]

    monkeypatch.setattr("src.mcp_server.tools_source_health.FDAUpdatesClient", lambda: FakeFDAClient())

    result = _check_source_health(source="FDA_openFDA")

    assert result["overall_status"] == "available"
    assert result["query_metadata"]["sources_checked"] == ["FDA_openFDA"]
    assert result["query_metadata"]["internal_sources_checked"] == ["FDA"]
    assert result["source_health"][0]["source_id"] == "FDA_openFDA"
    assert result["source_health"][0]["agency_or_registry"] == "FDA"
    assert result["source_health"][0]["source_type"] == "API"


def test_check_source_health_regulatory_error_response(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return {
                "error": {
                    "code": "SOURCE_UNAVAILABLE",
                    "message": "FDA unavailable",
                    "suggested_next_action": "Retry later.",
                }
            }

    monkeypatch.setattr("src.mcp_server.tools_source_health.FDAUpdatesClient", lambda: FakeFDAClient())

    result = _check_source_health(source="FDA_openFDA")

    assert result["overall_status"] == "degraded"
    assert result["sources"][0]["available"] is False
    assert result["source_health"][0]["status"] == "failed"
    assert result["source_health"][0]["failure_type"] == "api_status"
    assert result["source_health"][0]["error_message"] == "FDA unavailable"
    assert result["source_health"][0]["suggested_fix"] == "Retry later."


def test_check_source_health_clinicaltrials_error_response(monkeypatch):
    class FakeClinicalTrialsGovClient:
        def search_studies(self, **kwargs):
            return {
                "error": {
                    "code": "SOURCE_UNAVAILABLE",
                    "message": "ClinicalTrials.gov unavailable",
                }
            }

    monkeypatch.setattr(
        "src.mcp_server.tools_source_health.ClinicalTrialsGovClient",
        lambda: FakeClinicalTrialsGovClient(),
    )

    result = _check_source_health(source="ClinicalTrialsGov_API")

    assert result["overall_status"] == "degraded"
    assert result["sources"][0]["source"] == "ClinicalTrials.gov"
    assert result["source_health"][0]["source_id"] == "ClinicalTrialsGov_API"
    assert result["source_health"][0]["source_type"] == "API"
    assert result["source_health"][0]["status"] == "failed"
    assert result["source_health"][0]["failure_type"] == "api_status"


def test_check_source_health_handles_connector_exception(monkeypatch):
    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            raise RuntimeError("TFDA timeout")

    monkeypatch.setattr("src.mcp_server.tools_source_health.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = _check_source_health(source="TFDA_DataAction")

    assert result["overall_status"] == "degraded"
    assert result["sources"][0]["available"] is False
    assert result["source_health"][0]["source_id"] == "TFDA_DataAction"
    assert result["source_health"][0]["status"] == "failed"
    assert result["source_health"][0]["failure_type"] == "api_status"
    assert "TFDA timeout" in result["source_health"][0]["error_message"]


def test_check_source_health_rejects_unsupported_source():
    result = _check_source_health(source="EMA")

    assert result["error"]["code"] == "INVALID_PARAMETER"
    assert "supported_sources" in result["error"]["details"]


def test_check_source_health_rejects_invalid_sources_shape():
    result = _check_source_health(sources=[123])

    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_check_source_health_rejects_source_and_sources_together():
    result = _check_source_health(source="FDA", sources=["TFDA"])

    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_check_source_health_accepts_clinicaltrials_alias(monkeypatch):
    class FakeClinicalTrialsGovClient:
        def search_studies(self, **kwargs):
            return {"studies": []}

    monkeypatch.setattr(
        "src.mcp_server.tools_source_health.ClinicalTrialsGovClient",
        lambda: FakeClinicalTrialsGovClient(),
    )

    result = _check_source_health(source="clinicaltrials")

    assert result["overall_status"] == "available"
    assert result["sources"][0]["source"] == "ClinicalTrials.gov"
    assert result["source_health"][0]["source_id"] == "ClinicalTrialsGov_API"
    assert result["source_health"][0]["agency_or_registry"] == "ClinicalTrials.gov"
    assert result["source_health"][0]["source_type"] == "API"



# --- egress policy classification tests ---
def test_check_source_health_classifies_egress_policy_via_exception_message(monkeypatch):
    from src.mcp_server import tools_source_health
    from src.mcp_server.tools_healthcheck import check_source_health

    class RaisingClient:
        def search_updates(self, limit=1):
            raise RuntimeError("403 Host not in allowlist")

    monkeypatch.setattr(tools_source_health, "TFDAUpdatesClient", lambda: RaisingClient())

    result = check_source_health(sources=["TFDA_DataAction"])
    item = result["source_health"][0]

    assert item["failure_type"] == "egress_policy"
    assert "allowlist" in item["suggested_fix"].lower()
    assert "Codespaces" in item["suggested_fix"]
    assert any("MUST NOT be interpreted as no matching records" in text for text in item["known_limitations"])


def test_check_source_health_classifies_egress_policy_via_error_details(monkeypatch):
    from src.mcp_server import tools_source_health
    from src.mcp_server.tools_healthcheck import check_source_health

    class ErrorClient:
        def search_updates(self, limit=1):
            return {
                "error": {
                    "code": "SOURCE_UNAVAILABLE",
                    "message": "upstream failed",
                    "details": {"reason": "Host not in allowlist"},
                }
            }

    monkeypatch.setattr(tools_source_health, "FDAUpdatesClient", lambda: ErrorClient())

    result = check_source_health(sources=["FDA_openFDA"])
    item = result["source_health"][0]

    assert item["failure_type"] == "egress_policy"
    assert item["error_details"]["reason"] == "Host not in allowlist"


def test_check_source_health_keeps_api_status_for_generic_unavailable(monkeypatch):
    from src.mcp_server import tools_source_health
    from src.mcp_server.tools_healthcheck import check_source_health

    class RaisingClient:
        def search_updates(self, limit=1):
            raise RuntimeError("TFDA timeout")

    monkeypatch.setattr(tools_source_health, "TFDAUpdatesClient", lambda: RaisingClient())

    result = check_source_health(sources=["TFDA_DataAction"])
    item = result["source_health"][0]

    assert item["failure_type"] == "api_status"
