import json
import types
from pathlib import Path

from src.connectors.clinical_trials.clinicaltrials_gov_client import ClinicalTrialsGovClient
from src.core.normalization import normalize_clinicaltrials_record


class FakeResponse:
    def __init__(self, status_code=200, payload=None, json_error=False):
        self.status_code = status_code
        self._payload = payload
        self._json_error = json_error

    def json(self):
        if self._json_error:
            raise ValueError("bad json")
        return self._payload


def fixture_payload(name: str):
    return json.loads((Path("tests/fixtures") / name).read_text(encoding="utf-8"))


def test_build_studies_query_basic():
    client = ClinicalTrialsGovClient()
    q = client.build_studies_query(indication="NSCLC", page_size=10)
    assert q["query.cond"] == "NSCLC"
    assert q["pageSize"] == 10


def test_build_studies_query_with_sponsor():
    client = ClinicalTrialsGovClient()
    q = client.build_studies_query(indication="NSCLC", page_size=10, sponsor="Roche")
    assert q["query.spons"] == "Roche"


def test_search_studies_uses_requests_get(monkeypatch):
    called = {}

    def fake_get(url, params, timeout):
        called["url"] = url
        called["params"] = params
        called["timeout"] = timeout
        return FakeResponse(payload={"studies": []})

    fake_requests = types.SimpleNamespace(get=fake_get, RequestException=Exception)
    monkeypatch.setitem(__import__("sys").modules, "requests", fake_requests)

    client = ClinicalTrialsGovClient(timeout=15)
    payload = client.search_studies(indication="NSCLC", page_size=5, sponsor="Roche")
    assert payload == {"studies": []}
    assert called["url"].endswith("/studies")
    assert called["params"]["query.cond"] == "NSCLC"
    assert called["timeout"] == 15


def test_search_studies_handles_http_error(monkeypatch):
    fake_requests = types.SimpleNamespace(get=lambda *args, **kwargs: FakeResponse(status_code=500), RequestException=Exception)
    monkeypatch.setitem(__import__("sys").modules, "requests", fake_requests)
    client = ClinicalTrialsGovClient()
    result = client.search_studies(indication="NSCLC")
    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"


def test_search_studies_handles_bad_json(monkeypatch):
    fake_requests = types.SimpleNamespace(get=lambda *args, **kwargs: FakeResponse(status_code=200, json_error=True), RequestException=Exception)
    monkeypatch.setitem(__import__("sys").modules, "requests", fake_requests)
    client = ClinicalTrialsGovClient()
    result = client.search_studies(indication="NSCLC")
    assert result["error"]["code"] == "INTERNAL_ERROR"


def test_search_studies_rejects_non_object_payload(monkeypatch):
    fake_requests = types.SimpleNamespace(get=lambda *args, **kwargs: FakeResponse(status_code=200, payload=[]), RequestException=Exception)
    monkeypatch.setitem(__import__("sys").modules, "requests", fake_requests)
    client = ClinicalTrialsGovClient()
    result = client.search_studies(indication="NSCLC")
    assert result["error"]["code"] == "INTERNAL_ERROR"


def test_iter_studies_next_page_token_pagination(monkeypatch):
    pages = [fixture_payload("clinicaltrials_gov_v2_page_1.json"), fixture_payload("clinicaltrials_gov_v2_page_2.json")]
    client = ClinicalTrialsGovClient()
    monkeypatch.setattr(client, "search_studies", lambda **kwargs: pages.pop(0))
    studies = client.iter_studies(indication="NSCLC", max_pages=2)
    assert len(studies) == 2


def test_iter_studies_skips_non_dict_studies(monkeypatch):
    client = ClinicalTrialsGovClient()
    monkeypatch.setattr(client, "search_studies", lambda **kwargs: {"studies": [{"ok": 1}, "bad", 123]})
    studies = client.iter_studies(indication="NSCLC")
    assert studies == [{"ok": 1}]


def test_normalize_clinicaltrials_record_minimal():
    raw = {
        "protocolSection": {
            "identificationModule": {"nctId": "NCT00000001", "briefTitle": "Minimal Trial"},
            "sponsorCollaboratorsModule": {"leadSponsor": {"name": "SponsorX"}},
            "statusModule": {"overallStatus": "RECRUITING"},
            "designModule": {"phases": ["PHASE1"]},
        }
    }
    rec = normalize_clinicaltrials_record(raw, retrieved_at="2026-01-01T00:00:00Z")
    assert rec.trial_id == "NCT00000001"
    assert rec.registry == "ClinicalTrials.gov"
    assert rec.official_url.endswith("NCT00000001")
    assert rec.title == "Minimal Trial"
    assert rec.sponsor == "SponsorX"
    assert rec.status == "RECRUITING"
    assert rec.phase == "PHASE1"


def test_normalize_clinicaltrials_record_missing_optional_fields():
    rec = normalize_clinicaltrials_record({}, retrieved_at="2026-01-01T00:00:00Z")
    assert rec.trial_id == ""
    assert isinstance(rec.known_limitations, list)
    assert rec.known_limitations


def test_normalize_clinicaltrials_record_handles_null_protocol_section():
    rec = normalize_clinicaltrials_record({"protocolSection": None}, retrieved_at="2026-01-01T00:00:00Z")
    rec_dict = rec.__dict__
    assert rec.registry == "ClinicalTrials.gov"
    assert isinstance(rec.known_limitations, list)
    assert "product_modality" in rec_dict
    assert "biologic_type" not in rec_dict


def test_normalize_fixture_page_1_and_2():
    rec1 = normalize_clinicaltrials_record(fixture_payload("clinicaltrials_gov_v2_page_1.json")["studies"][0], retrieved_at="2026-01-01T00:00:00Z")
    rec2 = normalize_clinicaltrials_record(fixture_payload("clinicaltrials_gov_v2_page_2.json")["studies"][0], retrieved_at="2026-01-01T00:00:00Z")
    assert rec1.trial_id == "NCT10000001"
    assert rec2.trial_id == "NCT10000002"
    assert rec1.product_modality
    assert rec2.product_modality


def test_normalize_handles_malformed_non_list_nested_values():
    raw = {
        "protocolSection": {
            "identificationModule": {"nctId": "NCTX", "briefTitle": "Bad Nested"},
            "conditionsModule": {"conditions": "NSCLC"},
            "designModule": {"phases": "PHASE1"},
            "armsInterventionsModule": {"interventions": "not-a-list"},
            "contactsLocationsModule": {"locations": "not-a-list"},
            "outcomesModule": {"primaryOutcomes": "not-a-list"},
        }
    }
    rec = normalize_clinicaltrials_record(raw, retrieved_at="2026-01-01T00:00:00Z")
    assert rec.indications == []
    assert rec.intervention_names == []
    assert rec.primary_outcomes == []

def test_iter_studies_stops_on_non_list_studies(monkeypatch):
    client = ClinicalTrialsGovClient()
    monkeypatch.setattr(client, "search_studies", lambda **kwargs: {"studies": "not-a-list"})
    assert client.iter_studies(indication="NSCLC", max_pages=3) == []


def test_iter_studies_stops_when_error_returned(monkeypatch):
    client = ClinicalTrialsGovClient()
    monkeypatch.setattr(client, "search_studies", lambda **kwargs: {"error": {"code": "SOURCE_UNAVAILABLE"}})
    assert client.iter_studies(indication="NSCLC", max_pages=3) == []
