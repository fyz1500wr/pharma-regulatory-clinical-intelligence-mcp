from dataclasses import asdict
from datetime import datetime, timezone

from src.connectors.clinical_trials.clinicaltrials_gov_client import ClinicalTrialsGovClient
from src.core.errors import ErrorCode, build_error
from src.core.normalization import normalize_clinicaltrials_record


def search_clinical_trials_by_indication(indication: str, **kwargs):
    if not indication or not indication.strip():
        return build_error(ErrorCode.INVALID_PARAMETER, "indication is required")

    client = ClinicalTrialsGovClient()
    result = client.search_studies(
        indication=indication.strip(),
        page_size=kwargs.get("page_size", 20),
        sponsor=kwargs.get("sponsor"),
        phase=kwargs.get("phase"),
        status=kwargs.get("status"),
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
                "indication": indication.strip(),
                "registries_searched": ["ClinicalTrials.gov"],
                "known_limitations": ["Only ClinicalTrials.gov API v2 is active in MVP v1."],
            },
        }

    retrieved_at = datetime.now(timezone.utc).isoformat()
    normalized = [asdict(normalize_clinicaltrials_record(raw=study, retrieved_at=retrieved_at)) for study in studies]

    return {
        "trials": normalized,
        "query_metadata": {
            "indication": indication.strip(),
            "registries_searched": ["ClinicalTrials.gov"],
            "known_limitations": [
                "MVP v1 currently queries ClinicalTrials.gov only.",
                "Phase/status filters use conservative API v2 parameter mapping.",
            ],
        },
    }


def compare_companies_by_indication(**kwargs):
    return build_error(ErrorCode.DATA_NOT_INGESTED, "compare_companies_by_indication is not implemented in MVP v1 skeleton")
