from __future__ import annotations

import json
import sys
from datetime import datetime as real_datetime
from datetime import timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.mcp_server import tools_regulatory


class OfflineFDAUpdatesClient:
    def search_updates(self, query=None, source_types=None, limit=20):
        records = [
            {
                "id": "offline-query-metadata-fda-antibody-1",
                "title": "FDA monoclonal antibody CMC guidance update",
                "publication_date": "2026-05-10",
                "last_update_date": "2026-05-10",
                "official_url": "https://www.fda.gov/offline-query-metadata-antibody-example",
                "source_type": "FDA_GUIDANCE",
                "document_type": "guidance",
                "document_status": "final",
                "product_modality": ["antibody"],
                "topics": ["CMC", "quality"],
                "summary": "Offline fixture for monoclonal antibody query metadata consistency checks.",
            },
            {
                "id": "offline-query-metadata-fda-vaccine-1",
                "title": "FDA vaccine quality update",
                "publication_date": "2026-05-18",
                "last_update_date": "2026-05-18",
                "official_url": "https://www.fda.gov/offline-query-metadata-vaccine-example",
                "source_type": "FDA_GUIDANCE",
                "document_type": "guidance",
                "document_status": "draft",
                "product_modality": ["vaccine"],
                "topics": ["quality"],
                "summary": "Control fixture outside the requested antibody modality.",
            },
        ]
        return _filter_fixture_records(records, query=query, source_types=source_types, limit=limit)


class OfflineTFDAUpdatesClient:
    def search_updates(self, query=None, source_types=None, limit=20):
        records = [
            {
                "id": "offline-query-metadata-tfda-adc-1",
                "title": "TFDA ADC 品質審查公告",
                "publication_date": "2026-05-12",
                "last_update_date": "2026-05-12",
                "official_url": "https://www.fda.gov.tw/offline-query-metadata-adc-example",
                "source_type": "TFDA_HTML",
                "document_type": "regulatory_update",
                "document_status": "published",
                "product_modality": ["adc"],
                "topics": ["品質", "CMC"],
                "summary": "Offline fixture for ADC query metadata consistency checks.",
            },
            {
                "id": "offline-query-metadata-tfda-biosimilar-1",
                "title": "TFDA 生物相似性藥品公告",
                "publication_date": "2026-05-16",
                "last_update_date": "2026-05-16",
                "official_url": "https://www.fda.gov.tw/offline-query-metadata-biosimilar-example",
                "source_type": "TFDA_HTML",
                "document_type": "regulatory_update",
                "document_status": "published",
                "product_modality": ["biosimilar"],
                "topics": ["查驗登記"],
                "summary": "Control fixture outside the requested ADC modality.",
            },
        ]
        return _filter_fixture_records(records, query=query, source_types=source_types, limit=limit)


class _FixedDateTime:
    @staticmethod
    def now(tz=None):
        return real_datetime(2026, 6, 1, tzinfo=timezone.utc)

    @staticmethod
    def fromisoformat(value):
        return real_datetime.fromisoformat(value)


def _filter_fixture_records(records, *, query=None, source_types=None, limit=20):
    filtered = list(records)

    if query:
        normalized_query = str(query).strip().lower()
        filtered = [
            record
            for record in filtered
            if normalized_query
            in " ".join(
                [
                    str(record.get("title", "")),
                    str(record.get("summary", "")),
                    " ".join(record.get("topics", [])),
                ]
            ).lower()
        ]

    if source_types:
        allowed = {str(source_type).strip().upper() for source_type in source_types}
        filtered = [record for record in filtered if str(record.get("source_type", "")).upper() in allowed]

    return filtered[:limit]


def _assert(condition: bool, payload: Any) -> None:
    if not condition:
        raise AssertionError(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def _parse_iso_date(value: str | None) -> None:
    _assert(isinstance(value, str) and value, {"invalid_date": value})
    real_datetime.fromisoformat(value)


def _assert_record_metadata_contract(record: dict[str, Any], *, agency: str, source_type: str) -> None:
    required_fields = [
        "id",
        "agency",
        "region",
        "title",
        "publication_date",
        "last_update_date",
        "retrieved_at",
        "official_url",
        "source_type",
        "document_type",
        "document_status",
        "product_modality",
        "topics",
        "summary",
        "known_limitations",
        "content_hash",
    ]
    missing_fields = [field for field in required_fields if field not in record]
    _assert(missing_fields == [], {"missing_fields": missing_fields, "record": record})

    _assert(record["agency"] == agency, record)
    _assert(record["source_type"] == source_type, record)
    _assert(isinstance(record["title"], str) and record["title"], record)
    _assert(isinstance(record["official_url"], str) and record["official_url"].startswith("https://"), record)
    _parse_iso_date(record["publication_date"])
    _parse_iso_date(record["last_update_date"])
    _parse_iso_date(record["retrieved_at"])
    _assert(isinstance(record["product_modality"], list) and record["product_modality"], record)
    _assert(isinstance(record["topics"], list) and record["topics"], record)
    _assert(isinstance(record["content_hash"], str) and record["content_hash"], record)


def _assert_query_metadata_contract(
    payload: dict[str, Any],
    *,
    agency: str,
    source_types: list[str],
    query: str,
    product_modality: list[str],
    date_range: str,
) -> None:
    metadata = payload.get("query_metadata")
    _assert(isinstance(metadata, dict), payload)
    _assert(metadata.get("agency_searched") == [agency], metadata)
    _assert(metadata.get("sources_searched") == source_types, metadata)

    filters = metadata.get("filters_applied")
    _assert(isinstance(filters, dict), metadata)
    _assert(filters.get("query") == query, filters)
    _assert(filters.get("source_types") == source_types, filters)
    _assert(filters.get("product_modality") == product_modality, filters)
    _assert(filters.get("date_range") == date_range, filters)
    _assert(filters.get("date_from") == "2026-05-01", filters)
    _assert(filters.get("date_to") == "2026-06-01", filters)
    _assert(filters.get("limit") == 10, filters)


def _single_record(payload: dict[str, Any]) -> dict[str, Any]:
    _assert("error" not in payload, payload)
    _assert(len(payload.get("records", [])) == 1, payload)
    return payload["records"][0]


def run_smoke() -> dict[str, Any]:
    original_fda = tools_regulatory.FDAUpdatesClient
    original_tfda = tools_regulatory.TFDAUpdatesClient
    original_datetime = tools_regulatory.datetime

    try:
        tools_regulatory.FDAUpdatesClient = OfflineFDAUpdatesClient
        tools_regulatory.TFDAUpdatesClient = OfflineTFDAUpdatesClient
        tools_regulatory.datetime = _FixedDateTime

        fda_payload = tools_regulatory.search_regulatory_updates(
            agency="FDA",
            query="monoclonal antibody",
            source_types="FDA_GUIDANCE",
            product_modality="antibody",
            date_range="1m",
            limit=10,
        )
        fda_record = _single_record(fda_payload)
        _assert_record_metadata_contract(fda_record, agency="FDA", source_type="FDA_GUIDANCE")
        _assert_query_metadata_contract(
            fda_payload,
            agency="FDA",
            source_types=["FDA_GUIDANCE"],
            query="monoclonal antibody",
            product_modality=["antibody"],
            date_range="1m",
        )

        tfda_payload = tools_regulatory.search_regulatory_updates(
            agency="TFDA",
            query="ADC",
            source_types="TFDA_HTML",
            product_modality="adc",
            date_range="1m",
            limit=10,
        )
        tfda_record = _single_record(tfda_payload)
        _assert_record_metadata_contract(tfda_record, agency="TFDA", source_type="TFDA_HTML")
        _assert_query_metadata_contract(
            tfda_payload,
            agency="TFDA",
            source_types=["TFDA_HTML"],
            query="ADC",
            product_modality=["adc"],
            date_range="1m",
        )

        fda_metadata_keys = set(fda_payload["query_metadata"].keys())
        tfda_metadata_keys = set(tfda_payload["query_metadata"].keys())
        _assert(fda_metadata_keys == tfda_metadata_keys, {"FDA": fda_metadata_keys, "TFDA": tfda_metadata_keys})

        fda_filter_keys = set(fda_payload["query_metadata"]["filters_applied"].keys())
        tfda_filter_keys = set(tfda_payload["query_metadata"]["filters_applied"].keys())
        _assert(fda_filter_keys == tfda_filter_keys, {"FDA": fda_filter_keys, "TFDA": tfda_filter_keys})

        _assert(set(fda_record.keys()) == set(tfda_record.keys()), {"FDA": fda_record, "TFDA": tfda_record})

        summary = {
            "status": "passed",
            "validated_cases": [
                "FDA regulatory record metadata contract",
                "TFDA regulatory record metadata contract",
                "query_metadata agency and source contract",
                "query_metadata filters_applied query contract",
                "query_metadata filters_applied product_modality contract",
                "query_metadata filters_applied date_range contract",
                "date_from/date_to derived from 1m date_range",
                "FDA/TFDA query_metadata key consistency",
                "FDA/TFDA filters_applied key consistency",
                "FDA/TFDA normalized record key consistency",
            ],
            "important_interpretation": (
                "This offline smoke validates normalized regulatory search metadata consistency only. "
                "It does not validate live FDA/TFDA source availability or approve source expansion."
            ),
        }

        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        print("offline query metadata consistency smoke passed")
        return summary

    finally:
        tools_regulatory.FDAUpdatesClient = original_fda
        tools_regulatory.TFDAUpdatesClient = original_tfda
        tools_regulatory.datetime = original_datetime


if __name__ == "__main__":
    run_smoke()
