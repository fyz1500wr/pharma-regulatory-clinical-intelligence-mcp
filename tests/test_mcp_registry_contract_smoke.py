from src.mcp_server.server import TOOL_REGISTRY


EXPECTED_MVP_V1_TOOLS = {
    "search_regulatory_updates",
    "get_regulatory_document_detail",
    "compare_regulatory_updates",
    "search_clinical_trials_by_indication",
    "compare_companies_by_indication",
    "check_source_health",
    "list_source_failures",
    "generate_regulatory_digest",
}


def test_mvp_v1_tool_registry_contains_expected_tools():
    assert set(TOOL_REGISTRY) == EXPECTED_MVP_V1_TOOLS


def test_check_source_health_contract_smoke(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return [{"id": "fda-ok"}]

    monkeypatch.setattr("src.mcp_server.tools_source_health.FDAUpdatesClient", lambda: FakeFDAClient())

    result = TOOL_REGISTRY["check_source_health"](source="FDA_openFDA")

    assert "source_health" in result
    assert "query_metadata" in result
    assert result["source_health"][0]["source_id"] == "FDA_openFDA"
    assert result["source_health"][0]["agency_or_registry"] == "FDA"
    assert result["source_health"][0]["status"] == "pass"


def test_search_regulatory_updates_contract_smoke(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return [
                {
                    "id": "fda-contract-smoke-1",
                    "title": "FDA Contract Smoke Guidance",
                    "official_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/fda-contract-smoke-guidance",
                    "publication_date": "2026-01-01",
                    "last_update_date": None,
                    "source_type": "FDA_GUIDANCE",
                    "document_type": "guidance",
                    "document_status": "final",
                    "product_modality": ["drug"],
                    "topics": ["quality"],
                    "summary": "FDA contract smoke record.",
                    "known_limitations": [],
                }
            ]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())

    result = TOOL_REGISTRY["search_regulatory_updates"](agency="FDA", limit=1)

    assert "records" in result
    assert "query_metadata" in result
    assert result["records"][0]["agency"] == "FDA"
    assert result["records"][0]["id"] == "fda-contract-smoke-1"


def test_search_regulatory_updates_structured_error_contract_smoke():
    result = TOOL_REGISTRY["search_regulatory_updates"](agency="EMA")

    assert result["error"]["code"] == "INVALID_PARAMETER"
    assert "suggested_next_action" in result["error"]


def test_search_clinical_trials_by_indication_contract_smoke(monkeypatch):
    class FakeClinicalTrialsGovClient:
        def search_studies(self, **kwargs):
            return {
                "studies": [
                    {
                        "protocolSection": {
                            "identificationModule": {
                                "nctId": "NCT99999999",
                                "briefTitle": "Registry Contract Smoke Study",
                            },
                            "statusModule": {
                                "overallStatus": "RECRUITING",
                                "startDateStruct": {"date": "2026-01-01"},
                                "primaryCompletionDateStruct": {"date": "2027-01-01"},
                                "lastUpdateSubmitDateStruct": {"date": "2026-02-01"},
                                "hasResults": False,
                            },
                            "conditionsModule": {
                                "conditions": ["lung cancer"],
                            },
                            "sponsorCollaboratorsModule": {
                                "leadSponsor": {"name": "Smoke Sponsor"},
                            },
                            "designModule": {
                                "phases": ["PHASE2"],
                            },
                            "contactsLocationsModule": {
                                "locations": [{"country": "United States"}],
                            },
                            "armsInterventionsModule": {
                                "interventions": [{"name": "Smoke Drug"}],
                            },
                            "outcomesModule": {
                                "primaryOutcomes": [{"measure": "Overall response rate"}],
                            },
                            "descriptionModule": {
                                "briefSummary": "Registry contract smoke test record.",
                            },
                        }
                    }
                ]
            }

    monkeypatch.setattr(
        "src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient",
        lambda: FakeClinicalTrialsGovClient(),
    )

    result = TOOL_REGISTRY["search_clinical_trials_by_indication"](indication="lung cancer", page_size=1)

    assert "trials" in result
    assert "query_metadata" in result
    assert result["trials"][0]["registry"] == "ClinicalTrials.gov"
    assert result["trials"][0]["trial_id"] == "NCT99999999"


def test_search_clinical_trials_structured_error_contract_smoke():
    result = TOOL_REGISTRY["search_clinical_trials_by_indication"](indication="")

    assert result["error"]["code"] == "INVALID_PARAMETER"
    assert "suggested_next_action" in result["error"]


def _assert_contract_key_or_structured_error(result, expected_key):
    assert isinstance(result, dict)

    if expected_key in result:
        return

    assert "error" in result
    assert "code" in result["error"]
    assert "message" in result["error"]
    assert "suggested_next_action" in result["error"]


def test_placeholder_tools_keep_stable_top_level_contract_keys_or_structured_errors():
    document_detail = TOOL_REGISTRY["get_regulatory_document_detail"](document_id="demo")
    regulatory_compare = TOOL_REGISTRY["compare_regulatory_updates"]()
    company_compare = TOOL_REGISTRY["compare_companies_by_indication"](indication="lung cancer")
    digest = TOOL_REGISTRY["generate_regulatory_digest"]()
    failures = TOOL_REGISTRY["list_source_failures"]()

    _assert_contract_key_or_structured_error(document_detail, "document")
    _assert_contract_key_or_structured_error(regulatory_compare, "comparison")
    _assert_contract_key_or_structured_error(company_compare, "company_comparison")
    _assert_contract_key_or_structured_error(digest, "digest")

    assert "failures" in failures
    assert "summary" in failures
