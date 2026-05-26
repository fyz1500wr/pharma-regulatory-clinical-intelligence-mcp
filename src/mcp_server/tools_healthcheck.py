from __future__ import annotations

from typing import Any

from src.core.errors import ErrorCode, build_error
from src.mcp_server.tools_source_health import check_source_health as _check_source_health_impl


_ENDPOINTS = {
    "FDA": "https://www.fda.gov",
    "TFDA": "https://www.fda.gov.tw",
    "ClinicalTrials.gov": "https://clinicaltrials.gov",
}

_SOURCE_IDS = {
    "FDA": "FDA_connector",
    "TFDA": "TFDA_connector",
    "ClinicalTrials.gov": "ClinicalTrialsGov_API",
}

_CONNECTOR_FILES = {
    "FDA": "src/connectors/fda/fda_updates_client.py",
    "TFDA": "src/connectors/tfda/tfda_updates_client.py",
    "ClinicalTrials.gov": "src/connectors/clinical_trials/clinicaltrials_gov_client.py",
}


def _as_source_list(value: Any) -> list[str] | dict | None:
    if value is None:
        return None

    if isinstance(value, str):
        if not value.strip():
            return build_error(ErrorCode.INVALID_PARAMETER, "sources must contain non-empty strings")
        return [value]

    if isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value):
        return value

    return build_error(ErrorCode.INVALID_PARAMETER, "sources must be a string or list of non-empty strings")


def _status_for_contract(item: dict[str, Any]) -> str:
    if item.get("available") is True:
        return "pass"
    if item.get("available") is False:
        return "failed"
    return "unknown"


def _failure_type_for_contract(item: dict[str, Any]) -> str:
    if item.get("available") is True:
        return ""

    source_type = item.get("source_type")
    if source_type == "clinical_trials_registry":
        return "api_status"
    if source_type == "regulatory":
        return "unknown"
    return "unknown"


def _severity_for_contract(item: dict[str, Any]) -> str:
    if item.get("available") is True:
        return "low"

    error_code = item.get("error_code")
    if error_code == "INTERNAL_ERROR":
        return "high"
    if error_code == "SOURCE_UNAVAILABLE":
        return "high"
    return "medium"


def _to_contract_health_item(item: dict[str, Any]) -> dict[str, Any]:
    source = item.get("source", "unknown")
    checked_at = item.get("retrieved_at")

    return {
        "source_id": _SOURCE_IDS.get(source, source),
        "agency_or_registry": source,
        "source_type": item.get("source_type", "unknown"),
        "endpoint_url": _ENDPOINTS.get(source, ""),
        "status": _status_for_contract(item),
        "last_successful_check": checked_at if item.get("available") is True else None,
        "last_checked_at": checked_at,
        "failure_type": _failure_type_for_contract(item),
        "error_message": item.get("message", ""),
        "suggested_fix": item.get("suggested_next_action", ""),
        "suggested_connector_file": _CONNECTOR_FILES.get(source, ""),
        "severity": _severity_for_contract(item),
        "known_limitations": item.get("known_limitations", []),
    }


def _shape_contract_response(raw: dict[str, Any]) -> dict[str, Any]:
    raw_sources = raw.get("sources", [])
    source_health = [_to_contract_health_item(item) for item in raw_sources]

    metadata = raw.get("query_metadata", {})
    known_limitations = list(metadata.get("known_limitations", []))

    return {
        "source_health": source_health,
        "overall_status": raw.get("overall_status", "unknown"),
        "sources": raw_sources,
        "query_metadata": metadata,
        "known_limitations": known_limitations,
    }


def check_source_health(**kwargs):
    source = kwargs.get("source")
    sources = kwargs.get("sources")

    if source is not None and sources is not None:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            "Use either source or sources, not both",
            suggested_next_action="Use source='FDA' for one source or sources=['FDA', 'TFDA'] for multiple sources.",
        )

    source_list = _as_source_list(sources)
    if isinstance(source_list, dict) and "error" in source_list:
        return source_list

    if source is not None:
        source_list = _as_source_list(source)
        if isinstance(source_list, dict) and "error" in source_list:
            return source_list

    if source_list is None:
        raw = _check_source_health_impl(mode=kwargs.get("mode", "limited_live_connector_check"))
        if isinstance(raw, dict) and "error" in raw:
            return raw
        return _shape_contract_response(raw)

    merged_sources = []
    merged_checked = []
    merged_limitations = []

    for item in source_list:
        raw = _check_source_health_impl(source=item, mode=kwargs.get("mode", "limited_live_connector_check"))
        if isinstance(raw, dict) and "error" in raw:
            return raw

        merged_sources.extend(raw.get("sources", []))
        merged_checked.extend(raw.get("query_metadata", {}).get("sources_checked", []))
        merged_limitations.extend(raw.get("query_metadata", {}).get("known_limitations", []))

    overall_status = "available" if all(item.get("available") for item in merged_sources) else "degraded"
    retrieved_at = merged_sources[0].get("retrieved_at") if merged_sources else None

    return _shape_contract_response(
        {
            "overall_status": overall_status,
            "sources": merged_sources,
            "query_metadata": {
                "sources_checked": merged_checked,
                "retrieved_at": retrieved_at,
                "mode": kwargs.get("mode", "limited_live_connector_check"),
                "known_limitations": sorted(set(merged_limitations)),
            },
        }
    )


def list_source_failures(**kwargs):
    return {
        "failures": [],
        "summary": {
            "open_failure_count": 0,
            "critical_failure_count": 0,
            "known_limitations": ["No persisted events in skeleton"],
        },
    }
