from src.mcp_server.server import TOOL_REGISTRY
from src.mcp_server.tools_clinical_trials import search_clinical_trials_by_indication
from src.mcp_server.tools_regulatory import compare_regulatory_updates


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


def test_product_modality_still_uses_product_modality(monkeypatch):
    class FakeClient:
        def search_studies(self, **kwargs):
            return {
                "studies": [{"protocolSection": {"identificationModule": {"nctId": "NCT456", "briefTitle": "Study"}}}]
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


def test_search_clinical_trials_by_indication_empty_result_shape(monkeypatch):
    class FakeClient:
        def search_studies(self, **kwargs):
            return {"studies": []}

    monkeypatch.setattr("src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient", lambda: FakeClient())
    result = search_clinical_trials_by_indication("NSCLC")
    assert result["trials"] == []
    assert result["no_result_reason"] == "NO_MATCHING_RECORDS"


def test_search_clinical_trials_by_indication_trims_indication(monkeypatch):
    seen = {}

    class FakeClient:
        def search_studies(self, **kwargs):
            seen["indication"] = kwargs["indication"]
            return {"studies": []}

    monkeypatch.setattr("src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient", lambda: FakeClient())
    search_clinical_trials_by_indication("  NSCLC  ")
    assert seen["indication"] == "NSCLC"


def test_classifier_nce_does_not_match_cancer(monkeypatch):
    class FakeClient:
        def search_studies(self, **kwargs):
            return {
                "studies": [
                    {"protocolSection": {"identificationModule": {"nctId": "NCT90000001", "briefTitle": "NCE cancer study"}}}
                ]
            }

    monkeypatch.setattr("src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient", lambda: FakeClient())
    result = search_clinical_trials_by_indication("cancer")
    modalities = result["trials"][0]["product_modality"]
    assert "cell_therapy" not in modalities


def test_classifier_small_molecule_still_matches(monkeypatch):
    class FakeClient:
        def search_studies(self, **kwargs):
            return {
                "studies": [
                    {
                        "protocolSection": {
                            "identificationModule": {"nctId": "NCT90000002", "briefTitle": "Kinase inhibitor"},
                            "armsInterventionsModule": {"interventions": [{"name": "small molecule inhibitor"}]},
                        }
                    }
                ]
            }

    monkeypatch.setattr("src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient", lambda: FakeClient())
    result = search_clinical_trials_by_indication("oncology")
    assert "small_molecule" in result["trials"][0]["product_modality"]


def test_classifier_monoclonal_antibody_still_matches(monkeypatch):
    class FakeClient:
        def search_studies(self, **kwargs):
            return {
                "studies": [
                    {
                        "protocolSection": {
                            "identificationModule": {"nctId": "NCT90000003", "briefTitle": "mAb study"},
                            "armsInterventionsModule": {"interventions": [{"name": "monoclonal antibody"}]},
                        }
                    }
                ]
            }

    monkeypatch.setattr("src.mcp_server.tools_clinical_trials.ClinicalTrialsGovClient", lambda: FakeClient())
    result = search_clinical_trials_by_indication("oncology")
    assert "antibody" in result["trials"][0]["product_modality"]
