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

def test_search_updates_returns_source_unavailable_when_all_sources_fail(monkeypatch):
    client = FDAUpdatesClient()

    monkeypatch.setattr(
        client,
        "fetch_guidance_documents",
        lambda *args, **kwargs: {"error": {"code": "SOURCE_UNAVAILABLE", "message": "guidance down"}},
    )
    monkeypatch.setattr(
        client,
        "fetch_rss_feed",
        lambda *args, **kwargs: {"error": {"code": "SOURCE_UNAVAILABLE", "message": "rss down"}},
    )

    result = client.search_updates()
    assert "error" in result
    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"

def test_parse_realistic_guidance_table_fixture():
    client = FDAUpdatesClient()
    records = client.parse_guidance_documents(_read_fixture("fda_guidance_search_table_sample.html"))
    assert len(records) == 2
    assert records[0]["official_url"].startswith("https://www.fda.gov/")
    assert records[0]["publication_date"] == "2026-03-14"
    assert records[0]["document_status"] == "final"
    assert records[1]["document_status"] == "draft"
    assert "CDER" in records[0]["topics"]


def test_guidance_empty_table_returns_empty_list():
    client = FDAUpdatesClient()
    records = client.parse_guidance_documents(_read_fixture("fda_guidance_search_empty_sample.html"))
    assert records == []


def test_guidance_malformed_table_does_not_crash_and_records_limitations():
    client = FDAUpdatesClient()
    records = client.parse_guidance_documents(_read_fixture("fda_guidance_search_malformed_sample.html"))
    assert len(records) == 1
    assert records[0]["document_status"] == "unknown"
    assert records[0]["known_limitations"]


def test_parse_realistic_rss_fixture_dates_and_links():
    client = FDAUpdatesClient()
    records = client.parse_rss_items(_read_fixture("fda_whats_new_drugs_rss_realistic_sample.xml"))
    assert len(records) == 2
    assert records[0]["publication_date"] == "2026-02-02"
    assert records[0]["official_url"].startswith("https://www.fda.gov/")
    assert records[0]["source_type"] == "FDA_RSS"


def test_empty_rss_fixture_returns_empty_list():
    client = FDAUpdatesClient()
    records = client.parse_rss_items(_read_fixture("fda_whats_new_drugs_rss_empty_sample.xml"))
    assert records == []


def test_search_updates_source_type_guidance_only(monkeypatch):
    client = FDAUpdatesClient()

    monkeypatch.setattr(
        client,
        "fetch_guidance_documents",
        lambda **kwargs: {"html": _read_fixture("fda_guidance_search_table_sample.html")},
    )
    monkeypatch.setattr(
        client,
        "fetch_rss_feed",
        lambda *args, **kwargs: {"error": {"code": "SOURCE_UNAVAILABLE", "message": "rss should not be called"}},
    )

    records = client.search_updates(source_types=["FDA_GUIDANCE"], limit=10)
    assert isinstance(records, list)
    assert records
    assert all(record["source_type"] == "FDA_GUIDANCE" for record in records)


def test_search_updates_partial_source_failure_keeps_successful_records(monkeypatch):
    client = FDAUpdatesClient()

    monkeypatch.setattr(
        client,
        "fetch_guidance_documents",
        lambda **kwargs: {"html": _read_fixture("fda_guidance_search_table_sample.html")},
    )
    monkeypatch.setattr(
        client,
        "fetch_rss_feed",
        lambda *args, **kwargs: {"error": {"code": "SOURCE_UNAVAILABLE", "message": "rss down"}},
    )

    records = client.search_updates(source_types=["FDA_GUIDANCE", "FDA_RSS"], limit=10)
    assert isinstance(records, list)
    assert records
    assert any("Partial FDA source failure" in " ".join(record.get("known_limitations", [])) for record in records)
