from src.classifiers.product_modality_classifier import classify_product_modality
from src.core.models import ClinicalTrialRecord, RegulatoryUpdate


def _as_dict(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def normalize_fda_record(raw: dict, *, retrieved_at: str) -> RegulatoryUpdate:
    # TODO: map official openFDA/FDA update schema fields.
    return RegulatoryUpdate(
        id=str(raw.get("id", "")), agency="FDA", region="US", title=raw.get("title", ""),
        publication_date=raw.get("publication_date"), last_update_date=raw.get("last_update_date"),
        retrieved_at=retrieved_at, official_url=raw.get("official_url", ""), source_type=raw.get("source_type", "API"),
        document_type=raw.get("document_type", "unknown"), document_status=raw.get("document_status", "unknown"),
        product_modality=raw.get("product_modality", []), topics=raw.get("topics", []), summary=raw.get("summary", ""),
        known_limitations=raw.get("known_limitations", ["MVP v1 placeholder mapping"]) )


def normalize_tfda_record(raw: dict, *, retrieved_at: str) -> RegulatoryUpdate:
    # TODO: map TFDA official endpoint fields.
    return RegulatoryUpdate(
        id=str(raw.get("id", "")), agency="TFDA", region="Taiwan", title=raw.get("title", ""),
        publication_date=raw.get("publication_date"), last_update_date=raw.get("last_update_date"),
        retrieved_at=retrieved_at, official_url=raw.get("official_url", ""), source_type=raw.get("source_type", "API"),
        document_type=raw.get("document_type", "unknown"), document_status=raw.get("document_status", "unknown"),
        product_modality=raw.get("product_modality", []), topics=raw.get("topics", []), summary=raw.get("summary", ""),
        known_limitations=raw.get("known_limitations", ["MVP v1 placeholder mapping"]) )


def normalize_clinicaltrials_record(raw: dict, *, retrieved_at: str) -> ClinicalTrialRecord:
    protocol = raw.get("protocolSection", {}) if isinstance(raw, dict) else {}
    if not isinstance(protocol, dict):
        protocol = {}

    identification = protocol.get("identificationModule", {})
    status_module = protocol.get("statusModule", {})
    conditions_module = protocol.get("conditionsModule", {})
    sponsor_module = protocol.get("sponsorCollaboratorsModule", {})
    design_module = protocol.get("designModule", {})
    contacts_module = protocol.get("contactsLocationsModule", {})
    arms_module = protocol.get("armsInterventionsModule", {})
    outcomes_module = protocol.get("outcomesModule", {})
    description_module = protocol.get("descriptionModule", {})

    identification = identification if isinstance(identification, dict) else {}
    status_module = status_module if isinstance(status_module, dict) else {}
    conditions_module = conditions_module if isinstance(conditions_module, dict) else {}
    sponsor_module = sponsor_module if isinstance(sponsor_module, dict) else {}
    design_module = design_module if isinstance(design_module, dict) else {}
    contacts_module = contacts_module if isinstance(contacts_module, dict) else {}
    arms_module = arms_module if isinstance(arms_module, dict) else {}
    outcomes_module = outcomes_module if isinstance(outcomes_module, dict) else {}
    description_module = description_module if isinstance(description_module, dict) else {}

    nct_id = identification.get("nctId") or raw.get("nctId") or raw.get("trial_id", "")
    official_url = f"https://clinicaltrials.gov/study/{nct_id}" if nct_id else raw.get("official_url", "")

    interventions = [
        intervention.get("name", "")
        for intervention in arms_module.get("interventions", [])
        if isinstance(intervention, dict) and intervention.get("name")
    ]
    indications = conditions_module.get("conditions", []) or raw.get("indications", [])
    brief_summary = description_module.get("briefSummary", "")
    title = identification.get("briefTitle") or raw.get("title", "")
    sponsor = _as_dict(sponsor_module.get("leadSponsor", {})).get("name") or raw.get("sponsor", "")
    collaborators = [
        collaborator.get("name", "")
        for collaborator in sponsor_module.get("collaborators", [])
        if isinstance(collaborator, dict) and collaborator.get("name")
    ]
    phase_list = design_module.get("phases", [])
    phase = phase_list[0] if phase_list else raw.get("phase", "unknown")
    status = status_module.get("overallStatus") or raw.get("status", "unknown")
    countries = [
        location.get("country", "")
        for location in contacts_module.get("locations", [])
        if isinstance(location, dict) and location.get("country")
    ]
    primary_outcomes = [
        outcome.get("measure", "")
        for outcome in outcomes_module.get("primaryOutcomes", [])
        if isinstance(outcome, dict) and outcome.get("measure")
    ]

    modality_text = " ".join(interventions + [title, brief_summary])
    modality = classify_product_modality(modality_text).get("product_modality", ["unknown"])

    known_limitations = raw.get("known_limitations", [])
    if not brief_summary:
        known_limitations.append("ClinicalTrials.gov briefSummary missing from API response.")

    return ClinicalTrialRecord(
        trial_id=nct_id,
        registry="ClinicalTrials.gov",
        official_url=official_url,
        title=title,
        sponsor=sponsor,
        retrieved_at=retrieved_at,
        indications=indications,
        intervention_names=interventions,
        product_modality=modality,
        phase=phase,
        status=status,
        countries=countries,
        start_date=_as_dict(status_module.get("startDateStruct", {})).get("date") or raw.get("start_date"),
        primary_completion_date=_as_dict(status_module.get("primaryCompletionDateStruct", {})).get("date") or raw.get("primary_completion_date"),
        last_update_date=_as_dict(status_module.get("lastUpdateSubmitDateStruct", {})).get("date") or raw.get("last_update_date"),
        results_available=(status_module.get("hasResults") if "hasResults" in status_module else raw.get("results_available")),
        primary_outcomes=primary_outcomes,
        known_limitations=known_limitations,
    )
