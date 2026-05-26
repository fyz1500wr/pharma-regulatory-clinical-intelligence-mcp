from __future__ import annotations

from dataclasses import asdict

from datetime import datetime, timezone

from src.connectors.fda.fda_updates_client import FDAUpdatesClient
from src.core.errors import ErrorCode, build_error
from src.core.normalization import normalize_fda_record


def search_regulatory_updates(**kwargs):
    agency = kwargs.get("agency")
    query = kwargs.get("query")
    if agency is None:
        agency = "FDA"
    agency = agency.strip().upper() if isinstance(agency, str) else agency

    if agency == "TFDA":
        return {"records": [], "no_result_reason": "DATA_NOT_INGESTED", "query_metadata": {"agency_searched": ["TFDA"], "sources_searched": [], "filters_applied": kwargs}}
    if agency != "FDA":
        return build_error(ErrorCode.INVALID_PARAMETER, f"Unsupported agency: {agency}")

    client = FDAUpdatesClient()
    raw = client.search_updates(query=query, limit=kwargs.get("limit", 20))
    retrieved_at = datetime.now(timezone.utc).isoformat()
    records = [asdict(normalize_fda_record(item, retrieved_at=retrieved_at)) for item in raw]

    metadata = {"agency_searched": ["FDA"], "sources_searched": ["FDA_GUIDANCE", "FDA_RSS"], "filters_applied": {"query": query, "limit": kwargs.get("limit", 20)}}
    if not records:
        return {"records": [], "no_result_reason": "NO_MATCHING_RECORDS", "query_metadata": metadata}
    known_limitations = []
    for rec in records:
        known_limitations.extend(rec.get("known_limitations", []))
    return {"records": records, "query_metadata": metadata, "known_limitations": sorted(set(known_limitations))}


def get_regulatory_document_detail(document_id: str, **kwargs):
    if not document_id:
        return build_error(ErrorCode.INVALID_PARAMETER, "document_id is required")
    return build_error(ErrorCode.DATA_NOT_INGESTED, "Document detail is not available in skeleton")


def compare_regulatory_updates(**kwargs):
    return build_error(ErrorCode.DATA_NOT_INGESTED, "compare_regulatory_updates is not implemented in MVP v1 skeleton", suggested_next_action="Implement after MVP v1 core tools stabilize and data is ingested.")
