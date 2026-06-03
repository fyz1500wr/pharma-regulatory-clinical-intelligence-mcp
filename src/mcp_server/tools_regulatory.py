from __future__ import annotations

import calendar
from dataclasses import asdict
from datetime import datetime, timedelta, timezone

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
_ALLOWED_PRODUCT_MODALITIES = {
    "small_molecule",
    "peptide",
    "oligonucleotide",
    "mrna_rna",
    "antibody",
    "adc",
    "recombinant_protein",
    "biosimilar",
    "vaccine",
    "cell_therapy",
    "gene_therapy",
    "radiopharmaceutical",
    "combination_product",
    "unknown",
    "requires_manual_review",
}
_PRODUCT_MODALITY_FILTER_LIMITATION = (
    "Product modality filtering is based on MVP keyword/metadata classification and may require manual verification."
)
_ALLOWED_DATE_RANGES = {"1m", "3m", "6m", "1y", "3y", "5y", "custom"}


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



def _parse_product_modality(value) -> list[str] | None | dict:
    if value in (None, ""):
        return None
    if isinstance(value, str):
        modalities = [value]
    elif isinstance(value, list) and all(isinstance(item, str) for item in value):
        modalities = value
    else:
        return build_error(ErrorCode.INVALID_PARAMETER, "product_modality must be a string or list of strings")

    normalized = [item.strip().lower() for item in modalities if item.strip()]
    invalid = sorted(set(normalized) - _ALLOWED_PRODUCT_MODALITIES)
    if invalid:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            f"Unsupported product_modality: {invalid}",
            details=f"Supported product_modality labels: {sorted(_ALLOWED_PRODUCT_MODALITIES)}",
            suggested_next_action="Use product_modality labels from docs/product_modality_taxonomy.md.",
        )
    return normalized or None


def _record_product_modalities(record: dict) -> set[str]:
    value = record.get("product_modality", [])
    if isinstance(value, str):
        values = [value]
    elif isinstance(value, list):
        values = value
    else:
        values = []
    return {str(item).strip().lower() for item in values if str(item).strip()}


def _filter_records_by_product_modality(records: list[dict], product_modality: list[str] | None) -> list[dict]:
    if not product_modality:
        return records
    requested = set(product_modality)
    return [record for record in records if _record_product_modalities(record) & requested]


def _parse_iso_date(value, name: str):
    if value in (None, ""):
        return None
    if not isinstance(value, str):
        return build_error(ErrorCode.INVALID_PARAMETER, f"{name} must be YYYY-MM-DD")
    try:
        return datetime.fromisoformat(value).date().isoformat()
    except ValueError:
        return build_error(ErrorCode.INVALID_PARAMETER, f"{name} must be YYYY-MM-DD")



def _subtract_months(date_value, months: int):
    month_index = date_value.month - 1 - months
    year = date_value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(date_value.day, calendar.monthrange(year, month)[1])
    return date_value.replace(year=year, month=month, day=day)


def _parse_date_range_value(value) -> str | None | dict:
    if value in (None, ""):
        return None
    if not isinstance(value, str):
        return build_error(ErrorCode.INVALID_PARAMETER, "date_range must be one of 1m, 3m, 6m, 1y, 3y, 5y, custom")
    normalized = value.strip().lower()
    if normalized not in _ALLOWED_DATE_RANGES:
        return build_error(ErrorCode.INVALID_PARAMETER, "date_range must be one of 1m, 3m, 6m, 1y, 3y, 5y, custom")
    return normalized


def _resolve_date_filters(
    *,
    date_from: str | None,
    date_to: str | None,
    date_range,
    custom_date_range,
) -> tuple[str | None, str | None, str | None, dict | None] | dict:
    if custom_date_range not in (None, "") and date_range in (None, ""):
        date_range = "custom"

    parsed_date_range = _parse_date_range_value(date_range)
    if isinstance(parsed_date_range, dict) and "error" in parsed_date_range:
        return parsed_date_range

    if parsed_date_range is None:
        if custom_date_range not in (None, ""):
            return build_error(
                ErrorCode.INVALID_PARAMETER,
                "custom_date_range can only be used with date_range='custom'",
            )
        return date_from, date_to, None, None

    if date_from or date_to:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            "date_range/custom_date_range cannot be combined with date_from or date_to",
            suggested_next_action="Use either date_range/custom_date_range or explicit date_from/date_to.",
        )

    if parsed_date_range == "custom":
        if not isinstance(custom_date_range, dict):
            return build_error(
                ErrorCode.INVALID_PARAMETER,
                "custom_date_range must be an object with start_date and end_date when date_range='custom'",
            )

        start_date = _parse_iso_date(custom_date_range.get("start_date"), "custom_date_range.start_date")
        if isinstance(start_date, dict) and "error" in start_date:
            return start_date

        end_date = _parse_iso_date(custom_date_range.get("end_date"), "custom_date_range.end_date")
        if isinstance(end_date, dict) and "error" in end_date:
            return end_date

        if not start_date or not end_date:
            return build_error(
                ErrorCode.INVALID_PARAMETER,
                "custom_date_range requires both start_date and end_date",
            )

        if start_date > end_date:
            return build_error(
                ErrorCode.INVALID_PARAMETER,
                "custom_date_range.start_date must be earlier than or equal to custom_date_range.end_date",
            )

        return start_date, end_date, "custom", {"start_date": start_date, "end_date": end_date}

    if custom_date_range not in (None, ""):
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            "custom_date_range can only be used with date_range='custom'",
        )

    today = datetime.now(timezone.utc).date()
    months_by_range = {
        "1m": 1,
        "3m": 3,
        "6m": 6,
        "1y": 12,
        "3y": 36,
        "5y": 60,
    }
    start = _subtract_months(today, months_by_range[parsed_date_range])
    return start.isoformat(), today.isoformat(), parsed_date_range, None


def _filter_records(records: list[dict], *, document_status: str | None, date_from: str | None, date_to: str | None) -> list[dict]:
    filtered = records
    if document_status:
        filtered = [record for record in filtered if str(record.get("document_status", "unknown")).lower() == document_status]
    if date_from:
        filtered = [record for record in filtered if record.get("publication_date") and record["publication_date"] >= date_from]
    if date_to:
        filtered = [record for record in filtered if record.get("publication_date") and record["publication_date"] <= date_to]
    return filtered


def _parse_search_agency(agency, agencies) -> str | dict:
    if agency not in (None, "") and agencies not in (None, ""):
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            "Use either agency or agencies, not both",
            suggested_next_action="Pass agency='TFDA' or agencies=['TFDA'], but not both.",
        )

    if agencies not in (None, ""):
        if isinstance(agencies, str):
            values = [agencies]
        elif isinstance(agencies, list) and all(isinstance(item, str) for item in agencies):
            values = agencies
        else:
            return build_error(ErrorCode.INVALID_PARAMETER, "agencies must be a string or list of strings")

        normalized = [item.strip().upper() for item in values if item.strip()]
        if not normalized:
            return build_error(ErrorCode.INVALID_PARAMETER, "agencies must include FDA or TFDA")
        if len(normalized) != 1:
            return build_error(
                ErrorCode.INVALID_PARAMETER,
                "search_regulatory_updates currently supports exactly one agency",
                suggested_next_action="Use compare_regulatory_updates for multi-agency comparisons.",
            )

        agency = normalized[0]

    if agency in (None, ""):
        agency = "FDA"

    if not isinstance(agency, str):
        return build_error(ErrorCode.INVALID_PARAMETER, "agency must be a string")

    normalized_agency = agency.strip().upper()

    if normalized_agency not in {"FDA", "TFDA"}:
        return build_error(ErrorCode.INVALID_PARAMETER, f"Unsupported agency: {normalized_agency}")

    return normalized_agency

def search_regulatory_updates(**kwargs):
    agency = _parse_search_agency(kwargs.get("agency"), kwargs.get("agencies"))
    query = kwargs.get("query")
    if isinstance(agency, dict) and "error" in agency:
        return agency

    limit = _parse_limit(kwargs.get("limit", 20))
    if isinstance(limit, dict) and "error" in limit:
        return limit

    source_types = _parse_source_types(kwargs.get("source_types"), agency)
    if isinstance(source_types, dict) and "error" in source_types:
        return source_types

    product_modality = _parse_product_modality(kwargs.get("product_modality"))
    if isinstance(product_modality, dict) and "error" in product_modality:
        return product_modality

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

    resolved_dates = _resolve_date_filters(
        date_from=date_from,
        date_to=date_to,
        date_range=kwargs.get("date_range"),
        custom_date_range=kwargs.get("custom_date_range"),
    )
    if isinstance(resolved_dates, dict) and "error" in resolved_dates:
        return resolved_dates
    date_from, date_to, normalized_date_range, normalized_custom_date_range = resolved_dates

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
    records = _filter_records_by_product_modality(records, product_modality)

    metadata = {
        "agency_searched": [agency],
        "sources_searched": source_types,
        "filters_applied": {
            "query": query,
            "limit": limit,
            "source_types": source_types,
            "product_modality": product_modality,
            "document_status": document_status,
            "date_range": normalized_date_range,
            "custom_date_range": normalized_custom_date_range,
            "date_from": date_from,
            "date_to": date_to,
        },
    }

    if not records:
        payload = {"records": [], "no_result_reason": "NO_MATCHING_RECORDS", "query_metadata": metadata}
        if product_modality:
            payload["known_limitations"] = [_PRODUCT_MODALITY_FILTER_LIMITATION]
        return payload

    known_limitations = []
    for rec in records:
        known_limitations.extend(rec.get("known_limitations", []))
    if product_modality:
        known_limitations.append(_PRODUCT_MODALITY_FILTER_LIMITATION)

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


def _lookup_failure(
    agency: str,
    *,
    code: str,
    message: str,
    details="",
    suggested_next_action: str = "",
) -> dict:
    return {
        "agency": agency,
        "code": code,
        "message": message,
        "details": details,
        "suggested_next_action": suggested_next_action,
    }


def _lookup_failure_from_error_response(agency: str, response: dict) -> dict:
    error = response.get("error", {})
    return _lookup_failure(
        agency,
        code=error.get("code", ErrorCode.SOURCE_UNAVAILABLE.value),
        message=error.get("message", f"{agency} lookup returned a structured error"),
        details=error.get("details", ""),
        suggested_next_action=error.get("suggested_next_action", ""),
    )


def _add_partial_failure_metadata(payload: dict, lookup_failures: list[dict]) -> dict:
    payload["query_metadata"]["partial_lookup_failures"] = lookup_failures

    if lookup_failures:
        limitations = list(payload["document"].get("known_limitations", []))
        limitations.append("Document detail lookup completed with partial source failures.")
        payload["document"]["known_limitations"] = sorted(set(limitations))

    return payload


def get_regulatory_document_detail(document_id: str, **kwargs):
    if not isinstance(document_id, str) or not document_id.strip():
        return build_error(ErrorCode.INVALID_PARAMETER, "document_id is required")

    agencies = _parse_detail_agencies(kwargs.get("agency"))
    if isinstance(agencies, dict) and "error" in agencies:
        return agencies

    single_agency_lookup = kwargs.get("agency") not in (None, "")

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
    lookup_failures = []

    for agency in agencies:
        source_types = _parse_source_types(kwargs.get("source_types"), agency)
        if isinstance(source_types, dict) and "error" in source_types:
            return source_types

        checked_agencies.append(agency)
        checked_source_types.extend(source_types)

        client = FDAUpdatesClient() if agency == "FDA" else TFDAUpdatesClient()
        try:
            raw = client.search_updates(query=None, source_types=source_types, limit=limit)
        except Exception as exc:
            error = build_error(
                ErrorCode.SOURCE_UNAVAILABLE,
                f"{agency} document detail lookup failed: {exc}",
                suggested_next_action=f"Check {agency} connector runtime dependencies and source availability.",
            )
            if single_agency_lookup:
                return error
            lookup_failures.append(_lookup_failure_from_error_response(agency, error))
            continue

        if isinstance(raw, dict) and "error" in raw:
            if single_agency_lookup:
                return raw
            lookup_failures.append(_lookup_failure_from_error_response(agency, raw))
            continue

        if not isinstance(raw, list):
            error = build_error(
                ErrorCode.INTERNAL_ERROR,
                f"{agency} document detail lookup returned an unexpected response shape",
                details=f"Received type: {type(raw).__name__}",
                suggested_next_action=f"Update {agency} search_updates to return a list of records or a structured error.",
            )
            if single_agency_lookup:
                return error
            lookup_failures.append(_lookup_failure_from_error_response(agency, error))
            continue

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
                return _add_partial_failure_metadata(payload, lookup_failures)

    error_details = {
        "document_id": document_id.strip(),
        "agencies_checked": checked_agencies,
        "sources_checked": sorted(set(checked_source_types)),
        "partial_lookup_failures": lookup_failures,
    }

    if lookup_failures and len(lookup_failures) == len(agencies):
        failure_codes = {failure.get("code") for failure in lookup_failures}
        if failure_codes == {ErrorCode.SOURCE_UNAVAILABLE.value}:
            return build_error(
                ErrorCode.SOURCE_UNAVAILABLE,
                f"Document detail lookup failed for all requested agencies: {document_id.strip()}",
                details=error_details,
                suggested_next_action="Check source health before retrying document detail lookup.",
            )

        return build_error(
            ErrorCode.INTERNAL_ERROR,
            f"Document detail lookup encountered non-source-availability failures for all requested agencies: {document_id.strip()}",
            details=error_details,
            suggested_next_action=(
                "Inspect connector response shapes and error codes before treating this as a transient source outage."
            ),
        )

    if lookup_failures:
        return build_error(
            ErrorCode.PARTIAL_RESULTS,
            f"Document detail not found for document_id after partial lookup failures: {document_id.strip()}",
            details=error_details,
            suggested_next_action=(
                "At least one agency failed during lookup. Check source health, then retry with a specific agency "
                "or rerun search_regulatory_updates to refresh candidate document IDs."
            ),
        )

    return build_error(
        ErrorCode.NO_RESULTS,
        f"Document detail not found for document_id: {document_id.strip()}",
        details=error_details,
        suggested_next_action=(
            "Verify the document_id came from search_regulatory_updates records, or rerun search_regulatory_updates "
            "and pass the exact record id, content_hash, official_url, or title."
        ),
    )

_COMPARE_AXES = {"agency", "topic", "product_modality", "document_status"}
_DATE_RANGE_DAYS = {
    "1m": 30,
    "3m": 90,
    "6m": 180,
    "1y": 365,
    "3y": 1095,
    "5y": 1825,
}


def _parse_compare_agencies(value) -> list[str] | dict:
    if value in (None, ""):
        return ["FDA", "TFDA"]

    if isinstance(value, str):
        raw_agencies = [value]
    elif isinstance(value, list) and all(isinstance(item, str) for item in value):
        raw_agencies = value
    else:
        return build_error(ErrorCode.INVALID_PARAMETER, "agencies must be a string or list of strings")

    agencies = []
    for item in raw_agencies:
        agency = item.strip().upper()
        if not agency:
            continue
        if agency not in {"FDA", "TFDA"}:
            return build_error(
                ErrorCode.INVALID_PARAMETER,
                f"Unsupported agency for MVP v1 comparison: {agency}",
                suggested_next_action="Use MVP v1 active agencies only: FDA and TFDA.",
            )
        if agency not in agencies:
            agencies.append(agency)

    return agencies or ["FDA", "TFDA"]


def _parse_compare_axis(value) -> str | dict:
    if value in (None, ""):
        return "agency"
    if not isinstance(value, str):
        return build_error(ErrorCode.INVALID_PARAMETER, "comparison_axis must be a string")
    axis = value.strip().lower()
    if axis not in _COMPARE_AXES:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            f"Unsupported comparison_axis: {axis}",
            suggested_next_action=f"Use one of: {sorted(_COMPARE_AXES)}.",
        )
    return axis


def _parse_compare_values(value, name: str) -> list[str] | dict:
    if value in (None, ""):
        return []

    if isinstance(value, str):
        values = [value]
    elif isinstance(value, list) and all(isinstance(item, str) for item in value):
        values = value
    else:
        return build_error(ErrorCode.INVALID_PARAMETER, f"{name} must be a string or list of strings")

    normalized = [item.strip() for item in values if item.strip()]
    return normalized


def _parse_compare_query(kwargs) -> str | None | dict:
    query = kwargs.get("query")
    keywords = kwargs.get("keywords")

    if query not in (None, ""):
        if not isinstance(query, str):
            return build_error(ErrorCode.INVALID_PARAMETER, "query must be a string")
        return query.strip() or None

    if keywords in (None, ""):
        return None

    if isinstance(keywords, str):
        return keywords.strip() or None

    if isinstance(keywords, list) and all(isinstance(item, str) for item in keywords):
        joined = " ".join(item.strip() for item in keywords if item.strip())
        return joined or None

    return build_error(ErrorCode.INVALID_PARAMETER, "keywords must be a string or list of strings")


def _resolve_compare_dates(kwargs) -> dict:
    custom_date_range = kwargs.get("custom_date_range") or {}
    if custom_date_range and not isinstance(custom_date_range, dict):
        return build_error(ErrorCode.INVALID_PARAMETER, "custom_date_range must be an object")

    date_from_value = kwargs.get("date_from") or kwargs.get("start_date") or custom_date_range.get("start_date")
    date_to_value = kwargs.get("date_to") or kwargs.get("end_date") or custom_date_range.get("end_date")
    date_range = kwargs.get("date_range")

    if date_range not in (None, "", "custom"):
        if not isinstance(date_range, str):
            return build_error(ErrorCode.INVALID_PARAMETER, "date_range must be a string")
        normalized_range = date_range.strip().lower()
        if normalized_range not in _DATE_RANGE_DAYS:
            return build_error(
                ErrorCode.INVALID_PARAMETER,
                f"date_range must be one of {sorted(_DATE_RANGE_DAYS) + ['custom']}",
            )
        today = datetime.now(timezone.utc).date()
        date_to_value = date_to_value or today.isoformat()
        date_from_value = date_from_value or (today - timedelta(days=_DATE_RANGE_DAYS[normalized_range])).isoformat()
        date_range = normalized_range
    elif date_range == "custom":
        date_range = "custom"
    else:
        date_range = "custom" if date_from_value or date_to_value else None

    date_from = _parse_iso_date(date_from_value, "date_from")
    if isinstance(date_from, dict) and "error" in date_from:
        return date_from

    date_to = _parse_iso_date(date_to_value, "date_to")
    if isinstance(date_to, dict) and "error" in date_to:
        return date_to

    if date_from and date_to and date_from > date_to:
        return build_error(ErrorCode.INVALID_PARAMETER, "date_from must be earlier than or equal to date_to")

    return {"date_range": date_range, "date_from": date_from, "date_to": date_to}


def _as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _lower_set(values: list[str]) -> set[str]:
    return {str(value).strip().lower() for value in values if str(value).strip()}


def _record_matches_compare_filters(
    record: dict,
    *,
    product_modality: list[str],
    topics: list[str],
    document_status: list[str],
) -> bool:
    if product_modality and not (_lower_set(_as_list(record.get("product_modality"))) & _lower_set(product_modality)):
        return False

    if topics and not (_lower_set(_as_list(record.get("topics"))) & _lower_set(topics)):
        return False

    if document_status and str(record.get("document_status", "unknown")).strip().lower() not in _lower_set(document_status):
        return False

    return True


def _top_record_values(records: list[dict], field: str, limit: int = 5) -> list[str]:
    counts = {}
    labels = {}
    for record in records:
        for value in _as_list(record.get(field)):
            label = str(value).strip()
            if not label:
                continue
            key = label.lower()
            counts[key] = counts.get(key, 0) + 1
            labels.setdefault(key, label)

    ranked = sorted(counts, key=lambda key: (-counts[key], labels[key].lower()))
    return [labels[key] for key in ranked[:limit]]


def _compare_key_update(record: dict) -> dict:
    return {
        "id": record.get("id", ""),
        "agency": record.get("agency", ""),
        "title": record.get("title", ""),
        "publication_date": record.get("publication_date"),
        "official_url": record.get("official_url", ""),
        "impact_level": record.get("impact_level", "unknown"),
        "document_status": record.get("document_status", "unknown"),
        "summary": record.get("summary", ""),
    }


def _compare_known_limitations(records: list[dict], extra_limitations: list[str] | None = None) -> list[str]:
    limitations = list(extra_limitations or [])
    limitations.append("Skeleton-backed comparison uses normalized regulatory search metadata only.")
    limitations.append("Comparison output is descriptive and does not establish agency equivalence or final regulatory interpretation.")

    for record in records:
        limitations.extend(record.get("known_limitations", []))

    return sorted(set(limitations))


def _compare_entry(axis: str, value: str, records: list[dict], *, agency: str | None = None) -> dict:
    sorted_records = sorted(
        records,
        key=lambda record: (record.get("publication_date") or "", record.get("title") or ""),
        reverse=True,
    )
    agencies = sorted({record.get("agency", "") for record in records if record.get("agency")})
    if agency and agency not in agencies:
        agencies = [agency] + agencies

    if axis == "agency":
        notes = (
            [f"{value}: {len(records)} matching normalized update(s)."]
            if records
            else [f"{value}: no matching normalized updates found for the selected filters."]
        )
        agency_value = value
    else:
        notes = [f"Includes agencies: {', '.join(agencies) if agencies else 'none'}."]
        agency_value = "multiple"

    return {
        "comparison_axis": axis,
        "comparison_value": value,
        "agency": agency_value,
        "agencies": agencies,
        "record_count": len(records),
        "key_updates": [_compare_key_update(record) for record in sorted_records[:5]],
        "common_themes": _top_record_values(records, "topics"),
        "agency_specific_notes": notes,
        "known_limitations": _compare_known_limitations(records),
    }


def _build_comparison(axis: str, records: list[dict], successful_agencies: list[str]) -> list[dict]:
    if axis == "agency":
        by_agency = {agency: [] for agency in successful_agencies}
        for record in records:
            agency = record.get("agency", "unknown")
            by_agency.setdefault(agency, []).append(record)
        return [_compare_entry(axis, agency, by_agency.get(agency, []), agency=agency) for agency in successful_agencies]

    field_map = {
        "topic": "topics",
        "product_modality": "product_modality",
        "document_status": "document_status",
    }
    field = field_map[axis]
    grouped = {}
    for record in records:
        values = _as_list(record.get(field)) or ["unknown"]
        for value in values:
            label = str(value).strip() or "unknown"
            grouped.setdefault(label, []).append(record)

    return [_compare_entry(axis, value, grouped[value]) for value in sorted(grouped, key=lambda item: item.lower())]


def _build_compare_summary(
    records: list[dict],
    successful_agencies: list[str],
    lookup_failures: list[dict],
) -> dict:
    agency_counts = {agency: 0 for agency in successful_agencies}
    for record in records:
        agency = record.get("agency")
        if agency:
            agency_counts[agency] = agency_counts.get(agency, 0) + 1

    recommended_follow_up = []
    if lookup_failures:
        recommended_follow_up.append("Run check_source_health for agencies with partial lookup failures before relying on the comparison.")
    if records:
        recommended_follow_up.append("Use get_regulatory_document_detail for any key update before making regulatory or CMC decisions.")
    else:
        recommended_follow_up.append("Relax filters or rerun search_regulatory_updates to identify candidate documents.")
    recommended_follow_up.append("Perform manual regulatory review before treating this comparison as final agency requirement mapping.")

    return {
        "overall_themes": _top_record_values(records, "topics") or _top_record_values(records, "product_modality"),
        "major_differences": [f"{agency}: {count} matching update(s)" for agency, count in agency_counts.items()],
        "recommended_follow_up": recommended_follow_up,
    }


def compare_regulatory_updates(**kwargs):
    agencies = _parse_compare_agencies(kwargs.get("agencies", kwargs.get("agency")))
    if isinstance(agencies, dict) and "error" in agencies:
        return agencies

    axis = _parse_compare_axis(kwargs.get("comparison_axis"))
    if isinstance(axis, dict) and "error" in axis:
        return axis

    query = _parse_compare_query(kwargs)
    if isinstance(query, dict) and "error" in query:
        return query

    product_modality = _parse_compare_values(kwargs.get("product_modality"), "product_modality")
    if isinstance(product_modality, dict) and "error" in product_modality:
        return product_modality

    topics = _parse_compare_values(kwargs.get("topics"), "topics")
    if isinstance(topics, dict) and "error" in topics:
        return topics

    document_status = _parse_compare_values(kwargs.get("document_status"), "document_status")
    if isinstance(document_status, dict) and "error" in document_status:
        return document_status

    limit = _parse_limit(kwargs.get("limit", 20))
    if isinstance(limit, dict) and "error" in limit:
        return limit

    dates = _resolve_compare_dates(kwargs)
    if isinstance(dates, dict) and "error" in dates:
        return dates

    lookup_failures = []
    successful_agencies = []
    records = []
    known_limitations = []

    for agency in agencies:
        result = search_regulatory_updates(
            agency=agency,
            query=query,
            limit=limit,
            date_from=dates["date_from"],
            date_to=dates["date_to"],
        )

        if isinstance(result, dict) and "error" in result:
            if len(agencies) == 1:
                return result
            lookup_failures.append(_lookup_failure_from_error_response(agency, result))
            continue

        if not isinstance(result, dict):
            error = build_error(
                ErrorCode.INTERNAL_ERROR,
                f"{agency} comparison lookup returned an unexpected response shape",
                details=f"Received type: {type(result).__name__}",
            )
            if len(agencies) == 1:
                return error
            lookup_failures.append(_lookup_failure_from_error_response(agency, error))
            continue

        agency_records = result.get("records", [])
        if not isinstance(agency_records, list):
            error = build_error(
                ErrorCode.INTERNAL_ERROR,
                f"{agency} comparison records returned an unexpected response shape",
                details=f"Received records type: {type(agency_records).__name__}",
            )
            if len(agencies) == 1:
                return error
            lookup_failures.append(_lookup_failure_from_error_response(agency, error))
            continue

        successful_agencies.append(agency)
        known_limitations.extend(result.get("known_limitations", []))

        filtered_records = [
            record
            for record in agency_records
            if _record_matches_compare_filters(
                record,
                product_modality=product_modality,
                topics=topics,
                document_status=document_status,
            )
        ]
        records.extend(filtered_records)

    error_details = {
        "agencies_checked": agencies,
        "successful_agencies": successful_agencies,
        "partial_lookup_failures": lookup_failures,
    }

    if lookup_failures and len(lookup_failures) == len(agencies):
        failure_codes = {failure.get("code") for failure in lookup_failures}
        if failure_codes == {ErrorCode.SOURCE_UNAVAILABLE.value}:
            return build_error(
                ErrorCode.SOURCE_UNAVAILABLE,
                "compare_regulatory_updates failed for all requested agencies",
                details=error_details,
                suggested_next_action="Run check_source_health before retrying the comparison.",
            )

        return build_error(
            ErrorCode.INTERNAL_ERROR,
            "compare_regulatory_updates encountered non-source-availability failures for all requested agencies",
            details=error_details,
            suggested_next_action="Inspect connector response shapes and error codes before treating this as a transient source outage.",
        )

    comparison = _build_comparison(axis, records, successful_agencies)

    return {
        "comparison": comparison,
        "comparison_summary": _build_compare_summary(records, successful_agencies, lookup_failures),
        "query_metadata": {
            "agencies_checked": agencies,
            "successful_agencies": successful_agencies,
            "comparison_axis": axis,
            "filters_applied": {
                "query": query,
                "keywords": kwargs.get("keywords"),
                "date_range": dates["date_range"],
                "date_from": dates["date_from"],
                "date_to": dates["date_to"],
                "product_modality": product_modality,
                "topics": topics,
                "document_status": document_status,
                "limit_per_agency": limit,
            },
            "lookup_mode": "skeleton_backed_search_metadata",
            "partial_lookup_failures": lookup_failures,
            "known_limitations": _compare_known_limitations(records, known_limitations),
        },
    }
