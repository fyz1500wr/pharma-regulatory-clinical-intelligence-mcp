import json
import types
from pathlib import Path

from src.connectors.clinical_trials.clinicaltrials_gov_client import ClinicalTrialsGovClient
from src.core.normalization import normalize_clinicaltrials_record


class FakeResponse:
    def __init__(self, status_code=200, payload=None, json_error=False):
        self.status_code = status_code
        self._payload = {} if payload is None else payload
        self._json_error = json_error

    def json(self):
        if self._json_error:
            raise ValueError("bad json")
        return self._payload


def _load_fixture(name: str) -> dict:
    fixture_path = Path(__file__).parent / "fixtures" / name
    return json.loads(fixture_path.read_text(encoding="utf-8"))


def test_search_studies_rejects_non_object_payload(monkeypatch):
    fake_requests = types.SimpleNamespace(get=lambda *args, **kwargs: FakeResponse(payload=["not-object"]), RequestException=Exception)
    monkeypatch.setitem(__import__("sys").modules, "requests", fake_requests)
    client = ClinicalTrialsGovClient()
    result = client.search_studies(indication="NSCLC")
    assert result["error"]["code"] == "INTERNAL_ERROR"


def test_iter_studies_follows_next_page_token(monkeypatch):
    client = ClinicalTrialsGovClient()
    page_1 = _load_fixture("clinicaltrials_gov_v2_page_1.json")
    page_2 = _load_fixture("clinicaltrials_gov_v2_page_2.json")
    seen_tokens = []

    def fake_search_studies(**kwargs):
        seen_tokens.append(kwargs.get("page_token"))
        if kwargs.get("page_token") == "token-page-2":
            return page_2
        return page_1

    monkeypatch.setattr(client, "search_studies", fake_search_studies)
    studies = client.iter_studies(indication="NSCLC", max_pages=2)
    assert seen_tokens == [None, "token-page-2"]
    assert len(studies) == len(page_1["studies"]) + len(page_2["studies"])


def test_iter_studies_skips_non_dict_studies(monkeypatch):
    client = ClinicalTrialsGovClient()

    def fake_search_studies(**kwargs):
        return {"studies": [{"protocolSection": {}}, "bad-record"]}

    monkeypatch.setattr(client, "search_studies", fake_search_studies)
    studies = client.iter_studies(indication="NSCLC")
    assert studies == [{"protocolSection": {}}]


def test_normalize_clinicaltrials_record_rich_fixture_page_1():
    page_1 = _load_fixture("clinicaltrials_gov_v2_page_1.json")
    rec = normalize_clinicaltrials_record(page_1["studies"][0], retrieved_at="2026-01-01T00:00:00Z")
    assert rec.trial_id == "NCT90000001"
    assert rec.sponsor == "Synthetic Pharma A"
    assert rec.phase == "PHASE2"
    assert rec.status == "RECRUITING"
    assert rec.countries == ["United States", "Canada", "Japan"]
    assert rec.primary_outcomes == ["Progression-Free Survival", "Objective Response Rate"]
    assert rec.product_modality == ["antibody"]


def test_normalize_clinicaltrials_record_rich_fixture_page_2():
    page_2 = _load_fixture("clinicaltrials_gov_v2_page_2.json")
    rec = normalize_clinicaltrials_record(page_2["studies"][0], retrieved_at="2026-01-01T00:00:00Z")
    assert rec.results_available is True
    assert rec.countries == ["Germany", "France"]
    assert rec.primary_outcomes == ["Overall Survival"]
    assert rec.product_modality == ["antibody"]


def test_normalize_clinicaltrials_record_handles_non_list_nested_values():
    raw = {
        "protocolSection": {
            "identificationModule": {"nctId": "NCTX"},
            "conditionsModule": {"conditions": "NSCLC"},
            "armsInterventionsModule": {"interventions": "bad"},
            "contactsLocationsModule": {"locations": "bad"},
            "outcomesModule": {"primaryOutcomes": "bad"},
        }
    }
    rec = normalize_clinicaltrials_record(raw, retrieved_at="2026-01-01T00:00:00Z")
    assert rec.indications == []
    assert rec.intervention_names == []
    assert rec.countries == []
    assert rec.primary_outcomes == []
