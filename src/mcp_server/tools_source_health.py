from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.connectors.clinical_trials.clinicaltrials_gov_client import ClinicalTrialsGovClient
from src.connectors.fda.fda_updates_client import FDAUpdatesClient
from src.connectors.tfda.tfda_updates_client import TFDAUpdatesClient
from src.core.errors import ErrorCode, build_error


_SUPPORTED_SOURCES = {
    "FDA": "FDA",
    "TFDA": "TFDA",
    "CLINICALTRIALS.GOV": "ClinicalTrials.gov",
    "CLINICALTRIALS": "ClinicalTrials.gov",
    "CLINICAL_TRIALS_GOV": "ClinicalTrials.gov",
    "CLINICAL-TRIALS-GOV": "ClinicalTrials.gov",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_source_name(source: str | None) -> str | None:
    if source is None:
        return None

    if not isinstance(source, str) or not source.strip():
        return ""

    key = source.strip().upper()
    return _SUPPORTED_SOURCES.get(key)


def _error_parts(result: dict[str, Any]) -> tuple[str | None, str, str]:
    error = result.get("error", {}) if isinstance(result, dict) else {}
    if not isinstance(error, dict):
        return None, "", ""

    return (
        error.get("code"),
        error.get("message", ""),
        error.get("suggested_next_action", ""),
    )


def _available_result(source: str, source_type: str, retrieved_at: str) -> dict[str, Any]:
    return {
        "source": source,
        "source_type": source_type,
        "available": True,
        "status": "available",
        "error_code": None,
        "message": "",
        "retrieved_at": retrieved_at,
        "suggested_next_action": "",
        "known_limitations": [
            "Health check validates connector execution path only; it is not a full content completeness audit."
        ],
    }


def _unavailable_result(
    source: str,
    source_type: str,
    retrieved_at: str,
    *,
    error_code: str = "SOURCE_UNAVAILABLE",
    message: str = "",
    suggested_next_action: str = "",
) -> dict[str, Any]:
    return {
        "source": source,
        "source_type": source_type,
        "available": False,
        "status": "unavailable",
        "error_code": error_code,
        "message": message,
        "retrieved_at": retrieved_at,
        "suggested_next_action": suggested_next_action
        or f"Check {source} connector runtime dependencies and source availability.",
        "known_limitations": [
            "Health check uses a limited connector call and may not detect partial content coverage issues."
        ],
    }


def _unexpected_result(source: str, source_type: str, retrieved_at: str, result: Any) -> dict[str, Any]:
    return _unavailable_result(
        source,
        source_type,
        retrieved_at,
        error_code="INTERNAL_ERROR",
        message=f"Unexpected source health response shape: {type(result).__name__}",
        suggested_next_action=f"Update {source} health check adapter to handle this response shape.",
    )


def _check_regulatory_source(source: str, client: Any, retrieved_at: str) -> dict[str, Any]:
    try:
        result = client.search_updates(limit=1)
    except Exception as exc:
        return _unavailable_result(
            source,
            "regulatory",
            retrieved_at,
            error_code="SOURCE_UNAVAILABLE",
            message=f"{source} health check failed: {exc}",
        )

    if isinstance(result, dict) and "error" in result:
        error_code, message, suggested_next_action = _error_parts(result)
        return _unavailable_result(
            source,
            "regulatory",
            retrieved_at,
            error_code=error_code or "SOURCE_UNAVAILABLE",
            message=message,
            suggested_next_action=suggested_next_action,
        )

    if isinstance(result, list):
        return _available_result(source, "regulatory", retrieved_at)

    return _unexpected_result(source, "regulatory", retrieved_at, result)


def _check_clinical_trials_source(retrieved_at: str) -> dict[str, Any]:
    source = "ClinicalTrials.gov"
    try:
        result = ClinicalTrialsGovClient().search_studies(indication="cancer", page_size=1)
    except Exception as exc:
        return _unavailable_result(
            source,
            "clinical_trials_registry",
            retrieved_at,
            error_code="SOURCE_UNAVAILABLE",
            message=f"{source} health check failed: {exc}",
            suggested_next_action="Check ClinicalTrials.gov connector runtime dependencies and API v2 availability.",
        )

    if isinstance(result, dict) and "error" in result:
        error_code, message, suggested_next_action = _error_parts(result)
        return _unavailable_result(
            source,
            "clinical_trials_registry",
            retrieved_at,
            error_code=error_code or "SOURCE_UNAVAILABLE",
            message=message,
            suggested_next_action=suggested_next_action
            or "Check ClinicalTrials.gov connector runtime dependencies and API v2 availability.",
        )

    if isinstance(result, dict) and "studies" in result:
        return _available_result(source, "clinical_trials_registry", retrieved_at)

    return _unexpected_result(source, "clinical_trials_registry", retrieved_at, result)


def check_source_health(source: str | None = None, **kwargs):
    requested = _normalize_source_name(source)

    if source is not None and not requested:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            f"Unsupported source: {source}",
            details={"supported_sources": ["FDA", "TFDA", "ClinicalTrials.gov"]},
            suggested_next_action="Use source=None for all sources, or one of FDA, TFDA, ClinicalTrials.gov.",
        )

    sources_to_check = [requested] if requested else ["FDA", "TFDA", "ClinicalTrials.gov"]
    retrieved_at = _utc_now()
    results = []

    for item in sources_to_check:
        if item == "FDA":
            results.append(_check_regulatory_source("FDA", FDAUpdatesClient(), retrieved_at))
        elif item == "TFDA":
            results.append(_check_regulatory_source("TFDA", TFDAUpdatesClient(), retrieved_at))
        elif item == "ClinicalTrials.gov":
            results.append(_check_clinical_trials_source(retrieved_at))

    overall_status = "available" if all(item["available"] for item in results) else "degraded"

    return {
        "overall_status": overall_status,
        "sources": results,
        "query_metadata": {
            "sources_checked": sources_to_check,
            "retrieved_at": retrieved_at,
            "mode": kwargs.get("mode", "limited_live_connector_check"),
            "known_limitations": [
                "This health check confirms connector execution path and source response availability.",
                "It does not verify full source completeness, search recall, or downstream report quality.",
            ],
        },
    }
