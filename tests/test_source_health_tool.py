from src.mcp_server.tools_source_health import check_source_health


def test_check_source_health_all_sources_available(monkeypatch):
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

    result = check_source_health()

    assert result["overall_status"] == "available"
    assert result["query_metadata"]["sources_checked"] == ["FDA", "TFDA", "ClinicalTrials.gov"]
    assert len(result["sources"]) == 3
    assert all(item["available"] for item in result["sources"])


def test_check_source_health_single_tfda_available(monkeypatch):
    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return [{"id": "tfda-ok"}]

    monkeypatch.setattr("src.mcp_server.tools_source_health.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = check_source_health(source="TFDA")

    assert result["overall_status"] == "available"
    assert result["query_metadata"]["sources_checked"] == ["TFDA"]
    assert result["sources"][0]["source"] == "TFDA"
    assert result["sources"][0]["source_type"] == "regulatory"
    assert result["sources"][0]["available"] is True


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

    result = check_source_health(source="FDA")

    assert result["overall_status"] == "degraded"
    assert result["sources"][0]["available"] is False
    assert result["sources"][0]["error_code"] == "SOURCE_UNAVAILABLE"
    assert result["sources"][0]["message"] == "FDA unavailable"
    assert result["sources"][0]["suggested_next_action"] == "Retry later."


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

    result = check_source_health(source="ClinicalTrials.gov")

    assert result["overall_status"] == "degraded"
    assert result["sources"][0]["source"] == "ClinicalTrials.gov"
    assert result["sources"][0]["source_type"] == "clinical_trials_registry"
    assert result["sources"][0]["available"] is False
    assert result["sources"][0]["error_code"] == "SOURCE_UNAVAILABLE"


def test_check_source_health_handles_connector_exception(monkeypatch):
    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            raise RuntimeError("TFDA timeout")

    monkeypatch.setattr("src.mcp_server.tools_source_health.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = check_source_health(source="TFDA")

    assert result["overall_status"] == "degraded"
    assert result["sources"][0]["available"] is False
    assert result["sources"][0]["error_code"] == "SOURCE_UNAVAILABLE"
    assert "TFDA timeout" in result["sources"][0]["message"]


def test_check_source_health_rejects_unsupported_source():
    result = check_source_health(source="EMA")

    assert result["error"]["code"] == "INVALID_PARAMETER"
    assert "supported_sources" in result["error"]["details"]


def test_check_source_health_accepts_clinicaltrials_alias(monkeypatch):
    class FakeClinicalTrialsGovClient:
        def search_studies(self, **kwargs):
            return {"studies": []}

    monkeypatch.setattr(
        "src.mcp_server.tools_source_health.ClinicalTrialsGovClient",
        lambda: FakeClinicalTrialsGovClient(),
    )

    result = check_source_health(source="clinicaltrials")

    assert result["overall_status"] == "available"
    assert result["sources"][0]["source"] == "ClinicalTrials.gov"
