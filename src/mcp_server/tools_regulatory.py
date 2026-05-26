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


def _parse_detail_agencies(value) -> list[str] | dict:
    if value in (None, ""):
        return ["FDA", "TFDA"]

    if not isinstance(value, str):
        return build_error(ErrorCode.INVALID_PARAMETER, "agency must be FDA or TFDA")

    agency = value.strip().upper()
    if agency not in {"FDA", "TFDA"}:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            f"Unsupported agency for document detail: {agency}",
            suggested_next_action="Use agency='FDA' or agency='TFDA'.",
        )
    return [agency]


def _record_matches_document_id(record: dict, document_id: str) -> bool:
    document_id = document_id.strip()

    candidate_values = [
        record.get("id"),
        record.get("content_hash"),
        record.get("official_url"),
        record.get("title"),
    ]

    return any(str(value).strip() == document_id for value in candidate_values if value is not None)


def _document_detail_payload(record: dict) -> dict:
    known_limitations = list(record.get("known_limitations", []))
    known_limitations.append(
        "MVP v1 document detail is reconstructed from normalized search result metadata; full document body and attachment parsing are not yet implemented."
    )

    return {
        "document": {
            "id": record.get("id", ""),
            "agency": record.get("agency", ""),
            "title": record.get("title", ""),
            "original_language": "unknown",
            "translated_title": "",
            "publication_date": record.get("publication_date"),
            "last_update_date": record.get("last_update_date"),
            "effective_date": None,
            "consultation_deadline": None,
            "document_type": record.get("document_type", "unknown"),
            "document_status": record.get("document_status", "unknown"),
            "official_url": record.get("official_url", ""),
            "attachment_urls": [],
            "source_type": record.get("source_type", "unknown"),
            "retrieved_at": record.get("retrieved_at"),
            "content_hash": record.get("content_hash"),
            "product_modality": record.get("product_modality", ["unknown"]),
            "topics": record.get("topics", ["unknown"]),
            "summary": record.get("summary", ""),
            "impact_assessment": {
                "impact_level": "unknown",
                "impacted_functions": [],
                "eCTD_module_mapping": [],
                "rationale": "Impact assessment is not implemented in MVP v1 skeleton-backed document detail.",
            },
            "classification_notes": "Skeleton-backed detail uses normalized search metadata only.",
            "known_limitations": sorted(set(known_limitations)),
        }
    }


def get_regulatory_document_detail(document_id: str, **kwargs):
    if not isinstance(document_id, str) or not document_id.strip():
        return build_error(ErrorCode.INVALID_PARAMETER, "document_id is required")

    agencies = _parse_detail_agencies(kwargs.get("agency"))
    if isinstance(agencies, dict) and "error" in agencies:
        return agencies

    if kwargs.get("source_types") is not None and len(agencies) > 1:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            "source_types can only be used when agency is specified",
            suggested_next_action="Pass agency='FDA' or agency='TFDA' when filtering source_types.",
        )

    limit = _parse_limit(kwargs.get("limit", 100))
    if isinstance(limit, dict) and "error" in limit:
        return limit

    retrieved_at = datetime.now(timezone.utc).isoformat()
    checked_agencies = []
    checked_source_types = []

    for agency in agencies:
        source_types = _parse_source_types(kwargs.get("source_types"), agency)
        if isinstance(source_types, dict) and "error" in source_types:
            return source_types

        checked_agencies.append(agency)
        checked_source_types.extend(source_types)

        client = FDAUpdatesClient() if agency == "FDA" else TFDAUpdatesClient()
        try:
            raw = client.search_updates(query=document_id.strip(), source_types=source_types, limit=limit)
        except Exception as exc:
            return build_error(
                ErrorCode.SOURCE_UNAVAILABLE,
                f"{agency} document detail lookup failed: {exc}",
                suggested_next_action=f"Check {agency} connector runtime dependencies and source availability.",
            )

        if isinstance(raw, dict) and "error" in raw:
            return raw

        if not isinstance(raw, list):
            return build_error(
                ErrorCode.INTERNAL_ERROR,
                f"{agency} document detail lookup returned an unexpected response shape",
                details=f"Received type: {type(raw).__name__}",
                suggested_next_action=f"Update {agency} search_updates to return a list of records or a structured error.",
            )

        normalizer = normalize_fda_record if agency == "FDA" else normalize_tfda_record
        records = [asdict(normalizer(item, retrieved_at=retrieved_at)) for item in raw]

        for record in records:
            if _record_matches_document_id(record, document_id):
                payload = _document_detail_payload(record)
                payload["query_metadata"] = {
                    "document_id": document_id.strip(),
                    "agencies_checked": checked_agencies,
                    "sources_checked": sorted(set(checked_source_types)),
                    "lookup_mode": "skeleton_backed_search_metadata",
                    "known_limitations": [
                        "No persistent document detail store is implemented in MVP v1.",
                        "Detail response is reconstructed from normalized connector search result metadata.",
                    ],
                }
                return payload

    return build_error(
        ErrorCode.NO_RESULTS,
        f"Document detail not found for document_id: {document_id.strip()}",
        details={
            "document_id": document_id.strip(),
            "agencies_checked": checked_agencies,
            "sources_checked": sorted(set(checked_source_types)),
        },
        suggested_next_action=(
            "Verify the document_id came from search_regulatory_updates records, or rerun search_regulatory_updates "
            "and pass the exact record id, content_hash, official_url, or title."
        ),
    )


def compare_regulatory_updates(**kwargs):
    return build_error(
        ErrorCode.DATA_NOT_INGESTED,
        "compare_regulatory_updates is not implemented in MVP v1 skeleton",
        suggested_next_action="Implement after MVP v1 core tools stabilize and data is ingested.",
    )
