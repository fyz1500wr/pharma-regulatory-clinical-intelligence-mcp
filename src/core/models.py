from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class RegulatoryUpdate:
    id: str
    agency: str
    region: str
    title: str
    retrieved_at: str
    official_url: str
    source_type: str
    document_type: str = "unknown"
    document_status: str = "unknown"
    publication_date: Optional[str] = None
    last_update_date: Optional[str] = None
    product_modality: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    summary: str = ""
    known_limitations: list[str] = field(default_factory=list)
    content_hash: Optional[str] = None


@dataclass
class ClinicalTrialRecord:
    trial_id: str
    registry: str
    official_url: str
    title: str
    sponsor: str
    retrieved_at: str
    indications: list[str] = field(default_factory=list)
    intervention_names: list[str] = field(default_factory=list)
    product_modality: list[str] = field(default_factory=list)
    phase: str = "unknown"
    status: str = "unknown"
    countries: list[str] = field(default_factory=list)
    start_date: Optional[str] = None
    primary_completion_date: Optional[str] = None
    last_update_date: Optional[str] = None
    results_available: Optional[bool] = None
    primary_outcomes: list[str] = field(default_factory=list)
    known_limitations: list[str] = field(default_factory=list)


@dataclass
class SourceHealthEvent:
    failure_id: str
    source_id: str
    agency_or_registry: str
    source_type: str
    endpoint_url: str
    status: str
    failure_type: str
    severity: str
    detected_at: str
    error_message: str
    suggested_fix: str
    resolved_at: Optional[str] = None
    last_successful_check: Optional[str] = None
    suggested_connector_file: Optional[str] = None
    known_limitations: list[str] = field(default_factory=list)


@dataclass
class DigestRecord:
    digest_id: str
    digest_type: str
    date_range: str
    generated_at: str
    sources_searched: list[str]
    search_criteria: dict[str, Any]
    key_regulatory_updates: list[dict[str, Any]] = field(default_factory=list)
    key_clinical_trial_updates: list[dict[str, Any]] = field(default_factory=list)
    source_health_summary: dict[str, Any] = field(default_factory=dict)
    known_limitations: list[str] = field(default_factory=list)
