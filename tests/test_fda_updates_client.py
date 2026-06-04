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

def test_guidance_time_datetime_attribute_is_not_concatenated_with_display_text():
    client = FDAUpdatesClient()
    records = client.parse_guidance_documents(_read_fixture("fda_guidance_sample.html"))
    assert records
    assert records[0]["publication_date"] == "2026-01-15"



def test_fetch_guidance_documents_preserves_fda_abuse_detection_details(monkeypatch):
    class FakeHTTPError(Exception):
        pass

    class FakeResponse:
        url = "https://www.fda.gov/apology_objects/abuse-detection-apology.html"
        status_code = 404
        text = "Not found - abuse detection"

        def raise_for_status(self):
            exc = FakeHTTPError("404 Client Error: Not Found")
            exc.response = self
            raise exc

    class FakeRequests:
        @staticmethod
        def get(*args, **kwargs):
            return FakeResponse()

    import sys

    monkeypatch.setitem(sys.modules, "requests", FakeRequests)
    result = FDAUpdatesClient().fetch_guidance_documents()

    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"
    details = result["error"]["details"]
    assert details["requested_url"] == "https://www.fda.gov/drugs/guidance-compliance-regulatory-information"
    assert details["final_url"] == "https://www.fda.gov/apology_objects/abuse-detection-apology.html"
    assert details["status_code"] == 404
    assert details["detected_source_block"] is True
    assert details["redirected_to_abuse_detection"] is True


def test_fetch_rss_feed_preserves_fda_abuse_detection_details(monkeypatch):
    class FakeHTTPError(Exception):
        pass

    class FakeResponse:
        url = "https://www.fda.gov/apology_objects/abuse-detection-apology.html"
        status_code = 404
        text = "Not found - abuse detection"

        def raise_for_status(self):
            exc = FakeHTTPError("404 Client Error: Not Found")
            exc.response = self
            raise exc

    class FakeRequests:
        @staticmethod
        def get(*args, **kwargs):
            return FakeResponse()

    import sys

    feed_url = "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/whats-new-drug-rss-feed"
    monkeypatch.setitem(sys.modules, "requests", FakeRequests)
    result = FDAUpdatesClient().fetch_rss_feed(feed_url)

    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"
    details = result["error"]["details"]
    assert details["requested_url"] == feed_url
    assert details["final_url"] == "https://www.fda.gov/apology_objects/abuse-detection-apology.html"
    assert details["status_code"] == 404
    assert details["detected_source_block"] is True
    assert details["redirected_to_abuse_detection"] is True


def test_fetch_guidance_documents_treats_http_200_abuse_page_as_source_unavailable(monkeypatch):
    class FakeResponse:
        url = "https://www.fda.gov/apology_objects/abuse-detection-apology.html"
        status_code = 200
        text = "<html><body id='abuse-detection-apology'>FDA abuse detection apology page</body></html>"

        def raise_for_status(self):
            return None

    class FakeRequests:
        @staticmethod
        def get(*args, **kwargs):
            return FakeResponse()

    import sys

    monkeypatch.setitem(sys.modules, "requests", FakeRequests)
    result = FDAUpdatesClient().fetch_guidance_documents()

    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"
    assert "NO_MATCHING_RECORDS" not in str(result)
    details = result["error"]["details"]
    assert details["status_code"] == 200
    assert details["detected_source_block"] is True
    assert details["redirected_to_abuse_detection"] is True


def test_fetch_rss_feed_treats_http_200_abuse_page_as_source_unavailable(monkeypatch):
    class FakeResponse:
        url = "https://www.fda.gov/apology_objects/abuse-detection-apology.html"
        status_code = 200
        text = "<html><script>window.apology_objects = [];</script>abuse detection</html>"

        def raise_for_status(self):
            return None

    class FakeRequests:
        @staticmethod
        def get(*args, **kwargs):
            return FakeResponse()

    import sys

    feed_url = "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/whats-new-drug-rss-feed"
    monkeypatch.setitem(sys.modules, "requests", FakeRequests)
    result = FDAUpdatesClient().fetch_rss_feed(feed_url)

    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"
    assert "NO_MATCHING_RECORDS" not in str(result)
    details = result["error"]["details"]
    assert details["requested_url"] == feed_url
    assert details["status_code"] == 200
    assert details["detected_source_block"] is True
    assert details["redirected_to_abuse_detection"] is True


def test_fetch_guidance_documents_treats_http_200_body_only_abuse_page_as_source_unavailable(monkeypatch):
    class FakeResponse:
        url = "https://www.fda.gov/drugs/guidance-compliance-regulatory-information"
        status_code = 200
        text = "<html><script>window.apology_objects = [];</script></html>"

        def raise_for_status(self):
            return None

    class FakeRequests:
        @staticmethod
        def get(*args, **kwargs):
            return FakeResponse()

    import sys

    monkeypatch.setitem(sys.modules, "requests", FakeRequests)
    result = FDAUpdatesClient().fetch_guidance_documents()

    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"
    assert "html" not in result
    details = result["error"]["details"]
    assert details["final_url"] == "https://www.fda.gov/drugs/guidance-compliance-regulatory-information"
    assert details["status_code"] == 200
    assert details["detected_source_block"] is True
    assert details["redirected_to_abuse_detection"] is True


def test_fetch_rss_feed_treats_http_200_body_only_abuse_page_as_source_unavailable(monkeypatch):
    class FakeResponse:
        url = "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/whats-new-drug-rss-feed"
        status_code = 200
        text = "<html><main>Access blocked by FDA abuse detection</main></html>"

        def raise_for_status(self):
            return None

    class FakeRequests:
        @staticmethod
        def get(*args, **kwargs):
            return FakeResponse()

    import sys

    feed_url = "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/whats-new-drug-rss-feed"
    monkeypatch.setitem(sys.modules, "requests", FakeRequests)
    result = FDAUpdatesClient().fetch_rss_feed(feed_url)

    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"
    assert "xml" not in result
    details = result["error"]["details"]
    assert details["requested_url"] == feed_url
    assert details["final_url"] == feed_url
    assert details["status_code"] == 200
    assert details["detected_source_block"] is True
    assert details["redirected_to_abuse_detection"] is True


def test_search_updates_preserves_source_unavailable_when_fda_abuse_detection_blocks_all_sources(monkeypatch):
    client = FDAUpdatesClient()
    failure = {
        "error": {
            "code": "SOURCE_UNAVAILABLE",
            "message": "FDA fetch failed: 404 Client Error",
            "details": {
                "requested_url": "https://www.fda.gov/current",
                "final_url": "https://www.fda.gov/apology_objects/abuse-detection-apology.html",
                "status_code": 404,
                "detected_source_block": True,
                "redirected_to_abuse_detection": True,
            },
        }
    }

    monkeypatch.setattr(client, "fetch_guidance_documents", lambda *args, **kwargs: failure)
    monkeypatch.setattr(client, "fetch_rss_feed", lambda *args, **kwargs: failure)

    result = client.search_updates()
    assert result["error"]["code"] == "SOURCE_UNAVAILABLE"
    assert result["error"]["details"]["source_failures"][0]["details"]["redirected_to_abuse_detection"] is True
