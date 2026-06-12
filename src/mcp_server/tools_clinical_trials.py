from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from typing import Any

from datetime import datetime, timezone

from src.connectors.clinical_trials.clinicaltrials_gov_client import ClinicalTrialsGovClient
from src.core.errors import ErrorCode, build_error
from src.core.normalization import normalize_clinicaltrials_record


_MVP_REGISTRIES = {"ClinicalTrials.gov"}
_ALLOWED_DATE_RANGES = {"1m", "3m", "6m", "1y", "3y", "5y", "custom"}
_ACTIVE_STATUSES = {
    "RECRUITING",
    "ACTIVE_NOT_RECRUITING",
    "ENROLLING_BY_INVITATION",
    "NOT_YET_RECRUITING",
}
_COMPLETED_STATUSES = {
    "COMPLETED",
    "TERMINATED",
    "WITHDRAWN",
    "SUSPENDED",
}


def search_clinical_trials_by_indication(indication: str, **kwargs):
    if not isinstance(indication, str) or not indication.strip():
        return build_error(ErrorCode.INVALID_PARAMETER, "indication must be a non-empty string")

    page_size = _parse_page_size(kwargs.get("page_size"))
    if isinstance(page_size, dict) and "error" in page_size:
        return page_size

    phase = _normalize_optional_string_filter(kwargs.get("phase"), "phase")
    if isinstance(phase, dict) and "error" in phase:
        return phase

    status = _normalize_optional_string_filter(kwargs.get("status"), "status")
    if isinstance(status, dict) and "error" in status:
        return status

    clean_indication = indication.strip()

    client = ClinicalTrialsGovClient()
    result = client.search_studies(
        indication=clean_indication,
        page_size=page_size,
        sponsor=kwargs.get("sponsor"),
        phase=phase,
        status=status,
        page_token=kwargs.get("page_token"),
    )

    if "error" in result:
        return build_error(
            ErrorCode.SOURCE_UNAVAILABLE,
            "ClinicalTrials.gov search failed",
            details=result["error"].get("details", result["error"].get("message", "")),
            suggested_next_action="Retry later and check source health for ClinicalTrials.gov API v2.",
        )

    studies = result.get("studies", []) if isinstance(result, dict) else []
    if not studies:
        return {
            "trials": [],
            "no_result_reason": "NO_MATCHING_RECORDS",
            "suggested_next_action": "Broaden indication keywords or remove restrictive filters.",
            "query_metadata": {
                "indication": clean_indication,
                "registries_searched": ["ClinicalTrials.gov"],
                "known_limitations": ["Only ClinicalTrials.gov API v2 is active in MVP v1."],
            },
        }

    retrieved_at = datetime.now(timezone.utc).isoformat()
    normalized = [asdict(normalize_clinicaltrials_record(raw=study, retrieved_at=retrieved_at)) for study in studies]

    return {
        "trials": normalized,
        "query_metadata": {
            "indication": clean_indication,
            "registries_searched": ["ClinicalTrials.gov"],
            "known_limitations": [
                "MVP v1 currently queries ClinicalTrials.gov only.",
                "Phase/status filters use conservative API v2 parameter mapping.",
            ],
        },
    }


def _normalize_optional_string_filter(value: Any, name: str) -> list[str] | None | dict:
    if value is None:
        return None
    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned:
            return build_error(
                ErrorCode.INVALID_PARAMETER,
                f"{name} must be a non-empty string or list of strings",
            )
        return [cleaned]
    if isinstance(value, list):
        if not value:
            return build_error(
                ErrorCode.INVALID_PARAMETER,
                f"{name} must contain at least one value",
            )
        cleaned_values: list[str] = []
        for item in value:
            if not isinstance(item, str) or not item.strip():
                return build_error(
                    ErrorCode.INVALID_PARAMETER,
                    f"{name} must contain only non-empty strings",
                )
            cleaned_values.append(item.strip())
        return cleaned_values
    return build_error(
        ErrorCode.INVALID_PARAMETER,
        f"{name} must be a string or list of strings",
    )


def _parse_page_size(value: Any) -> int | dict:
    if value is None:
        return 20
    if isinstance(value, bool):
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            "page_size must be an integer between 1 and 100",
        )
    try:
        page_size = int(value)
    except (TypeError, ValueError):
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            "page_size must be an integer between 1 and 100",
        )
    if page_size < 1 or page_size > 100:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            "page_size must be an integer between 1 and 100",
        )
    return page_size


def _as_string_list(value: Any, name: str, *, required: bool = False) -> list[str] | dict:
    if value in (None, ""):
        if required:
            return build_error(ErrorCode.INVALID_PARAMETER, f"{name} must contain at least one value")
        return []

    if isinstance(value, str):
        values = [value]
    elif isinstance(value, list) and all(isinstance(item, str) for item in value):
        values = value
    else:
        return build_error(
        ErrorCode.INVALID_PARAMETER,
        f"{name} must be a string or list of strings",
    )

    cleaned = [item.strip() for item in values if item.strip()]
    if required and not cleaned:
        return build_error(ErrorCode.INVALID_PARAMETER, f"{name} must contain at least one value")
    return list(dict.fromkeys(cleaned))


def _parse_limit(value: Any) -> int | dict:
    if value is None:
        return 20
    if isinstance(value, bool):
        return build_error(ErrorCode.INVALID_PARAMETER, "limit must be an integer between 1 and 50")
    try:
        limit = int(value)
    except Exception:
        return build_error(ErrorCode.INVALID_PARAMETER, "limit must be an integer between 1 and 50")
    if limit < 1 or limit > 50:
        return build_error(ErrorCode.INVALID_PARAMETER, "limit must be an integer between 1 and 50")
    return limit


def _normalize_registries(value: Any) -> list[str] | dict:
    registries = _as_string_list(value, "registries")
    if isinstance(registries, dict) and "error" in registries:
        return registries

    registries = registries or ["ClinicalTrials.gov"]
    invalid = sorted(set(registries) - _MVP_REGISTRIES)
    if invalid:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            f"Unsupported registries for MVP v1 company comparison: {invalid}",
            suggested_next_action="Use MVP v1 active registry only: ClinicalTrials.gov.",
        )
    return registries


def _normalize_date_range(value: Any) -> str | dict:
    date_range = value or "3y"
    if date_range not in _ALLOWED_DATE_RANGES:
        return build_error(
            ErrorCode.INVALID_PARAMETER,
            f"date_range must be one of {sorted(_ALLOWED_DATE_RANGES)}",
        )
    return date_range


def _normalize_phase(value: str) -> str:
    phase = str(value or "").strip().upper().replace(" ", "_")
    aliases = {
        "EARLY_PHASE1": "EARLY_PHASE1",
        "EARLY_PHASE_1": "EARLY_PHASE1",
        "PHASE1": "PHASE1",
        "PHASE_1": "PHASE1",
        "PHASE2": "PHASE2",
        "PHASE_2": "PHASE2",
        "PHASE3": "PHASE3",
        "PHASE_3": "PHASE3",
        "PHASE4": "PHASE4",
        "PHASE_4": "PHASE4",
        "NA": "NA",
        "N/A": "NA",
    }
    return aliases.get(phase, phase)


def _phase_rank(phase: str) -> int:
    order = {
        "NA": 0,
        "EARLY_PHASE1": 1,
        "PHASE1": 2,
        "PHASE2": 3,
        "PHASE3": 4,
        "PHASE4": 5,
    }
    return order.get(_normalize_phase(phase), -1)


def _lower_set(values: list[Any]) -> set[str]:
    return {str(item).strip().lower() for item in values if str(item).strip()}


def _as_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _normalized_text(value: Any) -> str:
    return str(value or "").strip().lower()


def _sponsor_matches_requested_company(trial: dict[str, Any], requested_company: str) -> bool:
    sponsor = _normalized_text(trial.get("sponsor"))
    company = _normalized_text(requested_company)
    return bool(sponsor and company and company in sponsor)


def _association_basis(trial: dict[str, Any], requested_company: str) -> str:
    if _sponsor_matches_requested_company(trial, requested_company):
        return "sponsor_name_match"
    return "returned_by_clinicaltrials_gov_query_requires_manual_review"


def _trial_matches_filters(
    trial: dict[str, Any],
    *,
    product_modality: list[str],
    phase_filter: list[str],
    include_completed_trials: bool,
    include_results: bool,
) -> bool:
    if product_modality and not (_lower_set(_as_list(trial.get("product_modality"))) & _lower_set(product_modality)):
        return False

    if phase_filter:
        normalized_phase_filter = {_normalize_phase(item) for item in phase_filter}
        if _normalize_phase(trial.get("phase", "")) not in normalized_phase_filter:
            return False

    status = str(trial.get("status", "")).upper()
    if not include_completed_trials and status in _COMPLETED_STATUSES:
        return False

    if not include_results and trial.get("results_available") is True:
        return False

    return True


def _trial_summary(trial: dict[str, Any], *, requested_company: str | None = None) -> dict[str, Any]:
    summary = {
        "trial_id": trial.get("trial_id", ""),
        "title": trial.get("title", ""),
        "phase": trial.get("phase", "unknown"),
        "status": trial.get("status", "unknown"),
        "intervention_names": _as_list(trial.get("intervention_names")),
        "last_update_date": trial.get("last_update_date"),
        "official_url": trial.get("official_url", ""),
        "results_available": trial.get("results_available"),
        "sponsor": trial.get("sponsor", ""),
    }
    if requested_company is not None:
        sponsor = trial.get("sponsor", "")
        sponsor_matches = _sponsor_matches_requested_company(trial, requested_company)
        summary.update(
            {
                "requested_company": requested_company,
                "record_sponsor": sponsor,
                "sponsor_matches_requested_company": sponsor_matches,
                "association_basis": _association_basis(trial, requested_company),
            }
        )
    return summary


def _source_error_code(error: dict[str, Any]) -> str:
    code = error.get("code") if isinstance(error, dict) else None
    return str(code or ErrorCode.SOURCE_UNAVAILABLE.value)


def _company_not_evaluable_summary(company: str, error: dict[str, Any]) -> dict[str, Any]:
    code = _source_error_code(error)
    return {
        "company": company,
        "activity_evaluable": False,
        "source_status": "unavailable",
        "source_error_code": code,
        "association_mode": "not_evaluable_source_unavailable",
        "sponsor_name_match_count": None,
        "non_sponsor_record_count": None,
        "trial_count": None,
        "active_trial_count": None,
        "completed_trial_count": None,
        "display_trial_count": "Not evaluable — ClinicalTrials.gov source unavailable",
        "display_active_trial_count": "Not evaluable",
        "display_completed_trial_count": "Not evaluable",
        "modalities": ["unknown"],
        "highest_phase": "not_evaluable",
        "phase_distribution": {},
        "status_distribution": {},
        "key_trials": [],
        "summary": (
            f"{company} trial activity is not evaluable because the ClinicalTrials.gov sponsor search returned {code}. "
            "This is a source-access limitation and must not be interpreted as zero trial activity."
        ),
        "known_limitations": [
            "ClinicalTrials.gov sponsor search returned a source error; activity counts are not evaluable.",
            "Not evaluable is distinct from zero matching trial records.",
            "Trial counts must not be interpreted when the source is unavailable.",
            "MVP v1 compares ClinicalTrials.gov trial activity only when the registry source is reachable.",
        ],
    }


def _company_summary(company: str, trials: list[dict[str, Any]], *, page_size: int) -> dict[str, Any]:
    status_counter = Counter(str(trial.get("status", "unknown")).upper() for trial in trials)
    phases = [str(trial.get("phase", "unknown")) for trial in trials]
    modalities = sorted({m for trial in trials for m in _as_list(trial.get("product_modality")) if m})
    highest_phase = max(phases, key=_phase_rank) if phases else "unknown"

    active_trial_count = sum(status_counter.get(status, 0) for status in _ACTIVE_STATUSES)
    completed_trial_count = sum(status_counter.get(status, 0) for status in _COMPLETED_STATUSES)
    sponsor_name_match_count = sum(1 for trial in trials if _sponsor_matches_requested_company(trial, company))
    non_sponsor_record_count = len(trials) - sponsor_name_match_count

    key_trials = sorted(
        trials,
        key=lambda trial: (_phase_rank(trial.get("phase", "")), str(trial.get("last_update_date") or "")),
        reverse=True,
    )[:page_size]

    return {
        "company": company,
        "activity_evaluable": True,
        "source_status": "available",
        "source_error_code": None,
        "association_mode": "clinicaltrials_gov_query_result_mvp",
        "sponsor_name_match_count": sponsor_name_match_count,
        "non_sponsor_record_count": non_sponsor_record_count,
        "trial_count": len(trials),
        "active_trial_count": active_trial_count,
        "completed_trial_count": completed_trial_count,
        "display_trial_count": str(len(trials)),
        "display_active_trial_count": str(active_trial_count),
        "display_completed_trial_count": str(completed_trial_count),
        "modalities": modalities or ["unknown"],
        "highest_phase": highest_phase,
        "phase_distribution": dict(Counter(phases)),
        "status_distribution": dict(status_counter),
        "key_trials": [_trial_summary(trial, requested_company=company) for trial in key_trials],
        "summary": (
            f"The MVP ClinicalTrials.gov query for {company} returned {len(trials)} trial record(s) matching the requested indication and filters. "
            f"{sponsor_name_match_count} record(s) have sponsor names matching the requested company; "
            f"{non_sponsor_record_count} record(s) require manual review of sponsor or product association. "
            "This is trial activity only and should not be interpreted as clinical superiority, approval probability, or confirmed product ownership."
        ),
        "known_limitations": [
            "MVP v1 compares ClinicalTrials.gov trial activity only.",
            "Sponsor search depends on ClinicalTrials.gov sponsor naming and may miss subsidiaries, collaborators, or spelling variants.",
            "Returned records may require manual review of sponsor or product association before being described as company activity.",
            "Trial counts do not imply clinical success, regulatory approval probability, commercial strength, or confirmed product ownership.",
        ],
    }


def compare_companies_by_indication(indication: str | None = None, **kwargs):
    clean_indication = indication or kwargs.get("indication")
    if not isinstance(clean_indication, str) or not clean_indication.strip():
        return build_error(ErrorCode.INVALID_PARAMETER, "indication must be a non-empty string")
    clean_indication = clean_indication.strip()

    companies = _as_string_list(kwargs.get("companies"), "companies", required=True)
    if isinstance(companies, dict) and "error" in companies:
        return companies

    registries = _normalize_registries(kwargs.get("registries"))
    if isinstance(registries, dict) and "error" in registries:
        return registries

    date_range = _normalize_date_range(kwargs.get("date_range", "3y"))
    if isinstance(date_range, dict) and "error" in date_range:
        return date_range

    product_modality = _as_string_list(kwargs.get("product_modality"), "product_modality")
    if isinstance(product_modality, dict) and "error" in product_modality:
        return product_modality

    phase_filter = _as_string_list(kwargs.get("phase"), "phase")
    if isinstance(phase_filter, dict) and "error" in phase_filter:
        return phase_filter

    include_completed_trials = kwargs.get("include_completed_trials", True)
    if not isinstance(include_completed_trials, bool):
        return build_error(ErrorCode.INVALID_PARAMETER, "include_completed_trials must be a boolean")

    include_results = kwargs.get("include_results", True)
    if not isinstance(include_results, bool):
        return build_error(ErrorCode.INVALID_PARAMETER, "include_results must be a boolean")

    page_size = _parse_limit(kwargs.get("page_size", kwargs.get("limit")))
    if isinstance(page_size, dict) and "error" in page_size:
        return page_size

    source_errors = []
    company_comparison = []

    for company in companies:
        result = search_clinical_trials_by_indication(
            clean_indication,
            sponsor=company,
            page_size=page_size,
        )
        if isinstance(result, dict) and "error" in result:
            source_errors.append({"company": company, "error": result["error"]})
            company_comparison.append(_company_not_evaluable_summary(company, result["error"]))
            continue

        trials = result.get("trials", []) if isinstance(result, dict) else []
        filtered_trials = [
            trial for trial in trials
            if _trial_matches_filters(
                trial,
                product_modality=product_modality,
                phase_filter=phase_filter,
                include_completed_trials=include_completed_trials,
                include_results=include_results,
            )
        ]
        company_comparison.append(_company_summary(company, filtered_trials, page_size=page_size))

    data_gaps = [
        "MVP v1 uses ClinicalTrials.gov only; no EU CTIS, WHO ICTRP, literature, patent, finance, or commercial intelligence sources are included.",
        "date_range is recorded in query metadata only; date-based trial filtering is not applied in MVP v1.",
        "Company matching is sponsor-name based and does not infer corporate family relationships.",
        "Company association is query-result metadata only; sponsor identity and product ownership require manual review.",
        "This output compares trial activity only and does not rank company superiority.",
    ]
    if source_errors:
        data_gaps.append("One or more sponsor searches returned source errors; review query_metadata.source_errors.")
        data_gaps.append("Companies with source errors are not evaluable; not evaluable must not be interpreted as zero trial activity.")

    evaluable_count = sum(1 for item in company_comparison if item.get("activity_evaluable", True))
    not_evaluable_count = len(company_comparison) - evaluable_count
    total_trials = sum((item["trial_count"] or 0) for item in company_comparison if item.get("activity_evaluable", True))
    non_sponsor_record_count = sum(
        (item.get("non_sponsor_record_count") or 0) for item in company_comparison if item.get("activity_evaluable", True)
    )

    overall_trends = [f"{len(companies)} company query/queries compared for {clean_indication}."]
    if evaluable_count:
        overall_trends.append(
            f"{total_trials} matching ClinicalTrials.gov trial record(s) included among {evaluable_count} evaluable company query/queries after MVP filters."
        )
        if non_sponsor_record_count:
            overall_trends.append(
                f"{non_sponsor_record_count} returned record(s) do not have sponsor names matching the requested company and require manual association review."
            )
    else:
        overall_trends.append(
            "No company-level ClinicalTrials.gov trial activity total is reported because all sponsor lookups were not evaluable."
        )
    if not_evaluable_count:
        overall_trends.append(
            f"{not_evaluable_count} company(ies) not evaluable because one or more source lookups returned errors."
        )

    return {
        "company_comparison": company_comparison,
        "landscape_summary": {
            "indication": clean_indication,
            "companies_compared": companies,
            "registries_searched": registries,
            "overall_trends": overall_trends,
            "data_gaps": data_gaps,
        },
        "query_metadata": {
            "lookup_mode": "clinicaltrials_gov_sponsor_activity_mvp",
            "indication": clean_indication,
            "companies": companies,
            "registries": registries,
            "date_range": date_range,
            "date_range_filter_applied": False,
            "product_modality": product_modality,
            "phase": phase_filter,
            "include_completed_trials": include_completed_trials,
            "include_results": include_results,
            "association_mode": "clinicaltrials_gov_query_result_mvp",
            "source_errors": source_errors,
            "known_limitations": data_gaps,
        },
    }
