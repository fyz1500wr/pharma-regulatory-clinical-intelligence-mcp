from dataclasses import asdict
from pathlib import Path

from src.connectors.fda.fda_updates_client import FDAUpdatesClient
from src.core.normalization import normalize_fda_record


def _read_fixture(name: str) -> str:
    return Path("tests/fixtures", name).read_text(encoding="utf-8")


def test_parse_guidance_fixture():
    client = FDAUpdatesClient()
    records = client.parse_guidance_documents(_read_fixture("fda_guidance_sample.html"))
    assert len(records) >= 1
    assert records[0]["source_type"] == "FDA_GUIDANCE"


def test_parse_rss_fixture():
    client = FDAUpdatesClient()
    records = client.parse_rss_items(_read_fixture("fda_whats_new_drugs_sample.xml"))
    assert len(records) >= 1
    assert records[0]["source_type"] == "FDA_RSS"


def test_normalize_guidance_record():
    client = FDAUpdatesClient()
    raw = client.parse_guidance_documents(_read_fixture("fda_guidance_sample.html"))[0]
    rec = asdict(normalize_fda_record(raw, retrieved_at="2026-01-16T00:00:00Z"))
    assert rec["agency"] == "FDA"
    assert rec["region"] == "US"
    assert rec["official_url"].startswith("https://www.fda.gov/")
    assert rec["product_modality"]
    assert "biologic_type" not in rec


def test_normalize_rss_record():
    client = FDAUpdatesClient()
    raw = client.parse_rss_items(_read_fixture("fda_whats_new_drugs_sample.xml"))[0]
    rec = asdict(normalize_fda_record(raw, retrieved_at="2026-01-16T00:00:00Z"))
    assert rec["agency"] == "FDA"
    assert rec["official_url"].startswith("https://www.fda.gov/")


def test_malformed_fixture_does_not_crash():
    client = FDAUpdatesClient()
    assert client.parse_guidance_documents("<article") == []
    assert client.parse_rss_items("<rss>") == []


def test_source_failure_path(monkeypatch):
    class FakeRequests:
        @staticmethod
        def get(*args, **kwargs):
            raise RuntimeError("boom")

    import sys

    monkeypatch.setitem(sys.modules, "requests", FakeRequests)
    res = FDAUpdatesClient().fetch_rss_feed("https://www.fda.gov/rss.xml")
    assert "error" in res
    assert res["error"]["code"] == "SOURCE_UNAVAILABLE"


def test_empty_fixture_returns_empty_list():
    client = FDAUpdatesClient()
    assert client.parse_guidance_documents("") == []
    assert client.parse_rss_items("") == []
