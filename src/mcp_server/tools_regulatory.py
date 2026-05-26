from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone

from src.connectors.fda.fda_updates_client import FDAUpdatesClient
from src.connectors.tfda.tfda_updates_client import TFDAUpdatesClient
from src.core.errors import ErrorCode, build_error
from src.core.normalization import normalize_fda_record, normalize_tfda_record


_ALLOWED_SOURCE_TYPES = {
    "FDA": {"FDA_GUIDANCE", "FDA_RSS"},
    "TFDA": {"TFDA_HTML", "TFDA_JSON"},
}
_DEFAULT_SOURCE_TYPES = {
    "FDA": ["FDA_GUIDANCE", "FDA_RSS"],
    "TFDA": ["TFDA_HTML"],
}
_ALLOWED_DOCUMENT_STATUSES = {
    "FDA": {"draft", "final", "unknown"},
    "TFDA": {"published", "draft", "final", "unknown"},
}


def _parse_limit(value) -> int | dict:
    if value is None:
        return 20
    if isinstance(value, bool):
        return build_error(ErrorCode.INVALID_PARAMETER, "limit must be an integer between 1 and 100")
    try:
        limit = int(value)
    except Exception:
        return build_error(ErrorCode.INVALID_PARAMETER, "limit must be an integer between 1 and 100")
    if limit < 1 or limit > 100:
        return build_error(ErrorCode.INVALID_PARAMETER, "limit must be an integer between 1 and 100")
    return limit


def _parse_source_types(value, agency: str) -> list[str] | dict:
    if value is None:
        return list(_DEFAULT_SOURCE_TYPES[agency])
    if isinstance(value, str):
        source_types = [value]
    elif isinstance(value, list) and all(isinstance(item, str) for item in value):
        source_types = value
    else:
        return build_error(ErrorCode.INVALID_PARAMETER, "source_types must be a string or list of strings")

    normalized = [item.strip().upper() for item in source_types if item.strip()]
    invalid = sorted(set(normalized) - _ALLOWED_SOURCE_TYPES[agency])
    if invalid:
        return build_error(ErrorCode.INVALID_PARAMETER, f"Unsupported {agency} source_types: {invalid}")
    return normalized or list(_DEFAULT_SOURCE_TYPES[agency])


def _parse_iso_date(value, name: str):
    if value in (None, ""):
        return None
    if not isinstance(value, str):
        return build_error(ErrorCode.INVALID_PARAMETER, f"{name} must be YYYY-MM-DD")
    try:
        return datetime.fromisoformat(value).date().isoformat()
    except ValueError:
        return build_error(ErrorCode.INVALID_PARAMETER, f"{name} must be YYYY-MM-DD")


def _filter_records(records: list[dict], *, document_status: str | None, date_from: str | None, date_to: str | None) -> list[dict]:
    filtered = records
    if document_status:
        filtered = [record for record in filtered if str(record.get("document_status", "unknown")).lower() == document_status]
    if date_from:
        filtered = [record for record in filtered if record.get("publication_date") and record["publication_date"] >= date_from]
    if date_to:
        filtered = [record for record in filtered if record.get("publication_date") and record["publication_date"] <= date_to]
    return filtered


def search_regulatory_updates(**kwargs):
    agency = kwargs.get("agency")
    query = kwargs.get("query")
    if agency is None:
        agency = "FDA"

    if not isinstance(agency, str):
        return build_error(ErrorCode.INVALID_PARAMETER, "agency must be a string")

    agency = agency.strip().upper()

    if agency not in {"FDA", "TFDA"}:
        return build_error(ErrorCode.INVALID_PARAMETER, f"Unsupported agency: {agency}")

    limit = _parse_limit(kwargs.get("limit", 20))
    if isinstance(limit, dict) and "error" in limit:
        return limit

    source_types = _parse_source_types(kwargs.get("source_types"), agency)
    if isinstance(source_types, dict) and "error" in source_types:
        return source_types

    document_status = kwargs.get("document_status")
    if document_status is not None:
        if not isinstance(document_status, str):
            return build_error(
                ErrorCode.INVALID_PARAMETER,
                f"document_status must be one of {sorted(_ALLOWED_DOCUMENT_STATUSES[agency])}",
            )
        document_status = document_status.strip().lower()
        if document_status not in _ALLOWED_DOCUMENT_STATUSES[agency]:
            return build_error(
                ErrorCode.INVALID_PARAMETER,
                f"document_status must be one of {sorted(_ALLOWED_DOCUMENT_STATUSES[agency])}",
            )

    date_from = _parse_iso_date(kwargs.get("date_from"), "date_from")
    if isinstance(date_from, dict) and "error" in date_from:
        return date_from

    date_to = _parse_iso_date(kwargs.get("date_to"), "date_to")
    if isinstance(date_to, dict) and "error" in date_to:
        return date_to

    if date_from and date_to and date_from > date_to:
        return build_error(ErrorCode.INVALID_PARAMETER, "date_from must be earlier than or equal to date_to")

    client = FDAUpdatesClient() if agency == "FDA" else TFDAUpdatesClient()
    try:
        raw = client.search_updates(query=query, source_types=source_types, limit=limit)
    except Exception as exc:
        return build_error(
            ErrorCode.SOURCE_UNAVAILABLE,
            f"{agency} search failed: {exc}",
            suggested_next_action=f"Check {agency} connector runtime dependencies and source availability.",
        )

    if isinstance(raw, dict) and "error" in raw:
        return raw

    if not isinstance(raw, list):
        return build_error(
            ErrorCode.INTERNAL_ERROR,
            f"{agency} search returned an unexpected response shape",
            details=f"Received type: {type(raw).__name__}",
            suggested_next_action=f"Update {agency} search_updates to return a list of records or a structured error.",
        )

    raw = _filter_records(raw, document_status=document_status, date_from=date_from, date_to=date_to)

    retrieved_at = datetime.now(timezone.utc).isoformat()
    normalizer = normalize_fda_record if agency == "FDA" else normalize_tfda_record
    records = [asdict(normalizer(item, retrieved_at=retrieved_at)) for item in raw]

    metadata = {
        "agency_searched": [agency],
        "sources_searched": source_types,
        "filters_applied": {
            "query": query,
            "limit": limit,
            "source_types": source_types,
            "document_status": document_status,
            "date_from": date_from,
            "date_to": date_to,
        },
    }

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
    return build_error(
        ErrorCode.DATA_NOT_INGESTED,
        "compare_regulatory_updates is not implemented in MVP v1 skeleton",
        suggested_next_action="Implement after MVP v1 core tools stabilize and data is ingested.",
    )
