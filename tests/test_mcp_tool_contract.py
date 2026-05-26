from src.mcp_server.server import TOOL_REGISTRY
from src.mcp_server.tools_clinical_trials import search_clinical_trials_by_indication
from src.mcp_server.tools_regulatory import compare_regulatory_updates, search_regulatory_updates


def test_required_tool_names_exist():
    required = {
        "search_regulatory_updates", "get_regulatory_document_detail", "search_clinical_trials_by_indication",
        "check_source_health", "list_source_failures", "generate_regulatory_digest",
        "compare_regulatory_updates", "compare_companies_by_indication",
    }
    assert required.issubset(set(TOOL_REGISTRY.keys()))


def test_compare_regulatory_updates_structured_error():
    result = compare_regulatory_updates()
    assert "error" in result
    assert result["error"]["code"] == "DATA_NOT_INGESTED"


def test_search_regulatory_updates_fda_with_fake_client(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return [{"id":"1","title":"FDA Guidance","official_url":"https://www.fda.gov/x","publication_date":"2026-01-01","source_type":"FDA_GUIDANCE","document_type":"guidance","document_status":"draft","product_modality":["unknown"],"topics":["general"],"summary":"s","known_limitations":[]}]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    result = search_regulatory_updates(agency="FDA")
    assert result["records"]
    assert "product_modality" in result["records"][0]
    assert "biologic_type" not in result["records"][0]


def test_search_regulatory_updates_tfda_not_ingested():
    result = search_regulatory_updates(agency="TFDA")
    assert result["no_result_reason"] == "DATA_NOT_INGESTED"


def test_search_regulatory_updates_unsupported_agency():
    result = search_regulatory_updates(agency="EMA")
    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_search_regulatory_updates_empty_fda(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return []

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    result = search_regulatory_updates(agency="FDA")
    assert result["records"] == []
    assert result["no_result_reason"] == "NO_MATCHING_RECORDS"


def test_mcp_search_clinical_trials_by_indication_with_fake_client(monkeypatch):
    class FakeClient:
        def search_studies(self, **kwargs):
            return {
                "studies": [
                    {
                        "protocolSection": {
                            "identificationModule": {"nctId": "NCT123", "briefTitle": "Study"},
                            "sponsorCollaboratorsModule": {"leadSponsor": {"name": "Acme Pharma"}},
                            "statusModule": {"overallStatus": "RECRUITING", "hasResults": True},
                            "designModule": {"phases": ["PHASE2"]},
                            "armsInterventionsModule": {"interventions": [{"name": "small molecule inhibitor"}]},
                            "conditionsModule": {"conditions": ["NSCLC"]},
                        }
                    }
                ]
            }

    monkeypatch.setattr("src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient", lambda: FakeClient())
    result = search_clinical_trials_by_indication("NSCLC")
    assert result["trials"]
    assert result["query_metadata"]["registries_searched"] == ["ClinicalTrials.gov"]

def test_search_regulatory_updates_fda_source_unavailable(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return {
                "error": {
                    "code": "SOURCE_UNAVAILABLE",
                    "message": "FDA sources unavailable",
                    "suggested_next_action": "Check FDA source availability.",
                }
            }

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    result = search_regulatory_updates(agency="FDA")
    assert "error" in result
    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"


def test_search_regulatory_updates_fda_unexpected_exception(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            raise RuntimeError("boom")

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    result = search_regulatory_updates(agency="FDA")
    assert "error" in result
    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"


def test_mcp_search_clinical_trials_empty_results(monkeypatch):
    class FakeClient:
        def search_studies(self, **kwargs):
            return {"studies": []}

    monkeypatch.setattr("src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient", lambda: FakeClient())
    result = search_clinical_trials_by_indication("NSCLC")
    assert result["trials"] == []
    assert result["no_result_reason"] == "NO_MATCHING_RECORDS"


def test_trimmed_indication(monkeypatch):
    seen = {}

    class FakeClient:
        def search_studies(self, **kwargs):
            seen.update(kwargs)
            return {"studies": []}

    monkeypatch.setattr("src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient", lambda: FakeClient())
    search_clinical_trials_by_indication("  NSCLC  ")
    assert seen["indication"] == "NSCLC"


def test_product_modality_still_uses_product_modality(monkeypatch):
    class FakeClient:
        def search_studies(self, **kwargs):
            return {
                "studies": [
                    {
                        "protocolSection": {
                            "identificationModule": {
                                "nctId": "NCT456",
                                "briefTitle": "Study",
                            }
                        }
                    }
                ]
            }

    monkeypatch.setattr("src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient", lambda: FakeClient())
    result = search_clinical_trials_by_indication("oncology")
    trial = result["trials"][0]
    assert "product_modality" in trial
    assert "biologic_type" not in trial


def test_search_clinical_trials_by_indication_rejects_non_string_indication():
    for bad_input in ([], {}, 123):
        result = search_clinical_trials_by_indication(bad_input)
        assert "error" in result
        assert result["error"]["code"] == "INVALID_PARAMETER"

def test_search_regulatory_updates_source_types_guidance_only(monkeypatch):
    seen = {}

    class FakeFDAClient:
        def search_updates(self, **kwargs):
            seen.update(kwargs)
            return [
                {
                    "id": "g1",
                    "title": "Final FDA Guidance",
                    "official_url": "https://www.fda.gov/guidance",
                    "publication_date": "2026-03-14",
                    "source_type": "FDA_GUIDANCE",
                    "document_type": "guidance",
                    "document_status": "final",
                    "product_modality": ["unknown"],
                    "topics": ["general"],
                    "summary": "summary",
                    "known_limitations": [],
                }
            ]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    result = search_regulatory_updates(agency="FDA", source_types=["FDA_GUIDANCE"], limit=10)
    assert result["records"]
    assert seen["source_types"] == ["FDA_GUIDANCE"]
    assert result["query_metadata"]["sources_searched"] == ["FDA_GUIDANCE"]


def test_search_regulatory_updates_rejects_invalid_source_type():
    result = search_regulatory_updates(agency="FDA", source_types=["FDA_BAD"])
    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_search_regulatory_updates_rejects_invalid_limit():
    result = search_regulatory_updates(agency="FDA", limit=0)
    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_search_regulatory_updates_filters_document_status(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return [
                {
                    "id": "draft",
                    "title": "Draft FDA Guidance",
                    "official_url": "https://www.fda.gov/draft",
                    "publication_date": "2026-04-02",
                    "source_type": "FDA_GUIDANCE",
                    "document_type": "guidance",
                    "document_status": "draft",
                    "product_modality": ["unknown"],
                    "topics": ["general"],
                    "summary": "",
                    "known_limitations": [],
                },
                {
                    "id": "final",
                    "title": "Final FDA Guidance",
                    "official_url": "https://www.fda.gov/final",
                    "publication_date": "2026-03-14",
                    "source_type": "FDA_GUIDANCE",
                    "document_type": "guidance",
                    "document_status": "final",
                    "product_modality": ["unknown"],
                    "topics": ["general"],
                    "summary": "",
                    "known_limitations": [],
                },
            ]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    result = search_regulatory_updates(agency="FDA", document_status="draft")
    assert len(result["records"]) == 1
    assert result["records"][0]["document_status"] == "draft"


def test_search_regulatory_updates_filters_date_range(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return [
                {
                    "id": "old",
                    "title": "Old FDA Guidance",
                    "official_url": "https://www.fda.gov/old",
                    "publication_date": "2026-01-01",
                    "source_type": "FDA_GUIDANCE",
                    "document_type": "guidance",
                    "document_status": "final",
                    "product_modality": ["unknown"],
                    "topics": ["general"],
                    "summary": "",
                    "known_limitations": [],
                },
                {
                    "id": "new",
                    "title": "New FDA Guidance",
                    "official_url": "https://www.fda.gov/new",
                    "publication_date": "2026-04-02",
                    "source_type": "FDA_GUIDANCE",
                    "document_type": "guidance",
                    "document_status": "draft",
                    "product_modality": ["unknown"],
                    "topics": ["general"],
                    "summary": "",
                    "known_limitations": [],
                },
            ]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    result = search_regulatory_updates(agency="FDA", date_from="2026-04-01", date_to="2026-04-30")
    assert len(result["records"]) == 1
    assert result["records"][0]["id"] == "new"


def test_search_regulatory_updates_rejects_invalid_date_range():
    result = search_regulatory_updates(agency="FDA", date_from="2026-05-01", date_to="2026-04-01")
    assert result["error"]["code"] == "INVALID_PARAMETER"
