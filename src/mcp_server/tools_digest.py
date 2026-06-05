from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from src.core.errors import ErrorCode, build_error
from src.mcp_server.tools_clinical_trials import search_clinical_trials_by_indication
from src.mcp_server.tools_healthcheck import check_source_health, list_source_failures
from src.mcp_server.tools_regulatory import search_regulatory_updates


_ALLOWED_DIGEST_TYPES = {"regulatory_update", "clinical_trial_update", "combined"}
_ALLOWED_DATE_RANGES = {"1m", "3m", "6m", "1y", "3y", "5y", "custom"}
_DATE_RANGE_DAYS = {
    "1m": 30,
    "3m": 90,
    "6m": 180,
    "1y": 365,
    "3y": 1095,
    "5y": 1825,
}
_MVP_AGENCIES = {"FDA", "TFDA"}
_MVP_REGISTRIES = {"ClinicalTrials.gov"}


def _as_string_list(value: Any, name: str) -> list[str] | dict:
    if value in (None, ""):
        return []

    if isinstance(value, str):
        values = [value]
    elif isinstance(value, list) and all(isinstance(item, str) for item in value):
        values = value
    else:
        return build_error(ErrorCode.INVALID_PARAMETER, f"{name} must be a string or list of strings")

    return [item.strip() for item in values if item.strip()]


def _parse_limit(value: Any) -> int | dict:
    if value is None:
        return 10
    if isinstance(value, bool):
        return build_error(ErrorCode.INVALID_PARAMETER, "limit must be an integer between 1 and 50")
    try:
        limit = int(value)
    except Exception:
        return build_error(ErrorCode.INVALID_PARAMETER, "limit must be an integer between 1 and 50")
    if limit < 1 or limit > 50:
        return build_error(ErrorCode.INVALID_PARAMETER, "limit must be an integer between 1 and 50")
    return limit


def _normalize_agencies(values: list[str]) -> list[str] | dict:
    agencies = [item.strip().upper() for item in values] if values else ["FDA", "TFDA"]
    invalid = sorted(set(agencies) - _MVP_AGENCIES)
    if invalid:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            f"Unsupported agencies for MVP v1 digest: {invalid}",
            suggested_next_action="Use MVP v1 active agencies only: FDA and TFDA.",
        )
    return list(dict.fromkeys(agencies))


def _normalize_registries(values: list[str]) -> list[str] | dict:
    registries = values or ["ClinicalTrials.gov"]
    invalid = sorted(set(registries) - _MVP_REGISTRIES)
    if invalid:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            f"Unsupported registries for MVP v1 digest: {invalid}",
            suggested_next_action="Use MVP v1 active registry only: ClinicalTrials.gov.",
        )
    return list(dict.fromkeys(registries))


def _resolve_dates(kwargs: dict[str, Any]) -> dict[str, str | None] | dict:
    date_range = kwargs.get("date_range", "1m")
    if date_range not in _ALLOWED_DATE_RANGES:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            f"date_range must be one of {sorted(_ALLOWED_DATE_RANGES)}",
        )

    if date_range == "custom":
        date_from = kwargs.get("date_from") or kwargs.get("start_date")
        date_to = kwargs.get("date_to") or kwargs.get("end_date")
        return {"date_range": "custom", "date_from": date_from, "date_to": date_to}

    today = datetime.now(timezone.utc).date()
    return {
        "date_range": date_range,
        "date_from": (today - timedelta(days=_DATE_RANGE_DAYS[date_range])).isoformat(),
        "date_to": today.isoformat(),
    }


def _lower_set(values: list[str]) -> set[str]:
    return {str(item).strip().lower() for item in values if str(item).strip()}


def _as_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _record_matches_digest_filters(record: dict[str, Any], *, product_modality: list[str], topics: list[str]) -> bool:
    if product_modality and not (_lower_set(_as_list(record.get("product_modality"))) & _lower_set(product_modality)):
        return False

    if topics and not (_lower_set(_as_list(record.get("topics"))) & _lower_set(topics)):
        return False

    return True


def _regulatory_query(kwargs: dict[str, Any], *, topics: list[str], product_modality: list[str]) -> str | None:
    query = kwargs.get("query")
    if isinstance(query, str) and query.strip():
        return query.strip()

    keywords = []
    keywords.extend(topics)
    keywords.extend(product_modality)
    keywords.extend(_as_string_list(kwargs.get("keywords"), "keywords") or [])

    return " ".join(dict.fromkeys([item for item in keywords if item])) or None


def _digest_regulatory_update(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": record.get("title", ""),
        "agency": record.get("agency", ""),
        "publication_date": record.get("publication_date"),
        "impact_level": record.get("impact_level", "unknown"),
        "official_url": record.get("official_url", ""),
        "summary": record.get("summary", ""),
    }


def _digest_clinical_trial(trial: dict[str, Any]) -> dict[str, Any]:
    trial_id = trial.get("trial_id", "")
    return {
        "trial_id": trial_id,
        "title": trial.get("title", ""),
        "sponsor": trial.get("sponsor", ""),
        "phase": trial.get("phase", "unknown"),
        "status": trial.get("status", "unknown"),
        "last_update_date": trial.get("last_update_date"),
        "official_url": trial.get("official_url", ""),
        "summary": (
            f"{trial.get('title', 'Clinical trial')} is listed as "
            f"{trial.get('status', 'unknown')} for {', '.join(_as_list(trial.get('indications'))) or 'the requested indication'}."
        ),
    }


def _impact_matrix_item(item: dict[str, Any], *, item_type: str) -> dict[str, Any]:
    title = item.get("title") or item.get("trial_id") or "Untitled item"
    if item_type == "regulatory":
        impacted_functions = ["RA"]
        topics = _lower_set(_as_list(item.get("topics")))
        if topics & {"quality", "cmc", "gmp", "manufacturing"}:
            impacted_functions.extend(["CMC", "QA"])
        if topics & {"clinical", "gcp"}:
            impacted_functions.append("clinical")
        follow_up = "Review the source update and confirm regulatory impact before action."
    else:
        impacted_functions = ["clinical", "RA"]
        follow_up = "Review the trial record before drawing clinical or competitive conclusions."

    return {
        "item": title,
        "impact_level": item.get("impact_level", "unknown"),
        "impacted_functions": sorted(set(impacted_functions)),
        "recommended_follow_up": follow_up,
    }


def _source_health_summary(include_source_health_summary: bool) -> tuple[dict[str, Any], list[str]]:
    if not include_source_health_summary:
        return {
            "status": "unknown",
            "open_failures": 0,
            "notes": ["Source health summary was not requested."],
        }, []

    health = check_source_health()
    failures = list_source_failures()

    notes = []
    limitations = []

    if isinstance(health, dict) and "error" in health:
        notes.append(health["error"].get("message", "Source health check failed."))
        status = "failed"
    else:
        overall_status = health.get("overall_status", "unknown")
        status = "pass" if overall_status == "available" else "warning"
        limitations.extend(health.get("known_limitations", []))

    if isinstance(failures, dict) and "error" in failures:
        notes.append(failures["error"].get("message", "Source failure listing failed."))
        open_failures = 0
    else:
        open_failures = failures.get("summary", {}).get("open_failure_count", 0)
        notes.extend(failures.get("summary", {}).get("known_limitations", []))

    if not notes:
        notes.append("Source health checked using MVP v1 source health tools.")

    return {
        "status": status,
        "open_failures": open_failures,
        "notes": sorted(set(notes)),
    }, sorted(set(limitations))


def _source_error_labels(source_errors: list[dict[str, Any]]) -> list[str]:
    labels = []
    for item in source_errors:
        source = item.get("source") if isinstance(item, dict) else None
        if source:
            labels.append(str(source))
    return sorted(set(labels))


def _executive_summary(
    *,
    digest_type: str,
    regulatory_count: int,
    clinical_count: int,
    open_failures: int,
    source_errors: list[dict[str, Any]],
) -> str:
    parts = [
        f"Generated a minimal MVP v1 {digest_type} digest.",
        f"Included {regulatory_count} regulatory update(s) and {clinical_count} clinical trial update(s).",
    ]

    if source_errors:
        failed_sources = _source_error_labels(source_errors)
        failed_source_text = ", ".join(failed_sources) if failed_sources else "one or more requested sources"
        parts.append(
            f"Coverage is partial for requested source(s): {failed_source_text}; zero returned updates must not be interpreted as no updates for unavailable sources."
        )
        parts.append(f"{len(source_errors)} source query error(s) were captured; review query_metadata.source_errors.")

    if open_failures:
        if source_errors:
            parts.append(f"{open_failures} open source failure(s) were reported by source health tools.")
        else:
            parts.append(
                f"{open_failures} open source failure(s) were reported by source health tools, but no source query errors occurred for the requested sources in this digest."
            )
    else:
        parts.append("No open source failures were reported by source health tools.")

    parts.append("This is a rule-based aggregation, not a final regulatory or clinical assessment.")
    return " ".join(parts)


def generate_regulatory_digest(**kwargs):
    digest_type = kwargs.get("digest_type", "combined")
    if digest_type not in _ALLOWED_DIGEST_TYPES:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            f"digest_type must be one of {sorted(_ALLOWED_DIGEST_TYPES)}",
        )

    limit = _parse_limit(kwargs.get("limit"))
    if isinstance(limit, dict) and "error" in limit:
        return limit

    dates = _resolve_dates(kwargs)
    if isinstance(dates, dict) and "error" in dates:
        return dates

    agencies_raw = _as_string_list(kwargs.get("agencies"), "agencies")
    if isinstance(agencies_raw, dict) and "error" in agencies_raw:
        return agencies_raw
    agencies = _normalize_agencies(agencies_raw)
    if isinstance(agencies, dict) and "error" in agencies:
        return agencies

    registries_raw = _as_string_list(kwargs.get("registries"), "registries")
    if isinstance(registries_raw, dict) and "error" in registries_raw:
        return registries_raw
    registries = _normalize_registries(registries_raw)
    if isinstance(registries, dict) and "error" in registries:
        return registries

    product_modality = _as_string_list(kwargs.get("product_modality"), "product_modality")
    if isinstance(product_modality, dict) and "error" in product_modality:
        return product_modality

    topics = _as_string_list(kwargs.get("topics"), "topics")
    if isinstance(topics, dict) and "error" in topics:
        return topics

    indications = _as_string_list(kwargs.get("indications"), "indications")
    if isinstance(indications, dict) and "error" in indications:
        return indications

    companies = _as_string_list(kwargs.get("companies"), "companies")
    if isinstance(companies, dict) and "error" in companies:
        return companies

    include_impact_matrix = kwargs.get("include_impact_matrix", True)
    if not isinstance(include_impact_matrix, bool):
        return build_error(ErrorCode.INVALID_PARAMETER, "include_impact_matrix must be a boolean")

    include_source_health_summary = kwargs.get("include_source_health_summary", True)
    if not isinstance(include_source_health_summary, bool):
        return build_error(ErrorCode.INVALID_PARAMETER, "include_source_health_summary must be a boolean")

    source_errors = []
    known_limitations = [
        "MVP v1 digest is a rule-based aggregation over current MCP tool outputs.",
        "Digest content is not a final regulatory, clinical, legal, or medical assessment.",
        "Impact matrix is heuristic and requires manual review.",
    ]

    regulatory_updates = []
    if digest_type in {"regulatory_update", "combined"}:
        query = _regulatory_query(kwargs, topics=topics, product_modality=product_modality)
        for agency in agencies:
            result = search_regulatory_updates(
                agency=agency,
                query=query,
                limit=limit,
                date_from=dates["date_from"],
                date_to=dates["date_to"],
            )
            if isinstance(result, dict) and "error" in result:
                source_errors.append({"source": agency, "error": result["error"]})
                continue

            records = result.get("records", []) if isinstance(result, dict) else []
            for record in records:
                if _record_matches_digest_filters(record, product_modality=product_modality, topics=topics):
                    regulatory_updates.append(record)

            known_limitations.extend(result.get("known_limitations", []))

    clinical_trials = []
    if digest_type in {"clinical_trial_update", "combined"}:
        if not indications:
            known_limitations.append("No indications provided; clinical trial search was skipped in MVP v1 digest.")
        else:
            for indication in indications:
                sponsors = companies or [None]
                for sponsor in sponsors:
                    result = search_clinical_trials_by_indication(
                        indication,
                        sponsor=sponsor,
                        page_size=limit,
                    )
                    source_label = f"ClinicalTrials.gov:{indication}" + (f":{sponsor}" if sponsor else "")
                    if isinstance(result, dict) and "error" in result:
                        source_errors.append({"source": source_label, "error": result["error"]})
                        continue

                    clinical_trials.extend(result.get("trials", []))
                    known_limitations.extend(result.get("query_metadata", {}).get("known_limitations", []))

    key_regulatory_updates = [_digest_regulatory_update(record) for record in regulatory_updates[:limit]]
    key_clinical_trial_updates = [_digest_clinical_trial(trial) for trial in clinical_trials[:limit]]

    source_health_summary, health_limitations = _source_health_summary(include_source_health_summary)
    known_limitations.extend(health_limitations)
    if source_errors:
        failed_sources = ", ".join(_source_error_labels(source_errors)) or "one or more requested sources"
        known_limitations.append(
            f"Coverage is partial because requested source(s) returned query errors: {failed_sources}. Zero returned updates must not be interpreted as no updates for unavailable sources."
        )
    elif source_health_summary.get("open_failures"):
        known_limitations.append(
            "Open source failures may include sources outside the requested digest source set; query_metadata.source_errors identifies requested source query failures."
        )

    impact_matrix = []
    if include_impact_matrix:
        impact_matrix.extend(_impact_matrix_item(record, item_type="regulatory") for record in regulatory_updates[:limit])
        impact_matrix.extend(_impact_matrix_item(trial, item_type="clinical") for trial in clinical_trials[:limit])

    sources_searched = []
    if digest_type in {"regulatory_update", "combined"}:
        sources_searched.extend(agencies)
    if digest_type in {"clinical_trial_update", "combined"}:
        sources_searched.extend(registries)

    return {
        "digest": {
            "title": "MVP v1 Regulatory and Clinical Intelligence Digest",
            "date_range": dates["date_range"],
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "sources_searched": sources_searched,
            "search_criteria": {
                "digest_type": digest_type,
                "agencies": agencies,
                "registries": registries,
                "product_modality": product_modality,
                "topics": topics,
                "indications": indications,
                "companies": companies,
                "date_from": dates["date_from"],
                "date_to": dates["date_to"],
                "limit": limit,
            },
            "executive_summary": _executive_summary(
                digest_type=digest_type,
                regulatory_count=len(key_regulatory_updates),
                clinical_count=len(key_clinical_trial_updates),
                open_failures=source_health_summary["open_failures"],
                source_errors=source_errors,
            ),
            "key_regulatory_updates": key_regulatory_updates,
            "key_clinical_trial_updates": key_clinical_trial_updates,
            "impact_matrix": impact_matrix,
            "source_health_summary": source_health_summary,
            "known_limitations": sorted(set(known_limitations)),
        },
        "query_metadata": {
            "lookup_mode": "minimal_mvp_aggregation",
            "source_errors": source_errors,
            "known_limitations": sorted(set(known_limitations)),
        },
    }
