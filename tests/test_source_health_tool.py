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
    assert result["query_metadata"]["sources_checked"] == ["FDA", "TFDA", "ClinicalTrials.gov"]
    assert len(result["sources"]) == 3
    assert len(result["source_health"]) == 3
    assert all(item["status"] == "pass" for item in result["source_health"])


def test_check_source_health_accepts_contract_sources_list(monkeypatch):
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

    result = _check_source_health(sources=["TFDA", "ClinicalTrials.gov"])

    assert result["overall_status"] == "available"
    assert result["query_metadata"]["sources_checked"] == ["TFDA", "ClinicalTrials.gov"]
    assert [item["agency_or_registry"] for item in result["source_health"]] == ["TFDA", "ClinicalTrials.gov"]


def test_check_source_health_single_tfda_available_legacy_source_param(monkeypatch):
    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return [{"id": "tfda-ok"}]

    monkeypatch.setattr("src.mcp_server.tools_source_health.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = _check_source_health(source="TFDA")

    assert result["overall_status"] == "available"
    assert result["query_metadata"]["sources_checked"] == ["TFDA"]
    assert result["sources"][0]["source"] == "TFDA"
    assert result["source_health"][0]["source_id"] == "TFDA_connector"
    assert result["source_health"][0]["status"] == "pass"


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

    result = _check_source_health(source="FDA")

    assert result["overall_status"] == "degraded"
    assert result["sources"][0]["available"] is False
    assert result["source_health"][0]["status"] == "failed"
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

    result = _check_source_health(source="ClinicalTrials.gov")

    assert result["overall_status"] == "degraded"
    assert result["sources"][0]["source"] == "ClinicalTrials.gov"
    assert result["source_health"][0]["source_id"] == "ClinicalTrialsGov_API"
    assert result["source_health"][0]["status"] == "failed"
    assert result["source_health"][0]["failure_type"] == "api_status"


def test_check_source_health_handles_connector_exception(monkeypatch):
    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            raise RuntimeError("TFDA timeout")

    monkeypatch.setattr("src.mcp_server.tools_source_health.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = _check_source_health(source="TFDA")

    assert result["overall_status"] == "degraded"
    assert result["sources"][0]["available"] is False
    assert result["source_health"][0]["status"] == "failed"
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
    assert result["source_health"][0]["agency_or_registry"] == "ClinicalTrials.gov"
