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
                "id": "offline-fda-date-range-1m",
                "title": "Recent FDA date range guidance",
                "publication_date": "2026-05-15",
                "last_update_date": "2026-05-15",
                "official_url": "https://www.fda.gov/offline-date-range-1m-example",
                "source_type": "FDA_GUIDANCE",
                "document_type": "guidance",
                "document_status": "final",
                "product_modality": ["antibody"],
                "topics": ["CMC"],
                "summary": "Offline fixture within a 1-month date range.",
            },
            {
                "id": "offline-fda-date-range-1y",
                "title": "Older FDA date range guidance",
                "publication_date": "2025-07-01",
                "last_update_date": "2025-07-01",
                "official_url": "https://www.fda.gov/offline-date-range-1y-example",
                "source_type": "FDA_GUIDANCE",
                "document_type": "guidance",
                "document_status": "final",
                "product_modality": ["gene_therapy"],
                "topics": ["CMC"],
                "summary": "Offline fixture within a 1-year date range but outside a 1-month range.",
            },
            {
                "id": "offline-fda-date-range-custom",
                "title": "Historical FDA date range guidance",
                "publication_date": "2024-01-15",
                "last_update_date": "2024-01-15",
                "official_url": "https://www.fda.gov/offline-date-range-custom-example",
                "source_type": "FDA_GUIDANCE",
                "document_type": "guidance",
                "document_status": "final",
                "product_modality": ["vaccine"],
                "topics": ["quality"],
                "summary": "Offline fixture for custom date range and explicit date filter checks.",
            },
        ]
        return records[:limit]


class _FixedDateTime:
    @staticmethod
    def now(tz=None):
        return real_datetime(2026, 6, 1, tzinfo=timezone.utc)

    @staticmethod
    def fromisoformat(value):
        return real_datetime.fromisoformat(value)


def _assert(condition: bool, payload: Any) -> None:
    if not condition:
        raise AssertionError(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def _record_ids(payload: dict[str, Any]) -> list[str]:
    return [record["id"] for record in payload["records"]]


def run_smoke() -> dict[str, Any]:
    original_fda = tools_regulatory.FDAUpdatesClient
    original_datetime = tools_regulatory.datetime

    try:
        tools_regulatory.FDAUpdatesClient = OfflineFDAUpdatesClient
        tools_regulatory.datetime = _FixedDateTime

        one_month = tools_regulatory.search_regulatory_updates(
            agency="FDA",
            date_range="1m",
            limit=10,
        )
        _assert("error" not in one_month, one_month)
        _assert(_record_ids(one_month) == ["offline-fda-date-range-1m"], one_month)
        one_month_filters = one_month["query_metadata"]["filters_applied"]
        _assert(one_month_filters["date_range"] == "1m", one_month)
        _assert(one_month_filters["date_from"] == "2026-05-01", one_month)
        _assert(one_month_filters["date_to"] == "2026-06-01", one_month)

        one_year = tools_regulatory.search_regulatory_updates(
            agency="FDA",
            date_range="1y",
            limit=10,
        )
        _assert("error" not in one_year, one_year)
        _assert(
            _record_ids(one_year)
            == ["offline-fda-date-range-1m", "offline-fda-date-range-1y"],
            one_year,
        )
        one_year_filters = one_year["query_metadata"]["filters_applied"]
        _assert(one_year_filters["date_range"] == "1y", one_year)
        _assert(one_year_filters["date_from"] == "2025-06-01", one_year)
        _assert(one_year_filters["date_to"] == "2026-06-01", one_year)

        custom = tools_regulatory.search_regulatory_updates(
            agency="FDA",
            date_range="custom",
            custom_date_range={"start_date": "2024-01-01", "end_date": "2024-01-31"},
            limit=10,
        )
        _assert("error" not in custom, custom)
        _assert(_record_ids(custom) == ["offline-fda-date-range-custom"], custom)
        custom_filters = custom["query_metadata"]["filters_applied"]
        _assert(custom_filters["date_range"] == "custom", custom)
        _assert(
            custom_filters["custom_date_range"]
            == {"start_date": "2024-01-01", "end_date": "2024-01-31"},
            custom,
        )
        _assert(custom_filters["date_from"] == "2024-01-01", custom)
        _assert(custom_filters["date_to"] == "2024-01-31", custom)

        explicit = tools_regulatory.search_regulatory_updates(
            agency="FDA",
            date_from="2025-07-01",
            date_to="2025-07-01",
            limit=10,
        )
        _assert("error" not in explicit, explicit)
        _assert(_record_ids(explicit) == ["offline-fda-date-range-1y"], explicit)
        explicit_filters = explicit["query_metadata"]["filters_applied"]
        _assert(explicit_filters["date_range"] is None, explicit)
        _assert(explicit_filters["custom_date_range"] is None, explicit)
        _assert(explicit_filters["date_from"] == "2025-07-01", explicit)
        _assert(explicit_filters["date_to"] == "2025-07-01", explicit)

        invalid = tools_regulatory.search_regulatory_updates(
            agency="FDA",
            date_range="2y",
            limit=10,
        )
        _assert(invalid["error"]["code"] == "INVALID_PARAMETER", invalid)
        _assert("date_range must be one of" in invalid["error"]["message"], invalid)

        ambiguous = tools_regulatory.search_regulatory_updates(
            agency="FDA",
            date_range="1y",
            date_from="2025-01-01",
            limit=10,
        )
        _assert(ambiguous["error"]["code"] == "INVALID_PARAMETER", ambiguous)
        _assert("cannot be combined" in ambiguous["error"]["message"], ambiguous)

        summary = {
            "status": "passed",
            "validated_cases": [
                "date_range='1m'",
                "date_range='1y'",
                "date_range='custom'",
                "custom_date_range start_date / end_date",
                "date_from / date_to backward compatibility",
                "invalid date_range structured error",
                "ambiguous date input rejection",
                "query_metadata.filters_applied.date_range",
                "query_metadata.filters_applied.custom_date_range",
                "query_metadata.filters_applied.date_from",
                "query_metadata.filters_applied.date_to",
            ],
            "important_interpretation": (
                "This offline smoke validates date range filter behavior only. "
                "It does not validate live FDA/TFDA source availability."
            ),
        }

        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        print("offline regulatory date range smoke passed")
        return summary

    finally:
        tools_regulatory.FDAUpdatesClient = original_fda
        tools_regulatory.datetime = original_datetime


if __name__ == "__main__":
    run_smoke()
