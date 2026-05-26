from pathlib import Path

from src.connectors.tfda.tfda_updates_client import TFDAUpdatesClient


def _read_fixture(name: str) -> str:
    return Path("tests/fixtures", name).read_text(encoding="utf-8")


def test_parse_tfda_table_fixture():
    client = TFDAUpdatesClient()
    records = client.parse_html_updates(_read_fixture("tfda_announcements_table_sample.html"))

    assert len(records) == 2
    assert records[0]["source_type"] == "TFDA_HTML"
    assert records[0]["official_url"].startswith("https://www.fda.gov.tw/")
    assert records[0]["publication_date"] == "2026-01-15"
    assert records[0]["document_status"] == "published"
    assert records[0]["topics"] == ["藥品公告"]


def test_parse_tfda_empty_fixture_returns_empty_list():
    client = TFDAUpdatesClient()
    records = client.parse_html_updates(_read_fixture("tfda_announcements_empty_sample.html"))

    assert records == []


def test_parse_tfda_malformed_fixture_does_not_crash_and_records_limitations():
    client = TFDAUpdatesClient()
    records = client.parse_html_updates(_read_fixture("tfda_announcements_malformed_sample.html"))

    assert len(records) == 1
    assert records[0]["title"] == "缺少連結的公告"
    assert records[0]["publication_date"] is None
    assert records[0]["known_limitations"]


def test_parse_tfda_json_fixture():
    client = TFDAUpdatesClient()
    records = client.parse_json_updates(_read_fixture("tfda_announcements_json_sample.json"))

    assert len(records) == 1
    assert records[0]["source_type"] == "TFDA_JSON"
    assert records[0]["publication_date"] == "2026-03-01"
    assert records[0]["official_url"].startswith("https://www.fda.gov.tw/")


def test_tfda_source_failure_path(monkeypatch):
    client = TFDAUpdatesClient()

    monkeypatch.setattr(
        client,
        "fetch_updates",
        lambda *args, **kwargs: {"error": {"code": "SOURCE_UNAVAILABLE", "message": "tfda down"}},
    )

    result = client.search_updates()
    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"


def test_tfda_search_updates_query_filter(monkeypatch):
    client = TFDAUpdatesClient()

    monkeypatch.setattr(
        client,
        "fetch_updates",
        lambda *args, **kwargs: {"html": _read_fixture("tfda_announcements_table_sample.html")},
    )

    records = client.search_updates(query="醫療器材", limit=10)

    assert isinstance(records, list)
    assert len(records) == 1
    assert "醫療器材" in records[0]["title"] or "醫療器材" in " ".join(records[0]["topics"])

def test_normalize_tfda_record():
    from dataclasses import asdict
    from src.core.normalization import normalize_tfda_record

    client = TFDAUpdatesClient()
    raw = client.parse_html_updates(_read_fixture("tfda_announcements_table_sample.html"))[0]
    rec = asdict(normalize_tfda_record(raw, retrieved_at="2026-01-16T00:00:00Z"))

    assert rec["agency"] == "TFDA"
    assert rec["region"] == "Taiwan"
    assert rec["official_url"].startswith("https://www.fda.gov.tw/")
    assert rec["source_type"] == "TFDA_HTML"
    assert rec["document_type"] == "regulatory_update"
    assert rec["product_modality"]
    assert "biologic_type" not in rec
    assert rec["content_hash"]
