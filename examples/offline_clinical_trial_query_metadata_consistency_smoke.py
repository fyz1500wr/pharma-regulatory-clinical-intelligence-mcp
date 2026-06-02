from __future__ import annotations

import json
import sys
from datetime import datetime as real_datetime
from datetime import timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.mcp_server import tools_clinical_trials


class OfflineClinicalTrialsGovClient:
    def search_studies(
        self,
        *,
        indication: str,
        page_size: int = 20,
        sponsor: str | None = None,
        phase: str | None = None,
        status: str | None = None,
        page_token: str | None = None,
    ) -> dict[str, Any]:
        studies = [
            _study(
                nct_id="NCT00000011",
                title="ADC Therapy in Gastric Cancer",
                sponsor="Example Oncology Inc.",
                conditions=["Gastric Cancer"],
                interventions=["HER2 antibody-drug conjugate"],
                phase="PHASE2",
                status="RECRUITING",
                country="Taiwan",
                start_date="2026-01",
                primary_completion_date="2027-06",
                last_update_date="2026-05-20",
                results_available=False,
                primary_outcomes=["Objective response rate"],
                summary="Offline ClinicalTrials.gov fixture for ADC gastric cancer metadata checks.",
            ),
            _study(
                nct_id="NCT00000012",
                title="PD-1 Antibody in Gastric Cancer",
                sponsor="Example Oncology Inc.",
                conditions=["Gastric Cancer"],
                interventions=["PD-1 monoclonal antibody"],
                phase="PHASE3",
                status="COMPLETED",
                country="United States",
                start_date="2024-02",
                primary_completion_date="2025-08",
                last_update_date="2026-04-12",
                results_available=True,
                primary_outcomes=["Overall survival"],
                summary="Completed control fixture for result availability checks.",
            ),
            _study(
                nct_id="NCT00000013",
                title="mRNA Vaccine in Melanoma",
                sponsor="Different Biotech Ltd.",
                conditions=["Melanoma"],
                interventions=["mRNA cancer vaccine"],
                phase="PHASE1",
                status="ACTIVE_NOT_RECRUITING",
                country="Japan",
                start_date="2025-03",
                primary_completion_date="2026-12",
                last_update_date="2026-05-01",
                results_available=False,
                primary_outcomes=["Safety"],
                summary="Out-of-indication control fixture.",
            ),
        ]

        filtered = [study for study in studies if _matches_indication(study, indication)]
        if sponsor:
            filtered = [study for study in filtered if _lead_sponsor(study).lower() == sponsor.strip().lower()]
        if phase:
            filtered = [study for study in filtered if _phase(study).upper() == phase.strip().upper()]
        if status:
            filtered = [study for study in filtered if _status(study).upper() == status.strip().upper()]
        return {"studies": filtered[:page_size]}


def _study(
    *,
    nct_id: str,
    title: str,
    sponsor: str,
    conditions: list[str],
    interventions: list[str],
    phase: str,
    status: str,
    country: str,
    start_date: str,
    primary_completion_date: str,
    last_update_date: str,
    results_available: bool,
    primary_outcomes: list[str],
    summary: str,
) -> dict[str, Any]:
    return {
        "protocolSection": {
            "identificationModule": {"nctId": nct_id, "briefTitle": title},
            "statusModule": {
                "overallStatus": status,
                "startDateStruct": {"date": start_date},
                "primaryCompletionDateStruct": {"date": primary_completion_date},
                "lastUpdateSubmitDateStruct": {"date": last_update_date},
                "hasResults": results_available,
            },
            "conditionsModule": {"conditions": conditions},
            "sponsorCollaboratorsModule": {"leadSponsor": {"name": sponsor}},
            "designModule": {"phases": [phase]},
            "contactsLocationsModule": {"locations": [{"country": country}]},
            "armsInterventionsModule": {"interventions": [{"name": item} for item in interventions]},
            "outcomesModule": {"primaryOutcomes": [{"measure": item} for item in primary_outcomes]},
            "descriptionModule": {"briefSummary": summary},
        }
    }


def _conditions(study: dict[str, Any]) -> list[str]:
    return study["protocolSection"]["conditionsModule"]["conditions"]


def _lead_sponsor(study: dict[str, Any]) -> str:
    return study["protocolSection"]["sponsorCollaboratorsModule"]["leadSponsor"]["name"]


def _phase(study: dict[str, Any]) -> str:
    return study["protocolSection"]["designModule"]["phases"][0]


def _status(study: dict[str, Any]) -> str:
    return study["protocolSection"]["statusModule"]["overallStatus"]


def _matches_indication(study: dict[str, Any], indication: str) -> bool:
    needle = indication.strip().lower()
    return any(needle in condition.lower() for condition in _conditions(study))


class _FixedDateTime:
    @staticmethod
    def now(tz=None):
        return real_datetime(2026, 6, 1, tzinfo=timezone.utc)

    @staticmethod
    def fromisoformat(value):
        return real_datetime.fromisoformat(value)


def _assert(condition: bool, payload: Any) -> None:
    if not condition:
        raise AssertionError(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def _assert_trial_contract(trial: dict[str, Any]) -> None:
    required_fields = [
        "trial_id",
        "registry",
        "official_url",
        "title",
        "sponsor",
        "retrieved_at",
        "indications",
        "intervention_names",
        "product_modality",
        "phase",
        "status",
        "countries",
        "start_date",
        "primary_completion_date",
        "last_update_date",
        "results_available",
        "primary_outcomes",
        "known_limitations",
    ]
    missing = [field for field in required_fields if field not in trial]
    _assert(missing == [], {"missing_fields": missing, "trial": trial})
    _assert(trial["registry"] == "ClinicalTrials.gov", trial)
    _assert(trial["trial_id"].startswith("NCT"), trial)
    _assert(trial["official_url"].startswith("https://clinicaltrials.gov/study/"), trial)
    _assert(isinstance(trial["indications"], list) and trial["indications"], trial)
    _assert(isinstance(trial["intervention_names"], list) and trial["intervention_names"], trial)
    _assert(isinstance(trial["product_modality"], list) and trial["product_modality"], trial)
    _assert(isinstance(trial["primary_outcomes"], list) and trial["primary_outcomes"], trial)
    _assert(isinstance(trial["results_available"], bool), trial)


def _assert_search_metadata(payload: dict[str, Any], *, indication: str) -> None:
    metadata = payload.get("query_metadata")
    _assert(isinstance(metadata, dict), payload)
    _assert(metadata.get("indication") == indication, metadata)
    _assert(metadata.get("registries_searched") == ["ClinicalTrials.gov"], metadata)
    _assert("known_limitations" in metadata, metadata)


def _assert_company_metadata(payload: dict[str, Any]) -> None:
    metadata = payload.get("query_metadata")
    _assert(isinstance(metadata, dict), payload)
    _assert(metadata.get("lookup_mode") == "clinicaltrials_gov_sponsor_activity_mvp", metadata)
    _assert(metadata.get("indication") == "Gastric Cancer", metadata)
    _assert(metadata.get("companies") == ["Example Oncology Inc."], metadata)
    _assert(metadata.get("registries") == ["ClinicalTrials.gov"], metadata)
    _assert(metadata.get("date_range") == "3y", metadata)
    _assert(metadata.get("date_range_filter_applied") is False, metadata)
    _assert(metadata.get("product_modality") == ["adc"], metadata)
    _assert(metadata.get("phase") == ["PHASE2"], metadata)
    _assert(metadata.get("include_completed_trials") is False, metadata)
    _assert(metadata.get("include_results") is False, metadata)
    _assert("source_errors" in metadata, metadata)
    _assert("known_limitations" in metadata, metadata)


def run_smoke() -> dict[str, Any]:
    original_client = tools_clinical_trials.ClinicalTrialsGovClient
    original_datetime = tools_clinical_trials.datetime

    try:
        tools_clinical_trials.ClinicalTrialsGovClient = OfflineClinicalTrialsGovClient
        tools_clinical_trials.datetime = _FixedDateTime

        search_payload = tools_clinical_trials.search_clinical_trials_by_indication(
            "Gastric Cancer",
            page_size=10,
        )
        _assert("error" not in search_payload, search_payload)
        _assert(len(search_payload.get("trials", [])) == 2, search_payload)
        _assert_search_metadata(search_payload, indication="Gastric Cancer")
        for trial in search_payload["trials"]:
            _assert_trial_contract(trial)

        company_payload = tools_clinical_trials.compare_companies_by_indication(
            indication="Gastric Cancer",
            companies="Example Oncology Inc.",
            registries="ClinicalTrials.gov",
            date_range="3y",
            product_modality="adc",
            phase="PHASE2",
            include_completed_trials=False,
            include_results=False,
            page_size=10,
        )
        _assert("error" not in company_payload, company_payload)
        _assert_company_metadata(company_payload)
        company_summary = company_payload["company_comparison"][0]
        _assert(company_summary["company"] == "Example Oncology Inc.", company_summary)
        _assert(company_summary["trial_count"] == 1, company_summary)
        _assert(company_summary["active_trial_count"] == 1, company_summary)
        _assert(company_summary["completed_trial_count"] == 0, company_summary)
        _assert(company_summary["key_trials"][0]["results_available"] is False, company_summary)
        _assert(company_summary["key_trials"][0]["official_url"].endswith("NCT00000011"), company_summary)

        summary = {
            "status": "passed",
            "validated_cases": [
                "ClinicalTrials.gov normalized trial metadata contract",
                "clinical trial indication query metadata contract",
                "clinical trial sponsor/company query metadata contract",
                "clinical trial date_range metadata recorded but not applied",
                "clinical trial product_modality filter metadata contract",
                "clinical trial phase filter metadata contract",
                "clinical trial include_completed_trials metadata contract",
                "clinical trial include_results metadata contract",
                "clinical trial official_url and results_available fields",
            ],
            "important_interpretation": (
                "This offline smoke validates ClinicalTrials.gov-style query metadata consistency only. "
                "It does not validate live ClinicalTrials.gov availability or approve source expansion."
            ),
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        print("offline clinical trial query metadata consistency smoke passed")
        return summary

    finally:
        tools_clinical_trials.ClinicalTrialsGovClient = original_client
        tools_clinical_trials.datetime = original_datetime


if __name__ == "__main__":
    run_smoke()
