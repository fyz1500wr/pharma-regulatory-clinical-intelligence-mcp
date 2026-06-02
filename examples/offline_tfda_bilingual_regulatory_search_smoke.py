from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.mcp_server import tools_regulatory


class OfflineTFDAUpdatesClient:
    def search_updates(self, query=None, source_types=None, limit=20):
        records = [
            {
                "id": "offline-tfda-mrna-vaccine-1",
                "title": "mRNA疫苗品質及臨床試驗資料公告",
                "publication_date": "2026-05-20",
                "last_update_date": "2026-05-20",
                "official_url": "https://www.fda.gov.tw/offline-mrna-vaccine-example",
                "source_type": "TFDA_HTML",
                "document_type": "regulatory_update",
                "document_status": "published",
                "topics": ["品質", "臨床試驗", "CMC"],
                "summary": "TFDA-style offline fixture for 信使RNA and mRNA疫苗 regulatory retrieval.",
            },
            {
                "id": "offline-tfda-adc-1",
                "title": "抗體藥物複合體 ADC 藥品品質審查重點公告",
                "publication_date": "2026-05-22",
                "last_update_date": "2026-05-22",
                "official_url": "https://www.fda.gov.tw/offline-adc-example",
                "source_type": "TFDA_HTML",
                "document_type": "regulatory_update",
                "document_status": "published",
                "topics": ["品質", "CMC"],
                "summary": "TFDA-style offline fixture for 抗體藥物複合體 and antibody-drug conjugate retrieval.",
            },
            {
                "id": "offline-tfda-biosimilar-1",
                "title": "生物相似性藥品查驗登記審查注意事項",
                "publication_date": "2026-05-25",
                "last_update_date": "2026-05-25",
                "official_url": "https://www.fda.gov.tw/offline-biosimilar-example",
                "source_type": "TFDA_HTML",
                "document_type": "regulatory_update",
                "document_status": "published",
                "topics": ["品質", "查驗登記"],
                "summary": "TFDA-style offline fixture for 生物相似性藥品 regulatory retrieval.",
            },
            {
                "id": "offline-tfda-general-1",
                "title": "一般藥品法規公告",
                "publication_date": "2026-05-28",
                "last_update_date": "2026-05-28",
                "official_url": "https://www.fda.gov.tw/offline-general-example",
                "source_type": "TFDA_HTML",
                "document_type": "regulatory_update",
                "document_status": "published",
                "topics": ["法規"],
                "summary": "General TFDA-style fixture without a specific product modality.",
            },
        ]

        if query:
            normalized_query = str(query).strip().lower()
            records = [
                record
                for record in records
                if normalized_query
                in " ".join(
                    [
                        str(record.get("title", "")),
                        str(record.get("summary", "")),
                        " ".join(record.get("topics", [])),
                    ]
                ).lower()
            ]

        return records[:limit]


def _assert(condition: bool, payload: Any) -> None:
    if not condition:
        raise AssertionError(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def _record_ids(payload: dict[str, Any]) -> list[str]:
    return [record["id"] for record in payload["records"]]


def run_smoke() -> dict[str, Any]:
    original_tfda = tools_regulatory.TFDAUpdatesClient

    try:
        tools_regulatory.TFDAUpdatesClient = OfflineTFDAUpdatesClient

        mrna = tools_regulatory.search_regulatory_updates(
            agency="TFDA",
            query="mRNA疫苗",
            product_modality="mrna_rna",
            limit=10,
        )
        _assert("error" not in mrna, mrna)
        _assert(_record_ids(mrna) == ["offline-tfda-mrna-vaccine-1"], mrna)
        _assert("mrna_rna" in mrna["records"][0]["product_modality"], mrna)
        _assert(mrna["query_metadata"]["filters_applied"]["query"] == "mRNA疫苗", mrna)
        _assert(mrna["query_metadata"]["filters_applied"]["product_modality"] == ["mrna_rna"], mrna)

        adc = tools_regulatory.search_regulatory_updates(
            agency="TFDA",
            query="抗體藥物複合體",
            product_modality="adc",
            limit=10,
        )
        _assert("error" not in adc, adc)
        _assert(_record_ids(adc) == ["offline-tfda-adc-1"], adc)
        _assert(adc["records"][0]["product_modality"] == ["adc"], adc)

        biosimilar = tools_regulatory.search_regulatory_updates(
            agency="TFDA",
            query="生物相似性藥品",
            product_modality="biosimilar",
            limit=10,
        )
        _assert("error" not in biosimilar, biosimilar)
        _assert(_record_ids(biosimilar) == ["offline-tfda-biosimilar-1"], biosimilar)
        _assert(biosimilar["records"][0]["product_modality"] == ["biosimilar"], biosimilar)

        list_filter = tools_regulatory.search_regulatory_updates(
            agency="TFDA",
            product_modality=["adc", "biosimilar"],
            limit=10,
        )
        _assert("error" not in list_filter, list_filter)
        _assert(set(_record_ids(list_filter)) == {"offline-tfda-adc-1", "offline-tfda-biosimilar-1"}, list_filter)
        _assert(
            list_filter["query_metadata"]["filters_applied"]["product_modality"]
            == ["adc", "biosimilar"],
            list_filter,
        )

        no_result = tools_regulatory.search_regulatory_updates(
            agency="TFDA",
            query="mRNA疫苗",
            product_modality="adc",
            limit=10,
        )
        _assert(no_result["records"] == [], no_result)
        _assert(no_result["no_result_reason"] == "NO_MATCHING_RECORDS", no_result)
        _assert(no_result["query_metadata"]["filters_applied"]["query"] == "mRNA疫苗", no_result)
        _assert(no_result["query_metadata"]["filters_applied"]["product_modality"] == ["adc"], no_result)

        invalid = tools_regulatory.search_regulatory_updates(
            agency="TFDA",
            query="mRNA疫苗",
            product_modality="tfda_bilingual",
            limit=10,
        )
        _assert(invalid["error"]["code"] == "INVALID_PARAMETER", invalid)
        _assert("Unsupported product_modality" in invalid["error"]["message"], invalid)

        summary = {
            "status": "passed",
            "validated_cases": [
                "TFDA bilingual query retrieval for mRNA疫苗",
                "TFDA bilingual query retrieval for 抗體藥物複合體 ADC",
                "TFDA bilingual query retrieval for 生物相似性藥品",
                "TFDA product_modality classification from Chinese title/summary",
                "TFDA product_modality list filter after bilingual retrieval",
                "TFDA bilingual no-result behavior after modality filtering",
                "invalid product_modality structured error",
                "query_metadata.filters_applied.query",
                "query_metadata.filters_applied.product_modality",
            ],
            "important_interpretation": (
                "This offline smoke validates TFDA-style bilingual retrieval and product modality "
                "filter behavior only. It does not validate live TFDA source availability."
            ),
        }

        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        print("offline TFDA bilingual regulatory search smoke passed")
        return summary

    finally:
        tools_regulatory.TFDAUpdatesClient = original_tfda


if __name__ == "__main__":
    run_smoke()
