from src.core.models import ClinicalTrialRecord, RegulatoryUpdate


def regulatory_update_key(record: RegulatoryUpdate) -> tuple:
    return (record.agency, record.official_url, record.title, record.publication_date or record.last_update_date, record.content_hash)


def clinical_trial_key(record: ClinicalTrialRecord) -> tuple:
    return (record.registry, record.trial_id)


def dedupe_regulatory_updates(records: list[RegulatoryUpdate]) -> list[RegulatoryUpdate]:
    seen = set(); out = []
    for r in records:
        k = regulatory_update_key(r)
        if k not in seen:
            seen.add(k); out.append(r)
    return out
