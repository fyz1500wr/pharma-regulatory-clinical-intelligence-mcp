from __future__ import annotations

import json
import sys
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
                "id": "offline-fda-antibody-1",
                "title": "Monoclonal antibody development guidance",
                "publication_date": "2026-01-10",
                "last_update_date": "2026-01-10",
                "official_url": "https://www.fda.gov/offline-antibody-example",
                "source_type": "FDA_GUIDANCE",
                "document_type": "guidance",
                "document_status": "final",
                "product_modality": ["antibody"],
                "topics": ["CMC"],
                "summary": "Offline fixture for antibody regulatory update filtering.",
            },
            {
                "id": "offline-fda-gene-therapy-1",
                "title": "Gene therapy CMC guidance",
                "publication_date": "2026-01-15",
                "last_update_date": "2026-01-15",
                "official_url": "https://www.fda.gov/offline-gene-therapy-example",
                "source_type": "FDA_GUIDANCE",
                "document_type": "guidance",
                "document_status": "final",
                "product_modality": ["gene_therapy"],
                "topics": ["CMC"],
                "summary": "Offline fixture for gene therapy regulatory update filtering.",
            },
        ]
        return records[:limit]


class OfflineTFDAUpdatesClient:
    def search_updates(self, query=None, source_types=None, limit=20):
        records = [
            {
                "id": "offline-tfda-biosimilar-1",
                "title": "Biosimilar quality review notice",
                "publication_date": "2026-02-01",
                "last_update_date": "2026-02-01",
                "official_url": "https://www.fda.gov.tw/offline-biosimilar-example",
                "source_type": "TFDA_HTML",
                "document_type": "regulatory_update",
                "document_status": "published",
                "product_modality": ["biosimilar"],
                "topics": ["quality"],
                "summary": "Offline fixture for TFDA biosimilar regulatory update filtering.",
            }
        ]
        return records[:limit]


def _assert(condition: bool, payload: Any) -> None:
    if not condition:
        raise AssertionError(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def run_smoke() -> dict[str, Any]:
    original_fda = tools_regulatory.FDAUpdatesClient
    original_tfda = tools_regulatory.TFDAUpdatesClient

    try:
        tools_regulatory.FDAUpdatesClient = OfflineFDAUpdatesClient
        tools_regulatory.TFDAUpdatesClient = OfflineTFDAUpdatesClient

        antibody = tools_regulatory.search_regulatory_updates(
            agency="FDA",
            product_modality="antibody",
            limit=10,
        )
        _assert("error" not in antibody, antibody)
        _assert([r["id"] for r in antibody["records"]] == ["offline-fda-antibody-1"], antibody)
        _assert(antibody["query_metadata"]["filters_applied"]["product_modality"] == ["antibody"], antibody)

        multi = tools_regulatory.search_regulatory_updates(
            agency="FDA",
            product_modality=["antibody", "gene_therapy"],
            limit=10,
        )
        _assert("error" not in multi, multi)
        _assert(
            {r["id"] for r in multi["records"]}
            == {"offline-fda-antibody-1", "offline-fda-gene-therapy-1"},
            multi,
        )

        no_result = tools_regulatory.search_regulatory_updates(
            agency="FDA",
            product_modality="cell_therapy",
            limit=10,
        )
        _assert(no_result["records"] == [], no_result)
        _assert(no_result["no_result_reason"] == "NO_MATCHING_RECORDS", no_result)
        _assert(no_result["query_metadata"]["filters_applied"]["product_modality"] == ["cell_therapy"], no_result)

        invalid = tools_regulatory.search_regulatory_updates(
            agency="FDA",
            product_modality="biologic_type",
            limit=10,
        )
        _assert(invalid["error"]["code"] == "INVALID_PARAMETER", invalid)

        tfda = tools_regulatory.search_regulatory_updates(
            agency="TFDA",
            product_modality="biosimilar",
            limit=10,
        )
        _assert("error" not in tfda, tfda)
        _assert([r["id"] for r in tfda["records"]] == ["offline-tfda-biosimilar-1"], tfda)

        summary = {
            "status": "passed",
            "validated_cases": [
                "FDA product_modality string filter",
                "FDA product_modality list filter",
                "FDA product_modality no-result behavior",
                "invalid product_modality structured error",
                "TFDA product_modality filter",
                "query_metadata.filters_applied.product_modality",
            ],
            "important_interpretation": (
                "This offline smoke validates filter behavior only. "
                "It does not validate live FDA/TFDA source availability."
            ),
        }

        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        print("offline product modality regulatory search smoke passed")
        return summary

    finally:
        tools_regulatory.FDAUpdatesClient = original_fda
        tools_regulatory.TFDAUpdatesClient = original_tfda


if __name__ == "__main__":
    run_smoke()
