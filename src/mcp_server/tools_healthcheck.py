from __future__ import annotations

from typing import Any

from src.core.errors import ErrorCode, build_error
from src.mcp_server.tools_source_health import check_source_health as _check_source_health_impl


_SOURCE_SPECS = {
    "FDA": {
        "internal_source": "FDA",
        "source_id": "FDA_openFDA",
        "agency_or_registry": "FDA",
        "source_type": "API",
        "endpoint_url": "https://api.fda.gov",
        "suggested_connector_file": "src/connectors/fda/fda_updates_client.py",
    },
    "TFDA": {
        "internal_source": "TFDA",
        "source_id": "TFDA_DataAction",
        "agency_or_registry": "TFDA",
        "source_type": "API",
        "endpoint_url": "https://www.fda.gov.tw",
        "suggested_connector_file": "src/connectors/tfda/tfda_updates_client.py",
    },
    "ClinicalTrials.gov": {
        "internal_source": "ClinicalTrials.gov",
        "source_id": "ClinicalTrialsGov_API",
        "agency_or_registry": "ClinicalTrials.gov",
        "source_type": "API",
        "endpoint_url": "https://clinicaltrials.gov",
        "suggested_connector_file": "src/connectors/clinical_trials/clinicaltrials_gov_client.py",
    },
}

_SOURCE_ALIASES = {
    "FDA": "FDA",
    "FDA_OPENFDA": "FDA",
    "TFDA": "TFDA",
    "TFDA_DATAACTION": "TFDA",
    "CLINICALTRIALS.GOV": "ClinicalTrials.gov",
    "CLINICALTRIALS": "ClinicalTrials.gov",
    "CLINICAL_TRIALS_GOV": "ClinicalTrials.gov",
    "CLINICAL-TRIALS-GOV": "ClinicalTrials.gov",
    "CLINICALTRIALSGOV_API": "ClinicalTrials.gov",
    "CLINICALTRIALS_GOV_API": "ClinicalTrials.gov",
}

_SUPPORTED_SOURCE_VALUES = [
    "FDA",
    "FDA_openFDA",
    "TFDA",
    "TFDA_DataAction",
    "ClinicalTrials.gov",
    "ClinicalTrialsGov_API",
]

_FDA_ABUSE_DETECTION_PATTERNS = (
    "apology_objects",
    "abuse-detection-apology",
    "abuse detection",
)

_FDA_ABUSE_DETECTION_SUSPECTED_CAUSE = (
    "The FDA request was redirected to an FDA abuse-detection/apology path or source-access block. "
    "This is not proof that FDA has no records, and it is not a no matching records signal. "
    "Rerun in another approved runtime or manually verify FDA official sources before interpreting FDA coverage."
)

_FDA_ABUSE_DETECTION_KNOWN_LIMITATION = (
    "FDA abuse-detection/apology redirects are source-access failures; they MUST NOT be interpreted as "
    "NO_MATCHING_RECORDS or as FDA having zero matching regulatory updates."
)

_EGRESS_POLICY_PATTERNS = (
    "Host not in allowlist",
    "not in allowlist",
    "egress allowlist",
    "runtime network policy",
    "network allowlist",
)

_EGRESS_POLICY_SUGGESTED_FIX = (
    "Check the runtime/network egress allowlist, including Claude Code Web environment settings if applicable, "
    "and add the source host; otherwise rerun live-source validation in Codespaces/local."
)

_EGRESS_POLICY_KNOWN_LIMITATION = (
    "Runtime network policy / egress allowlist failure means the source could not be reached from this runtime; "
    "it MUST NOT be interpreted as no matching records, no clinical trials, or no regulatory updates."
)


def _as_source_list(value: Any) -> list[str] | dict | None:
    if value is None:
        return None

    if isinstance(value, str):
        if not value.strip():
            return build_error(ErrorCode.INVALID_PARAMETER, "sources must contain non-empty strings")
        return [value.strip()]

    if isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value):
        return [item.strip() for item in value]

    return build_error(ErrorCode.INVALID_PARAMETER, "sources must be a string or list of non-empty strings")


def _normalize_source_key(value: str) -> str:
    return value.strip().upper()


def _source_spec_for_value(value: str) -> dict[str, str] | None:
    internal_source = _SOURCE_ALIASES.get(_normalize_source_key(value))
    if not internal_source:
        return None
    return _SOURCE_SPECS[internal_source]


def _source_specs_for_values(values: list[str]) -> list[dict[str, str]] | dict:
    specs = []

    for value in values:
        spec = _source_spec_for_value(value)
        if spec is None:
            return build_error(
                ErrorCode.INVALID_PARAMETER,
                f"Unsupported source: {value}",
                details={"supported_sources": _SUPPORTED_SOURCE_VALUES},
                suggested_next_action=(
                    "Use source=None for all sources, or one of FDA, FDA_openFDA, TFDA, "
                    "TFDA_DataAction, ClinicalTrials.gov, ClinicalTrialsGov_API."
                ),
            )
        specs.append(spec)

    return specs


def _status_for_contract(item: dict[str, Any]) -> str:
    if item.get("available") is True:
        return "pass"
    if item.get("available") is False:
        return "failed"
    return "unknown"


def _iter_strings(value: Any):
    if value is None:
        return
    if isinstance(value, str):
        yield value
        return
    if isinstance(value, dict):
        for item in value.values():
            yield from _iter_strings(item)
        return
    if isinstance(value, (list, tuple, set)):
        for item in value:
            yield from _iter_strings(item)
        return
    yield str(value)


def _diagnostic_text(item: dict[str, Any]) -> str:
    return " ".join(
        [
            *list(_iter_strings(item.get("message"))),
            *list(_iter_strings(item.get("error_message"))),
            *list(_iter_strings(item.get("error_details"))),
            *list(_iter_strings(item.get("suggested_next_action"))),
            *list(_iter_strings(item.get("suggested_fix"))),
            *list(_iter_strings(item.get("known_limitations"))),
        ]
    ).lower()


def _looks_like_egress_policy(item: dict[str, Any]) -> bool:
    text = _diagnostic_text(item)
    return any(pattern.lower() in text for pattern in _EGRESS_POLICY_PATTERNS)


def _looks_like_fda_abuse_detection(item: dict[str, Any]) -> bool:
    text = _diagnostic_text(item)
    return any(pattern in text for pattern in _FDA_ABUSE_DETECTION_PATTERNS)


def _failure_type_for_contract(item: dict[str, Any]) -> str:
    if item.get("available") is True:
        return ""

    if _looks_like_egress_policy(item):
        return "egress_policy"

    source_type = item.get("source_type")
    if source_type == "clinical_trials_registry":
        return "api_status"
    if source_type == "regulatory":
        return "api_status"
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


def _suggested_fix_for_contract(item: dict[str, Any]) -> str:
    if _looks_like_fda_abuse_detection(item):
        return (
            "Rerun FDA validation in another approved runtime or manually verify FDA official sources; "
            "do not treat the abuse-detection/apology redirect as no matching FDA records."
        )
    if _looks_like_egress_policy(item):
        return _EGRESS_POLICY_SUGGESTED_FIX
    return item.get("suggested_next_action", "")


def _known_limitations_for_contract(item: dict[str, Any]) -> list[str]:
    limitations = list(item.get("known_limitations", []))
    if _looks_like_fda_abuse_detection(item) and _FDA_ABUSE_DETECTION_KNOWN_LIMITATION not in limitations:
        limitations.append(_FDA_ABUSE_DETECTION_KNOWN_LIMITATION)
    if _looks_like_egress_policy(item) and _EGRESS_POLICY_KNOWN_LIMITATION not in limitations:
        limitations.append(_EGRESS_POLICY_KNOWN_LIMITATION)
    return limitations


def _default_spec_for_health_item(item: dict[str, Any]) -> dict[str, str]:
    source = item.get("source")
    return _SOURCE_SPECS.get(source, {
        "internal_source": source or "unknown",
        "source_id": source or "unknown",
        "agency_or_registry": source or "unknown",
        "source_type": "unknown",
        "endpoint_url": "",
        "suggested_connector_file": "",
    })


def _to_contract_health_item(item: dict[str, Any], spec: dict[str, str] | None = None) -> dict[str, Any]:
    resolved_spec = spec or _default_spec_for_health_item(item)
    checked_at = item.get("retrieved_at")

    return {
        "source_id": resolved_spec["source_id"],
        "agency_or_registry": resolved_spec["agency_or_registry"],
        "source_type": resolved_spec["source_type"],
        "endpoint_url": resolved_spec["endpoint_url"],
        "status": _status_for_contract(item),
        "last_successful_check": checked_at if item.get("available") is True else None,
        "last_checked_at": checked_at,
        "failure_type": _failure_type_for_contract(item),
        "error_message": item.get("message", ""),
        "error_details": item.get("error_details", ""),
        "suggested_fix": _suggested_fix_for_contract(item),
        "suggested_connector_file": resolved_spec["suggested_connector_file"],
        "severity": _severity_for_contract(item),
        "known_limitations": _known_limitations_for_contract(item),
    }


def _shape_contract_response(
    raw: dict[str, Any],
    *,
    specs: list[dict[str, str]] | None = None,
    sources_checked: list[str] | None = None,
) -> dict[str, Any]:
    raw_sources = raw.get("sources", [])

    if specs is None:
        source_health = [_to_contract_health_item(item) for item in raw_sources]
        contract_sources_checked = [
            _default_spec_for_health_item(item)["source_id"]
            for item in raw_sources
        ]
    else:
        source_health = [
            _to_contract_health_item(item, spec)
            for item, spec in zip(raw_sources, specs, strict=False)
        ]
        contract_sources_checked = [spec["source_id"] for spec in specs]

    metadata = dict(raw.get("query_metadata", {}))
    metadata["sources_checked"] = sources_checked or contract_sources_checked
    metadata["internal_sources_checked"] = [
        item.get("source", "unknown")
        for item in raw_sources
    ]

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
            suggested_next_action="Use source='FDA_openFDA' for one source or sources=['FDA_openFDA', 'TFDA_DataAction'] for multiple sources.",
        )

    source_list = _as_source_list(sources)
    if isinstance(source_list, dict) and "error" in source_list:
        return source_list

    if source is not None:
        source_list = _as_source_list(source)
        if isinstance(source_list, dict) and "error" in source_list:
            return source_list

    if source_list is None:
        specs = list(_SOURCE_SPECS.values())
    else:
        specs = _source_specs_for_values(source_list)
        if isinstance(specs, dict) and "error" in specs:
            return specs

    merged_sources = []
    merged_limitations = []

    for spec in specs:
        raw = _check_source_health_impl(
            source=spec["internal_source"],
            mode=kwargs.get("mode", "limited_live_connector_check"),
        )
        if isinstance(raw, dict) and "error" in raw:
            return raw

        merged_sources.extend(raw.get("sources", []))
        merged_limitations.extend(raw.get("query_metadata", {}).get("known_limitations", []))

    overall_status = "available" if all(item.get("available") for item in merged_sources) else "degraded"
    retrieved_at = merged_sources[0].get("retrieved_at") if merged_sources else None

    return _shape_contract_response(
        {
            "overall_status": overall_status,
            "sources": merged_sources,
            "query_metadata": {
                "retrieved_at": retrieved_at,
                "mode": kwargs.get("mode", "limited_live_connector_check"),
                "known_limitations": sorted(set(merged_limitations)),
            },
        },
        specs=specs,
    )


_FAILURE_TYPES = {
    "api_status",
    "egress_policy",
    "schema_validation",
    "rss_status",
    "html_selector",
    "attachment_download",
    "empty_result",
    "unknown",
}
_FAILURE_SEVERITIES = {"low", "medium", "high", "critical"}


def _as_filter_list(value: Any, name: str) -> list[str] | dict:
    if value in (None, ""):
        return []

    if isinstance(value, str):
        values = [value]
    elif isinstance(value, list) and all(isinstance(item, str) for item in value):
        values = value
    else:
        return build_error(ErrorCode.INVALID_PARAMETER, f"{name} must be a string or list of strings")

    return [item.strip() for item in values if item.strip()]


def _failure_id_for_health_item(item: dict[str, Any]) -> str:
    source_id = item.get("source_id", "unknown")
    failure_type = item.get("failure_type") or "unknown"
    status = "open" if item.get("status") in {"failed", "warning", "unknown"} else "resolved"
    return f"{source_id}-{failure_type}-{status}".replace(" ", "_")


def _status_for_failure(item: dict[str, Any]) -> str:
    if item.get("status") in {"failed", "warning", "unknown"}:
        return "open"
    return "resolved"


def _suspected_cause_for_failure(item: dict[str, Any]) -> str:
    failure_type = item.get("failure_type") or "unknown"
    if _looks_like_fda_abuse_detection(item):
        return _FDA_ABUSE_DETECTION_SUSPECTED_CAUSE
    if failure_type == "egress_policy":
        return (
            "Health check call was blocked by the runtime/network egress allowlist "
            "(e.g. Claude Code Web Host not in allowlist 403). "
            "This is a runtime network policy issue, NOT the upstream source being offline, "
            "and NOT a no-result / no matching records signal."
        )
    if failure_type == "api_status":
        return "Current source health check did not pass; API or connector availability may be affected."
    if failure_type == "schema_validation":
        return "Current source response may not match the expected parser or normalization schema."
    if failure_type == "html_selector":
        return "Current source webpage structure may have changed."
    if failure_type == "empty_result":
        return "Current source returned no usable records for the health check."
    return "Current source health check did not pass; cause requires manual review."


def _health_item_to_failure(item: dict[str, Any]) -> dict[str, Any]:
    detected_at = item.get("last_checked_at")
    status = _status_for_failure(item)

    return {
        "failure_id": _failure_id_for_health_item(item),
        "source_id": item.get("source_id", "unknown"),
        "agency_or_registry": item.get("agency_or_registry", "unknown"),
        "detected_at": detected_at,
        "resolved_at": item.get("last_successful_check") if status == "resolved" else None,
        "status": status,
        "failure_type": item.get("failure_type") or "unknown",
        "severity": item.get("severity", "medium"),
        "error_message": item.get("error_message", ""),
        "error_details": item.get("error_details", ""),
        "suspected_cause": _suspected_cause_for_failure(item),
        "suggested_fix": item.get("suggested_fix", ""),
        "suggested_connector_file": item.get("suggested_connector_file", ""),
        "github_issue_url": "",
        "known_limitations": item.get("known_limitations", []),
    }


def _failure_matches_filters(
    failure: dict[str, Any],
    *,
    agencies_or_registries: list[str],
    failure_types: list[str],
    severities: list[str],
    include_resolved: bool,
) -> bool:
    if not include_resolved and failure.get("status") == "resolved":
        return False

    if agencies_or_registries:
        allowed = {item.strip().lower() for item in agencies_or_registries}
        if str(failure.get("agency_or_registry", "")).strip().lower() not in allowed:
            return False

    if failure_types:
        allowed = {item.strip().lower() for item in failure_types}
        if str(failure.get("failure_type", "")).strip().lower() not in allowed:
            return False

    if severities:
        allowed = {item.strip().lower() for item in severities}
        if str(failure.get("severity", "")).strip().lower() not in allowed:
            return False

    return True


def _validate_failure_types(values: list[str]) -> dict | None:
    invalid = sorted({item.strip().lower() for item in values} - _FAILURE_TYPES)
    if invalid:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            f"Unsupported failure_types: {invalid}",
            details={"supported_failure_types": sorted(_FAILURE_TYPES)},
        )
    return None


def _validate_severities(values: list[str]) -> dict | None:
    invalid = sorted({item.strip().lower() for item in values} - _FAILURE_SEVERITIES)
    if invalid:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            f"Unsupported severity values: {invalid}",
            details={"supported_severity_values": sorted(_FAILURE_SEVERITIES)},
        )
    return None


def list_source_failures(**kwargs):
    sources = kwargs.get("sources")
    source = kwargs.get("source")
    agencies_or_registries = _as_filter_list(kwargs.get("agencies_or_registries"), "agencies_or_registries")
    if isinstance(agencies_or_registries, dict) and "error" in agencies_or_registries:
        return agencies_or_registries

    failure_types = _as_filter_list(kwargs.get("failure_types"), "failure_types")
    if isinstance(failure_types, dict) and "error" in failure_types:
        return failure_types

    failure_type_error = _validate_failure_types(failure_types)
    if failure_type_error:
        return failure_type_error

    severities = _as_filter_list(kwargs.get("severity"), "severity")
    if isinstance(severities, dict) and "error" in severities:
        return severities

    severity_error = _validate_severities(severities)
    if severity_error:
        return severity_error

    include_resolved = kwargs.get("include_resolved", False)
    if not isinstance(include_resolved, bool):
        return build_error(ErrorCode.INVALID_PARAMETER, "include_resolved must be a boolean")

    if source is not None and sources is not None:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            "Use either source or sources, not both",
            suggested_next_action="Use source='FDA_openFDA' for one source or sources=['FDA_openFDA', 'TFDA_DataAction'] for multiple sources.",
        )

    selected_sources = sources if sources is not None else source
    if selected_sources is None and agencies_or_registries:
        selected_sources = agencies_or_registries

    health_result = check_source_health(
        sources=selected_sources,
        mode=kwargs.get("mode", "limited_live_connector_check"),
    )
    if isinstance(health_result, dict) and "error" in health_result:
        return health_result

    source_health = health_result.get("source_health", [])
    if not isinstance(source_health, list):
        return build_error(
            ErrorCode.INTERNAL_ERROR,
            "check_source_health returned an unexpected source_health shape",
            details=f"Received source_health type: {type(source_health).__name__}",
        )

    failures = [
        _health_item_to_failure(item)
        for item in source_health
        if item.get("status") in {"failed", "warning", "unknown"}
    ]

    failures = [
        failure
        for failure in failures
        if _failure_matches_filters(
            failure,
            agencies_or_registries=agencies_or_registries,
            failure_types=failure_types,
            severities=severities,
            include_resolved=include_resolved,
        )
    ]

    critical_failure_count = sum(1 for failure in failures if failure.get("severity") == "critical")
    high_failure_count = sum(1 for failure in failures if failure.get("severity") == "high")
    open_failure_count = sum(1 for failure in failures if failure.get("status") == "open")

    known_limitations = [
        "MVP v1 list_source_failures is a current health snapshot, not a persisted historical failure event store.",
        "date_range is accepted for contract compatibility but does not query historical failure records in MVP v1.",
        "resolved failures are not available unless a future persisted event store is implemented.",
    ]
    known_limitations.extend(health_result.get("known_limitations", []))

    return {
        "failures": failures,
        "summary": {
            "open_failure_count": open_failure_count,
            "critical_failure_count": critical_failure_count,
            "high_failure_count": high_failure_count,
            "known_limitations": sorted(set(known_limitations)),
        },
        "query_metadata": {
            "sources_checked": health_result.get("query_metadata", {}).get("sources_checked", []),
            "internal_sources_checked": health_result.get("query_metadata", {}).get("internal_sources_checked", []),
            "filters_applied": {
                "source": source,
                "sources": sources,
                "agencies_or_registries": agencies_or_registries,
                "failure_types": failure_types,
                "severity": severities,
                "include_resolved": include_resolved,
                "date_range": kwargs.get("date_range"),
                "mode": kwargs.get("mode", "limited_live_connector_check"),
            },
            "lookup_mode": "current_health_snapshot",
            "known_limitations": sorted(set(known_limitations)),
        },
    }
