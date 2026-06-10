# Canonical Dashboard Data Schema Contract

Status: Draft schema contract / docs-spec only  
Last updated: 2026-06-10

## 1. Purpose

This document defines the canonical dashboard data schema families that should sit between official source ingestion and future dashboard/digest artifacts.

It follows the dashboard-first architecture established in `docs/dashboard_target_architecture.md` and keeps implementation controlled by defining data contracts before adding any dashboard renderer, GitHub Actions workflow, source connector, scheduler, persistence layer, or new MCP tool.

The contract is intended to support four future dashboard surfaces:

1. Regulatory / guidance updates.
2. Biologic or therapeutic modality view.
3. Clinical trial tracker.
4. Source health / source-change monitor.

This document is not a runtime implementation.

## 2. Scope

This contract defines four schema families:

```text
RegulatoryGuidanceUpdate
ClinicalTrialUpdate
SourceHealthEvent
DashboardDigestSummary
```

These schema families are designed for JSON, CSV, Markdown digest, or static dashboard artifacts, but this document does not implement artifact generation.

## 3. Shared Field Principles

Every dashboard-facing record should preserve:

- source identity;
- official URL or registry URL;
- date evidence;
- query/filter context;
- source-health caveats;
- human-review caveats;
- enough stable identifiers for deduplication and traceability;
- enough tags to support modality, topic, indication, and source-category filtering.

Records must not contain confidential, non-public, vendor-confidential, GMP raw, QA-approved, official submission, or private company data.

## 4. Shared Base Fields

All schema families should include the following base fields where applicable.

| Field | Type | Required | Notes |
|---|---:|---:|---|
| `record_id` | string | Yes | Stable deterministic ID generated from source, source record identifier, date, and URL where possible. |
| `schema_name` | string | Yes | One of the canonical schema family names. |
| `schema_version` | string | Yes | Start with `0.1-draft` for docs/spec contracts. |
| `source_name` | string | Yes | Example: FDA, TFDA, ClinicalTrials.gov, EMA, ICH. |
| `source_category` | string | Yes | Example: agency, registry, global_harmonisation_guidance, source_health. |
| `source_url` | string | Conditional | Official source page, API URL, registry URL, or document URL. |
| `retrieved_at` | string | Conditional | ISO 8601 timestamp for future runtime retrieval. Not required in docs/spec examples. |
| `record_date` | string | Conditional | Primary date used for dashboard filtering. |
| `date_window_bucket` | string | Conditional | One of 1_month, 3_months, 6_months, 1_year, 3_years, 5_years, outside_window, unknown. |
| `query_context` | object | Optional | Original dashboard filter/query context if generated from a search. |
| `source_health_status` | string | Conditional | pass, warning, failed, source_unavailable, unknown. |
| `human_review_required` | boolean | Yes | Default true for regulatory/clinical intelligence outputs. |
| `limitations` | array[string] | Optional | Known caveats and source limitations. |

## 5. Schema: RegulatoryGuidanceUpdate

### 5.1 Purpose

Represents a regulatory, legal, guidance, or regulator-linked update shown in the dashboard.

This schema is intended for official or high-reliability public source updates from approved sources and future expansion candidates such as FDA, TFDA, EMA, NMPA/CDE, PMDA, and ICH.

### 5.2 Source Classification Rules

- FDA, TFDA, EMA, NMPA/CDE, and PMDA should be classified as agency or regulator-linked source records.
- ICH should be classified as `global_harmonisation_guidance`, not as a drug-review agency and not as a clinical trial registry.
- Source expansion candidates must not be treated as approved runtime sources until separately approved.

### 5.3 Fields

| Field | Type | Required | Notes |
|---|---:|---:|---|
| `record_id` | string | Yes | Stable update ID. |
| `schema_name` | string | Yes | `RegulatoryGuidanceUpdate`. |
| `source_name` | string | Yes | FDA, TFDA, EMA, NMPA_CDE, PMDA, ICH, etc. |
| `source_category` | string | Yes | agency, regulator_linked, global_harmonisation_guidance. |
| `region` | string | Optional | US, TW, EU, CN, JP, global. |
| `title` | string | Yes | Official or normalized title. |
| `document_type` | string | Optional | guidance, law, regulation, announcement, Q&A, inspection, safety, other. |
| `published_date` | string | Optional | Source publication date. |
| `updated_date` | string | Optional | Source update date. |
| `effective_date` | string | Optional | Effective date if available. |
| `adoption_date` | string | Optional | Especially relevant to ICH or harmonised guidance. |
| `record_date` | string | Conditional | Preferred dashboard date, chosen from update/publication/effective/adoption date. |
| `official_url` | string | Yes | Official page or document URL. |
| `attachment_urls` | array[string] | Optional | PDF, Word, XML, HTML attachments. |
| `summary_or_snippet` | string | Optional | Short source-aware description. |
| `topic_tags` | array[string] | Optional | Example: CMC, clinical, safety, quality, labeling, GMP. |
| `modality_tags` | array[string] | Optional | Example: biologic, recombinant_protein, antibody, cell_therapy. |
| `guideline_family` | string | Optional | Useful for ICH, such as Q, E, M, S. |
| `guideline_code` | string | Optional | Example: Q5, Q7, Q9, Q10, Q12, Q14. |
| `guideline_stage_or_status` | string | Optional | draft, final, adopted, revised, withdrawn, unknown. |
| `implementation_topic` | string | Optional | Topic affected by guidance implementation. |
| `date_window_bucket` | string | Conditional | Dashboard filter bucket. |
| `source_health_status` | string | Conditional | Linked source-health state. |
| `evidence_caveats` | array[string] | Optional | Caveats about missing dates, source access limits, or partial metadata. |
| `human_review_required` | boolean | Yes | Must default to true. |

### 5.4 Minimum Example

```json
{
  "record_id": "example-reg-guidance-001",
  "schema_name": "RegulatoryGuidanceUpdate",
  "schema_version": "0.1-draft",
  "source_name": "ICH",
  "source_category": "global_harmonisation_guidance",
  "region": "global",
  "title": "Example ICH quality guideline update",
  "document_type": "guidance",
  "published_date": "2026-01-15",
  "record_date": "2026-01-15",
  "official_url": "https://example.invalid/official-guidance",
  "topic_tags": ["quality", "CMC"],
  "modality_tags": ["biologic"],
  "guideline_family": "Q",
  "guideline_code": "Q-example",
  "date_window_bucket": "6_months",
  "source_health_status": "unknown",
  "human_review_required": true,
  "evidence_caveats": ["Illustrative mock record only; not a real source record."]
}
```

## 6. Schema: ClinicalTrialUpdate

### 6.1 Purpose

Represents a clinical trial status, registry, or result-availability update for dashboard tracking by indication, sponsor/company name, intervention, phase, and status.

The approved MVP registry source remains ClinicalTrials.gov API v2. Any other registry source requires separate feasibility and approval.

### 6.2 Fields

| Field | Type | Required | Notes |
|---|---:|---:|---|
| `record_id` | string | Yes | Stable trial update ID. |
| `schema_name` | string | Yes | `ClinicalTrialUpdate`. |
| `registry_name` | string | Yes | ClinicalTrials.gov, EU CTIS, WHO ICTRP, etc. |
| `registry_id` | string | Yes | Example: NCT ID. |
| `registry_url` | string | Yes | Official registry record URL. |
| `trial_title` | string | Yes | Official trial title. |
| `brief_title` | string | Optional | Short title if provided. |
| `condition_or_indication` | array[string] | Yes | Conditions or indications from registry. |
| `sponsor` | string | Optional | Sponsor name as reported by registry. |
| `collaborators` | array[string] | Optional | Collaborators as reported by registry. |
| `interventions` | array[string] | Optional | Drug/biologic/device/procedure names. |
| `intervention_types` | array[string] | Optional | drug, biologic, device, procedure, behavioral, other. |
| `phase` | string | Optional | Phase 1, Phase 2, Phase 3, etc. |
| `trial_status` | string | Optional | recruiting, active_not_recruiting, completed, terminated, unknown. |
| `start_date` | string | Optional | Registry start date. |
| `primary_completion_date` | string | Optional | Registry primary completion date. |
| `completion_date` | string | Optional | Registry completion date. |
| `last_update_posted` | string | Optional | Registry last update date. |
| `results_available` | boolean | Optional | Whether official results are posted. |
| `results_first_posted` | string | Optional | Official results first posted date. |
| `results_url` | string | Optional | Official results page URL. |
| `record_date` | string | Conditional | Preferred dashboard date, usually last_update_posted. |
| `indication_tags` | array[string] | Optional | Normalized indication tags. |
| `modality_tags` | array[string] | Optional | Normalized modality tags, rule-based unless separately approved. |
| `source_health_status` | string | Conditional | Registry/source health state. |
| `evidence_caveats` | array[string] | Optional | Caveats about sponsor names, missing fields, registry limitations. |
| `human_review_required` | boolean | Yes | Must default to true. |

### 6.3 Required Interpretation Limits

This schema must not be used to infer:

- clinical success;
- regulatory approval probability;
- company superiority;
- commercial strength;
- product ownership beyond the registry-reported sponsor/collaborator fields;
- corporate-family or alias relationships.

### 6.4 Minimum Example

```json
{
  "record_id": "example-clinical-trial-001",
  "schema_name": "ClinicalTrialUpdate",
  "schema_version": "0.1-draft",
  "registry_name": "ClinicalTrials.gov",
  "registry_id": "NCT00000000",
  "registry_url": "https://clinicaltrials.gov/study/NCT00000000",
  "trial_title": "Example biologic trial in example indication",
  "condition_or_indication": ["Example indication"],
  "sponsor": "Example Sponsor",
  "interventions": ["Example biologic"],
  "phase": "Phase 2",
  "trial_status": "completed",
  "last_update_posted": "2026-02-01",
  "results_available": false,
  "record_date": "2026-02-01",
  "date_window_bucket": "6_months",
  "source_health_status": "unknown",
  "human_review_required": true,
  "evidence_caveats": ["Illustrative mock record only; not a real trial."]
}
```

## 7. Schema: SourceHealthEvent

### 7.1 Purpose

Represents a source-access, API, parser, webpage, or abnormal-record-count event that affects dashboard reliability.

This schema supports the source health / source-change monitor tab and should prevent source failures from being misread as no results.

### 7.2 Fields

| Field | Type | Required | Notes |
|---|---:|---:|---|
| `record_id` | string | Yes | Stable source-health event ID. |
| `schema_name` | string | Yes | `SourceHealthEvent`. |
| `source_name` | string | Yes | FDA, TFDA, ClinicalTrials.gov, etc. |
| `source_category` | string | Yes | agency, registry, guidance, source_health. |
| `check_name` | string | Yes | Name of source check. |
| `checked_at` | string | Conditional | Future runtime check timestamp. |
| `status` | string | Yes | pass, warning, failed, source_unavailable, unknown. |
| `failure_type` | string | Optional | http_error, parser_error, schema_change, egress_block, abuse_detection, no_response, abnormal_record_delta, other. |
| `http_status` | integer | Optional | HTTP status where applicable. |
| `parser_error_message` | string | Optional | Short non-secret diagnostic message. |
| `schema_changed_flag` | boolean | Optional | True if API/schema changed. |
| `html_selector_changed_flag` | boolean | Optional | True if webpage selector likely changed. |
| `record_count_current` | integer | Optional | Current count from check. |
| `record_count_previous` | integer | Optional | Previous count if historical state exists. |
| `record_count_delta` | integer | Optional | Difference between current and prior count. |
| `recommended_action` | string | Optional | Human-readable next action. |
| `blocks_dashboard_use` | boolean | Optional | Whether this event should block or caveat dashboard output. |
| `human_review_required` | boolean | Yes | Must default to true. |

### 7.3 Required Interpretation Rules

- `pass` does not prove complete source coverage.
- `failed` or `source_unavailable` must not be interpreted as no records.
- FDA abuse-detection or apology responses must remain source-access limitations, not no-result evidence.
- Abnormal record deltas should be warnings until reviewed.

### 7.4 Minimum Example

```json
{
  "record_id": "example-source-health-001",
  "schema_name": "SourceHealthEvent",
  "schema_version": "0.1-draft",
  "source_name": "FDA",
  "source_category": "agency",
  "check_name": "fda-regulatory-update-search",
  "status": "source_unavailable",
  "failure_type": "abuse_detection",
  "parser_error_message": "Source returned an access-limitation page instead of expected results.",
  "blocks_dashboard_use": true,
  "recommended_action": "Review source access and do not interpret as zero results.",
  "human_review_required": true
}
```

## 8. Schema: DashboardDigestSummary

### 8.1 Purpose

Represents a high-level digest artifact produced from dashboard records for Claude Project or PM/RA review.

This schema is for source-aware summary metadata and does not authorize an automated final report generator.

### 8.2 Fields

| Field | Type | Required | Notes |
|---|---:|---:|---|
| `record_id` | string | Yes | Stable digest ID. |
| `schema_name` | string | Yes | `DashboardDigestSummary`. |
| `digest_title` | string | Yes | Human-readable digest title. |
| `digest_period_start` | string | Optional | Start date for digest period. |
| `digest_period_end` | string | Optional | End date for digest period. |
| `generated_at` | string | Conditional | Future artifact generation time. |
| `source_names` | array[string] | Yes | Sources included. |
| `source_health_summary` | array[string] | Optional | Source-health caveats and status notes. |
| `regulatory_update_count` | integer | Optional | Count of included regulatory/guidance records. |
| `clinical_trial_update_count` | integer | Optional | Count of included clinical trial records. |
| `high_impact_items` | array[object] | Optional | Pointer records, not unsupported conclusions. |
| `missing_or_unavailable_sources` | array[string] | Optional | Sources excluded due to access or scope. |
| `dashboard_artifact_links` | array[string] | Optional | Links to generated artifacts if later approved. |
| `human_review_required` | boolean | Yes | Must default to true. |
| `limitations` | array[string] | Yes | Required caveats. |

### 8.3 Minimum Example

```json
{
  "record_id": "example-dashboard-digest-001",
  "schema_name": "DashboardDigestSummary",
  "schema_version": "0.1-draft",
  "digest_title": "Example regulatory and clinical dashboard summary",
  "digest_period_start": "2026-01-01",
  "digest_period_end": "2026-01-31",
  "source_names": ["FDA", "TFDA", "ClinicalTrials.gov"],
  "source_health_summary": ["Example caveat only; no live source check was run."],
  "regulatory_update_count": 0,
  "clinical_trial_update_count": 0,
  "missing_or_unavailable_sources": [],
  "human_review_required": true,
  "limitations": ["Illustrative mock digest only; not a generated dashboard artifact."]
}
```

## 9. Date Window Contract

Dashboard date windows should use the following normalized values:

```text
1_month
3_months
6_months
1_year
3_years
5_years
outside_window
unknown
```

Date-window assignment should be based on the selected dashboard reference date and the best available source date.

Priority for regulatory/guidance records:

```text
updated_date -> published_date -> effective_date -> adoption_date -> unknown
```

Priority for clinical trial records:

```text
last_update_posted -> results_first_posted -> primary_completion_date -> completion_date -> start_date -> unknown
```

## 10. Tagging Contract

### 10.1 Modality Tags

Initial normalized modality tags may include:

```text
small_molecule
peptide
oligonucleotide_or_rna
recombinant_protein
monoclonal_antibody
antibody_drug_conjugate
vaccine
cell_therapy
gene_therapy
radiopharmaceutical
biosimilar
combination_product
other
unknown
```

### 10.2 Topic Tags

Initial normalized topic tags may include:

```text
CMC
quality
GMP
clinical
nonclinical
safety
labeling
inspection
postmarket
pharmacovigilance
submission
trial_results
source_health
other
unknown
```

### 10.3 Indication Tags

Initial indication tags should be text-normalized from source records. Disease ontology integration is not approved by this contract.

## 11. Storage And Artifact Boundary

This contract allows future discussion of JSON, CSV, Markdown, or static HTML dashboard artifacts, but it does not approve storage or persistence implementation.

Any persistent store, committed data snapshot, artifact upload, branch publication, GitHub Pages deployment, database, or retention policy requires separate approval.

## 12. Explicit Non-Goals

This contract does not add or approve:

- runtime dashboard renderer;
- GitHub Actions workflow;
- scheduled ingestion;
- alert or notification workflow;
- GitHub Pages publication;
- database or persistence layer;
- new MCP tool;
- `.mcp.json` change;
- new source connector;
- EMA, NMPA/CDE, PMDA, ICH, WHO ICTRP, EU CTIS, literature, patent, finance, or news integration;
- company alias database;
- corporate-family mapping;
- product ownership inference;
- clinical success scoring;
- approval probability scoring;
- management decision automation;
- CMC weekly management report template;
- confidential or non-public record storage.

## 13. Recommended Next Step

After this schema contract is reviewed, the next controlled PR should be one of:

```text
Add static dashboard dry-run design using mock data
Add dashboard artifact contract for JSON/CSV/Markdown outputs
Add MVP-source dashboard export planning contract
```

The next PR should remain docs/spec-only unless runtime dashboard work is explicitly approved.
