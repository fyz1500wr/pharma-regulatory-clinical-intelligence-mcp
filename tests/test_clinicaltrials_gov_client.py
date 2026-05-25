import types

from src.connectors.clinical_trials.clinicaltrials_gov_client import ClinicalTrialsGovClient
from src.core.normalization import normalize_clinicaltrials_record


class FakeResponse:
    def __init__(self, status_code=200, payload=None, json_error=False):
        self.status_code = status_code
        self._payload = payload or {}
        self._json_error = json_error

    def json(self):
        if self._json_error:
            raise ValueError("bad json")
        return self._payload


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


def test_iter_studies_rejects_non_object_payload(monkeypatch):
    client = ClinicalTrialsGovClient()
    monkeypatch.setattr(client, "search_studies", lambda **kwargs: "not-a-dict")
    assert client.iter_studies(indication="NSCLC", max_pages=2) == []


def test_iter_studies_paginates_with_next_page_token(monkeypatch):
    client = ClinicalTrialsGovClient()
    calls = []
    pages = [
        {"studies": [{"protocolSection": {"identificationModule": {"nctId": "NCTP1"}}}], "nextPageToken": "token-2"},
        {"studies": [{"protocolSection": {"identificationModule": {"nctId": "NCTP2"}}}]},
    ]

    def fake_search(**kwargs):
        calls.append(kwargs.get("page_token"))
        return pages[len(calls) - 1]

    monkeypatch.setattr(client, "search_studies", fake_search)
    result = client.iter_studies(indication="NSCLC", max_pages=3)
    assert len(result) == 2
    assert calls == [None, "token-2"]


def test_iter_studies_skips_non_dict_studies_via_normalizer():
    rec = normalize_clinicaltrials_record("not-a-dict", retrieved_at="2026-01-01T00:00:00Z")
    assert rec.trial_id == ""
    assert rec.registry == "ClinicalTrials.gov"


def test_normalize_clinicaltrials_record_rich_fixture_page_1():
    raw = {
        "protocolSection": {
            "identificationModule": {"nctId": "NCT11111111", "briefTitle": "Small Molecule Trial"},
            "sponsorCollaboratorsModule": {"leadSponsor": {"name": "Acme"}},
            "statusModule": {"overallStatus": "RECRUITING"},
            "designModule": {"phases": ["PHASE2"]},
            "armsInterventionsModule": {"interventions": [{"name": "small molecule inhibitor"}]},
            "conditionsModule": {"conditions": ["NSCLC"]},
        }
    }
    rec = normalize_clinicaltrials_record(raw, retrieved_at="2026-01-01T00:00:00Z")
    assert rec.trial_id == "NCT11111111"
    assert "small_molecule" in rec.product_modality


def test_normalize_clinicaltrials_record_rich_fixture_page_2():
    raw = {
        "protocolSection": {
            "identificationModule": {"nctId": "NCT22222222", "briefTitle": "Monoclonal Antibody Trial"},
            "sponsorCollaboratorsModule": {"leadSponsor": {"name": "BioCo"}},
            "statusModule": {"overallStatus": "ACTIVE_NOT_RECRUITING"},
            "designModule": {"phases": ["PHASE1"]},
            "armsInterventionsModule": {"interventions": [{"name": "monoclonal antibody"}]},
            "conditionsModule": {"conditions": ["Oncology"]},
        }
    }
    rec = normalize_clinicaltrials_record(raw, retrieved_at="2026-01-01T00:00:00Z")
    assert rec.trial_id == "NCT22222222"
    assert "antibody" in rec.product_modality


def test_normalize_clinicaltrials_record_handles_malformed_non_list_nested_values():
    raw = {
        "protocolSection": {
            "identificationModule": {"nctId": "NCT33333333"},
            "armsInterventionsModule": {"interventions": {"name": "broken"}},
            "conditionsModule": {"conditions": "NSCLC"},
        }
    }
    rec = normalize_clinicaltrials_record(raw, retrieved_at="2026-01-01T00:00:00Z")
    assert rec.trial_id == "NCT33333333"
    assert rec.intervention_names == []
