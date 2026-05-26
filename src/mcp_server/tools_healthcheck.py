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


def _failure_type_for_contract(item: dict[str, Any]) -> str:
    if item.get("available") is True:
        return ""

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
        "suggested_fix": item.get("suggested_next_action", ""),
        "suggested_connector_file": resolved_spec["suggested_connector_file"],
        "severity": _severity_for_contract(item),
        "known_limitations": item.get("known_limitations", []),
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


def list_source_failures(**kwargs):
    return {
        "failures": [],
        "summary": {
            "open_failure_count": 0,
            "critical_failure_count": 0,
            "known_limitations": ["No persisted events in skeleton"],
        },
    }
