from src.mcp_server.tools_clinical_trials import search_clinical_trials_by_indication
from src.mcp_server.tools_regulatory import search_regulatory_updates


def test_mvp_v1_regulatory_fda_and_tfda_smoke(monkeypatch):
    class FakeFDAClient:
        def search_updates(self, **kwargs):
            return [
                {
                    "id": "fda-smoke-1",
                    "title": "FDA Smoke Guidance",
                    "official_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/fda-smoke-guidance",
                    "publication_date": "2026-01-01",
                    "last_update_date": None,
                    "source_type": "FDA_GUIDANCE",
                    "document_type": "guidance",
                    "document_status": "final",
                    "product_modality": ["drug"],
                    "topics": ["quality"],
                    "summary": "FDA smoke test record.",
                    "known_limitations": [],
                }
            ]

    class FakeTFDAClient:
        def search_updates(self, **kwargs):
            return [
                {
                    "id": "tfda-smoke-1",
                    "title": "TFDA Smoke Update",
                    "official_url": "https://www.fda.gov.tw/TC/newsContent.aspx?id=1",
                    "publication_date": "2026-01-15",
                    "last_update_date": None,
                    "source_type": "TFDA_HTML",
                    "document_type": "regulatory_update",
                    "document_status": "published",
                    "product_modality": ["drug"],
                    "topics": ["藥品公告"],
                    "summary": "TFDA smoke test record.",
                    "known_limitations": [],
                }
            ]

    monkeypatch.setattr("src.mcp_server.tools_regulatory.FDAUpdatesClient", lambda: FakeFDAClient())
    monkeypatch.setattr("src.mcp_server.tools_regulatory.TFDAUpdatesClient", lambda: FakeTFDAClient())

    fda = search_regulatory_updates(agency="FDA", limit=1)
    tfda = search_regulatory_updates(agency="TFDA", limit=1)

    assert fda["records"][0]["agency"] == "FDA"
    assert fda["query_metadata"]["agency_searched"] == ["FDA"]
    assert fda["query_metadata"]["sources_searched"] == ["FDA_GUIDANCE", "FDA_RSS"]
    assert "biologic_type" not in fda["records"][0]

    assert tfda["records"][0]["agency"] == "TFDA"
    assert tfda["query_metadata"]["agency_searched"] == ["TFDA"]
    assert tfda["query_metadata"]["sources_searched"] == ["TFDA_HTML"]
    assert "biologic_type" not in tfda["records"][0]


def test_mvp_v1_clinicaltrials_smoke(monkeypatch):
    class FakeClinicalTrialsGovClient:
        def search_studies(self, **kwargs):
            return {
                "studies": [
                    {
                        "protocolSection": {
                            "identificationModule": {
                                "nctId": "NCT00000001",
                                "briefTitle": "ClinicalTrials.gov Smoke Study",
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
                                "briefSummary": "Smoke test clinical trial record.",
                            },
                        }
                    }
                ]
            }

    monkeypatch.setattr(
        "src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient",
        lambda: FakeClinicalTrialsGovClient(),
    )

    result = search_clinical_trials_by_indication(indication="lung cancer", page_size=1)

    assert result["trials"][0]["registry"] == "ClinicalTrials.gov"
    assert result["trials"][0]["trial_id"] == "NCT00000001"
    assert result["query_metadata"]["registries_searched"] == ["ClinicalTrials.gov"]


def test_mvp_v1_regulatory_invalid_agency_still_rejected():
    result = search_regulatory_updates(agency="EMA")

    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_mvp_v1_clinicaltrials_invalid_indication_still_rejected():
    result = search_clinical_trials_by_indication(indication="")

    assert result["error"]["code"] == "INVALID_PARAMETER"
