from src.mcp_server.server import TOOL_REGISTRY


def _fake_regulatory_record(record_id, *, agency="FDA"):
    if agency == "TFDA":
        return {
            "id": record_id,
            "title": "TFDA MVP v1 Smoke Update",
            "official_url": "https://www.fda.gov.tw/TC/newsContent.aspx?id=smoke",
            "publication_date": "2026-01-15",
            "source_type": "TFDA_HTML",
            "document_type": "regulatory_update",
            "document_status": "published",
            "product_modality": ["unknown"],
            "topics": ["quality"],
            "summary": "TFDA smoke test record.",
            "known_limitations": [],
        }

    return {
        "id": record_id,
        "title": "FDA MVP v1 Smoke Guidance",
        "official_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/smoke",
        "publication_date": "2026-01-01",
        "source_type": "FDA_GUIDANCE",
        "document_type": "guidance",
        "document_status": "final",
        "product_modality": ["unknown"],
        "topics": ["quality"],
        "summary": "FDA smoke test record.",
        "known_limitations": [],
    }


def _fake_health(source, *, available=True):
    source_type = "clinical_trials_registry" if source == "ClinicalTrials.gov" else "regulatory"
    return {
        "overall_status": "available" if available else "degraded",
        "sources": [
            {
                "source": source,
                "source_type": source_type,
                "available": available,
                "retrieved_at": "2026-01-01T00:00:00+00:00",
                "error_code": "" if available else "SOURCE_UNAVAILABLE",
                "message": "OK" if available else f"{source} unavailable",
                "suggested_next_action": f"Check {source} connector.",
                "known_limitations": [],
            }
        ],
        "query_metadata": {
            "known_limitations": [],
        },
    }


def test_tool_registry_search_regulatory_updates_smoke(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return [_fake_regulatory_record("fda-smoke-1", agency="FDA")]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())

    result = TOOL_REGISTRY["search_regulatory_updates"](agency="FDA", query="quality", limit=5)

    assert "error" not in result
    assert result["records"]
    assert result["records"][0]["agency"] == "FDA"
    assert result["query_metadata"]["agency_searched"] == ["FDA"]


def test_tool_registry_get_regulatory_document_detail_smoke(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return [_fake_regulatory_record("fda-smoke-detail-1", agency="FDA")]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())

    result = TOOL_REGISTRY["get_regulatory_document_detail"](
        "fda-smoke-detail-1",
        agency="FDA",
    )

    assert "error" not in result
    assert result["document"]["id"] == "fda-smoke-detail-1"
    assert result["document"]["agency"] == "FDA"
    assert result["query_metadata"]["lookup_mode"] == "skeleton_backed_search_metadata"


def test_tool_registry_compare_regulatory_updates_smoke(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return [_fake_regulatory_record("fda-smoke-compare-1", agency="FDA")]

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return [_fake_regulatory_record("tfda-smoke-compare-1", agency="TFDA")]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    result = TOOL_REGISTRY["compare_regulatory_updates"](
        agencies=["FDA", "TFDA"],
        comparison_axis="agency",
        query="quality",
    )

    assert "error" not in result
    assert "comparison" in result
    assert "comparison_summary" in result
    assert result["query_metadata"]["lookup_mode"] == "skeleton_backed_search_metadata"


def test_tool_registry_search_clinical_trials_by_indication_smoke(monkeypatch):
    class FakeClinicalTrialsGovClient:
        def search_studies(self, **kwargs):
            return {
                "studies": [
                    {
                        "protocolSection": {
                            "identificationModule": {
                                "nctId": "NCT00000001",
                                "briefTitle": "MVP v1 Smoke Trial",
                            },
                            "sponsorCollaboratorsModule": {
                                "leadSponsor": {"name": "Acme Pharma"},
                            },
                            "statusModule": {
                                "overallStatus": "RECRUITING",
                                "hasResults": False,
                            },
                            "designModule": {
                                "phases": ["PHASE2"],
                            },
                            "armsInterventionsModule": {
                                "interventions": [{"name": "small molecule"}],
                            },
                            "conditionsModule": {
                                "conditions": ["NSCLC"],
                            },
                        }
                    }
                ]
            }

    monkeypatch.setattr(
        "src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient",
        lambda: FakeClinicalTrialsGovClient(),
    )

    result = TOOL_REGISTRY["search_clinical_trials_by_indication"]("NSCLC")

    assert "error" not in result
    assert result["trials"]
    assert result["query_metadata"]["registries_searched"] == ["ClinicalTrials.gov"]


def test_tool_registry_check_source_health_smoke(monkeypatch):
    def fake_health_impl(source, mode):
        return _fake_health(source, available=True)

    monkeypatch.setattr("src.mcp_server.tools_healthcheck._check_source_health_impl", fake_health_impl)

    result = TOOL_REGISTRY["check_source_health"](sources=["FDA_openFDA", "ClinicalTrialsGov_API"])

    assert "error" not in result
    assert result["overall_status"] == "available"
    assert result["query_metadata"]["sources_checked"] == ["FDA_openFDA", "ClinicalTrialsGov_API"]


def test_tool_registry_list_source_failures_smoke(monkeypatch):
    def fake_health_impl(source, mode):
        return _fake_health(source, available=(source != "FDA"))

    monkeypatch.setattr("src.mcp_server.tools_healthcheck._check_source_health_impl", fake_health_impl)

    result = TOOL_REGISTRY["list_source_failures"](sources=["FDA_openFDA"])

    assert "error" not in result
    assert len(result["failures"]) == 1
    assert result["failures"][0]["source_id"] == "FDA_openFDA"
    assert result["summary"]["open_failure_count"] == 1


def test_tool_registry_compare_companies_by_indication_remains_placeholder():
    result = TOOL_REGISTRY["compare_companies_by_indication"](indication="NSCLC")

    assert result["error"]["code"] == "DATA_NOT_INGESTED"


def test_tool_registry_generate_regulatory_digest_minimal_mvp_smoke(monkeypatch):
    def fake_search_regulatory_updates(**kwargs):
        return {
            "records": [
                {
                    "title": "FDA MVP v1 Digest Smoke Guidance",
                    "agency": "FDA",
                    "publication_date": "2026-01-01",
                    "impact_level": "unknown",
                    "official_url": "https://www.fda.gov/smoke",
                    "summary": "Digest smoke regulatory record.",
                    "topics": ["quality"],
                    "product_modality": ["unknown"],
                }
            ],
            "known_limitations": [],
        }

    def fake_search_clinical_trials_by_indication(indication, **kwargs):
        return {
            "trials": [
                {
                    "trial_id": "NCT00000001",
                    "title": "Digest Smoke Trial",
                    "sponsor": "Acme Pharma",
                    "phase": "PHASE2",
                    "status": "RECRUITING",
                    "last_update_date": "2026-01-02",
                    "official_url": "https://clinicaltrials.gov/study/NCT00000001",
                    "indications": [indication],
                }
            ],
            "query_metadata": {"known_limitations": []},
        }

    def fake_check_source_health(**kwargs):
        return {"overall_status": "available", "known_limitations": []}

    def fake_list_source_failures(**kwargs):
        return {"summary": {"open_failure_count": 0, "known_limitations": []}}

    monkeypatch.setattr("src.mcp_server.tools_digest.search_regulatory_updates", fake_search_regulatory_updates)
    monkeypatch.setattr(
        "src.mcp_server.tools_digest.search_clinical_trials_by_indication",
        fake_search_clinical_trials_by_indication,
    )
    monkeypatch.setattr("src.mcp_server.tools_digest.check_source_health", fake_check_source_health)
    monkeypatch.setattr("src.mcp_server.tools_digest.list_source_failures", fake_list_source_failures)

    result = TOOL_REGISTRY["generate_regulatory_digest"](
        date_range="1m",
        agencies=["FDA"],
        registries=["ClinicalTrials.gov"],
        indications=["NSCLC"],
    )

    assert "error" not in result
    assert result["digest"]["title"] == "MVP v1 Regulatory and Clinical Intelligence Digest"
    assert result["digest"]["key_regulatory_updates"]
    assert result["digest"]["key_clinical_trial_updates"]
    assert result["query_metadata"]["lookup_mode"] == "minimal_mvp_aggregation"
