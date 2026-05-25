from src.core.errors import build_error, ErrorCode


def search_clinical_trials_by_indication(indication: str, **kwargs):
    if not indication:
        return build_error(ErrorCode.INVALID_PARAMETER, "indication is required")
    return {"trials": [], "no_result_reason": "DATA_NOT_INGESTED", "suggested_next_action": "Ingest ClinicalTrials.gov MVP v1 data."}


def compare_companies_by_indication(**kwargs):
    return build_error(ErrorCode.DATA_NOT_INGESTED, "compare_companies_by_indication is not implemented in MVP v1 skeleton")
