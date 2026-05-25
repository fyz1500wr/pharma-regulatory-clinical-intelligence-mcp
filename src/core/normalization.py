from src.core.models import ClinicalTrialRecord, RegulatoryUpdate


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
    # TODO: map ClinicalTrials.gov API v2 study fields.
    return ClinicalTrialRecord(
        trial_id=raw.get("trial_id", ""), registry="ClinicalTrials.gov", official_url=raw.get("official_url", ""),
        title=raw.get("title", ""), sponsor=raw.get("sponsor", ""), retrieved_at=retrieved_at,
        indications=raw.get("indications", []), intervention_names=raw.get("intervention_names", []),
        product_modality=raw.get("product_modality", []), phase=raw.get("phase", "unknown"),
        status=raw.get("status", "unknown"), countries=raw.get("countries", []),
        start_date=raw.get("start_date"), primary_completion_date=raw.get("primary_completion_date"),
        last_update_date=raw.get("last_update_date"), results_available=raw.get("results_available"),
        primary_outcomes=raw.get("primary_outcomes", []), known_limitations=raw.get("known_limitations", ["MVP v1 placeholder mapping"]),
    )
