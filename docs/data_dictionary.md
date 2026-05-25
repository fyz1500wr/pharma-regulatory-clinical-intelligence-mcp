# Data Dictionary

## 1. Purpose

This document defines the standard data fields used by the Pharmaceutical Regulatory and Clinical Intelligence System.

It provides a common vocabulary for regulatory updates, clinical trial records, source health events, and digest/report records.

This file is a **data field governance document**. It is not a SQL schema, ORM model, parser specification, GitHub Actions configuration, or Claude prompt template.

The data dictionary supports:

```text
docs/source_priority_matrix.md
docs/product_modality_taxonomy.md
docs/mcp_tool_contract.md
workflows/regulatory_clinical_intelligence_workflow.md
```

---

## 2. General Field Rules

### 2.1 Date Format

All dates should use ISO format:

```text
YYYY-MM-DD
```

All datetimes should use ISO 8601 format:

```text
YYYY-MM-DDTHH:MM:SSZ
```

When timezone is unknown, preserve the source-provided value and note the limitation.

### 2.2 Publication Date Is Not Retrieval Date

Do not confuse:

| Field | Meaning |
|---|---|
| `publication_date` | Date the agency or registry published the item |
| `last_update_date` | Date the source says the item was last updated |
| `retrieved_at` | Date and time this system retrieved the item |
| `effective_date` | Date a rule, guidance, or requirement becomes effective |
| `consultation_deadline` | Deadline for public comment or consultation |

If a source does not provide a date, use `null` and add a note in `known_limitations`.

### 2.3 Official URL Required

Every primary record should preserve an official source URL.

If a URL is missing, the record should be marked:

```text
requires_manual_review
```

or include a clear limitation.

### 2.4 Source Type Required

Each record must identify how the data was obtained.

Approved `source_type` values:

```text
API
RSS
open_data
downloadable_file
official_html
parser
manual_import
unknown
```

### 2.5 Product Modality Labels

Use the approved labels from:

```text
docs/product_modality_taxonomy.md
```

Do not use:

```text
biologic_type
```

Use:

```text
product_modality
```

### 2.6 Unknown and Manual Review

Use controlled values instead of guessing:

```text
unknown
requires_manual_review
```

Use `unknown` when no reliable information is available.

Use `requires_manual_review` when information exists but automated classification may be misleading.

---

## 3. Common Fields

These fields may appear across multiple record types.

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | string | Yes | Internal stable identifier for the normalized record |
| `source_id` | string | Conditional | Identifier for the configured source endpoint or feed |
| `agency` | string | Conditional | Regulatory agency, such as FDA, EMA, TFDA, NMPA, CDE, or PMDA |
| `registry` | string | Conditional | Clinical trial registry, such as ClinicalTrials.gov |
| `region` | string | Conditional | Region or jurisdiction, such as US, EU, Taiwan, China, or Japan |
| `title` | string | Yes | Official title or normalized title |
| `official_url` | string | Yes | Official source URL |
| `source_type` | enum | Yes | API, RSS, open_data, downloadable_file, official_html, parser, manual_import, or unknown |
| `retrieved_at` | datetime | Yes | Date and time when the system retrieved the record |
| `content_hash` | string | Optional | Hash or fingerprint of content for change detection |
| `classification_confidence` | enum | Conditional | high, medium, low, or requires_manual_review |
| `known_limitations` | list[string] | Optional | Known limitations, missing fields, or source issues |

---

## 4. RegulatoryUpdate

### 4.1 Purpose

`RegulatoryUpdate` represents a regulatory document, announcement, guidance, notice, Q&A, safety update, or related official update.

It supports MCP tools such as:

```text
search_regulatory_updates
get_regulatory_document_detail
compare_regulatory_updates
generate_regulatory_digest
```

### 4.2 Field Definition

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | string | Yes | Internal stable record ID |
| `agency` | enum | Yes | FDA, EMA, TFDA, NMPA, CDE, or PMDA |
| `region` | string | Yes | US, EU, Taiwan, China, Japan, or other applicable region |
| `title` | string | Yes | Official document or announcement title |
| `original_language` | string | Optional | Original source language |
| `translated_title` | string | Optional | English or Chinese translated title if created by the system |
| `publication_date` | date | Conditional | Official publication date |
| `last_update_date` | date | Optional | Official last updated date |
| `effective_date` | date | Optional | Effective date, if provided |
| `consultation_deadline` | date | Optional | Public comment or consultation deadline, if provided |
| `retrieved_at` | datetime | Yes | Retrieval datetime |
| `official_url` | string | Yes | Official source page URL |
| `attachment_urls` | list[string] | Optional | Official PDF, Word, Excel, or other attachment URLs |
| `source_type` | enum | Yes | API, RSS, open_data, downloadable_file, official_html, parser, or unknown |
| `document_type` | enum | Yes | guidance, regulation, notice, Q&A, news, safety_update, consultation, other, or unknown |
| `document_status` | enum | Yes | draft, final, consultation, updated, withdrawn, unknown |
| `product_modality` | list[enum] | Optional | Standard product modality labels |
| `topics` | list[enum] | Optional | Regulatory topics such as CMC, clinical, GMP, labeling |
| `impact_level` | enum | Optional | low, medium, high, critical, unknown, or requires_manual_review |
| `impacted_functions` | list[string] | Optional | CMC, clinical, QA, RA, PV, manufacturing, nonclinical, etc. |
| `eCTD_module_mapping` | list[string] | Optional | Module 1, Module 2, Module 3, Module 4, Module 5, if applicable |
| `summary` | string | Optional | Short normalized summary |
| `classification_confidence` | enum | Optional | high, medium, low, or requires_manual_review |
| `classification_notes` | string | Optional | Notes explaining product modality, topic, or impact classification |
| `known_limitations` | list[string] | Optional | Missing fields, language issues, parser warnings, or source limitations |
| `content_hash` | string | Optional | Content fingerprint for duplicate detection and change tracking |
| `version_group_id` | string | Optional | Identifier linking draft, final, revised, or withdrawn versions |

### 4.3 Minimal MVP v1 Fields

For MVP v1, every `RegulatoryUpdate` should include at minimum:

```text
id
agency
region
title
publication_date or last_update_date
retrieved_at
official_url
source_type
document_type
document_status
product_modality
topics
summary
known_limitations
```

---

## 5. ClinicalTrialRecord

### 5.1 Purpose

`ClinicalTrialRecord` represents a clinical trial registry record from ClinicalTrials.gov or another approved official registry.

It supports MCP tools such as:

```text
search_clinical_trials_by_indication
compare_companies_by_indication
generate_regulatory_digest
```

### 5.2 Field Definition

| Field | Type | Required | Description |
|---|---|---:|---|
| `trial_id` | string | Yes | Official registry trial ID, such as NCT number |
| `registry` | enum | Yes | ClinicalTrials.gov, TFDA, EU_CTR, CTIS, WHO_ICTRP, or other approved registry |
| `official_url` | string | Yes | Official trial registry URL |
| `title` | string | Yes | Official trial title |
| `brief_summary` | string | Optional | Brief study summary from registry |
| `indications` | list[string] | Conditional | Disease, condition, or indication terms |
| `sponsor` | string | Yes | Official sponsor name |
| `collaborators` | list[string] | Optional | Collaborator names |
| `company_normalized` | string | Optional | Normalized company or sponsor name |
| `intervention_names` | list[string] | Optional | Official intervention names |
| `product_modality` | list[enum] | Optional | Standard product modality labels |
| `phase` | string | Optional | Phase 1, Phase 2, Phase 3, Phase 4, Early Phase 1, Not Applicable, or unknown |
| `status` | string | Optional | Official recruitment or study status |
| `countries` | list[string] | Optional | Countries or regions listed by the registry |
| `start_date` | date | Optional | Official study start date |
| `primary_completion_date` | date | Optional | Official primary completion date |
| `completion_date` | date | Optional | Official completion date |
| `last_update_date` | date | Conditional | Official registry last update date |
| `results_available` | boolean | Optional | Whether trial results are available in the registry |
| `primary_outcomes` | list[string] | Optional | Primary outcome measures |
| `secondary_outcomes` | list[string] | Optional | Secondary outcome measures |
| `enrollment` | integer | Optional | Planned or actual enrollment, if available |
| `study_type` | string | Optional | Interventional, observational, expanded access, etc. |
| `allocation` | string | Optional | Randomized, non-randomized, N/A, unknown |
| `masking` | string | Optional | Open label, double blind, etc. |
| `classification_confidence` | enum | Optional | high, medium, low, or requires_manual_review |
| `classification_notes` | string | Optional | Notes explaining indication, company, or modality classification |
| `known_limitations` | list[string] | Optional | Missing fields, outdated registry records, or classification uncertainty |
| `retrieved_at` | datetime | Yes | Retrieval datetime |
| `content_hash` | string | Optional | Content fingerprint for change detection |

### 5.3 Minimal MVP v1 Fields

For MVP v1, every `ClinicalTrialRecord` should include at minimum:

```text
trial_id
registry
official_url
title
indications
sponsor
intervention_names
product_modality
phase
status
countries
start_date
primary_completion_date
last_update_date
results_available
primary_outcomes
retrieved_at
known_limitations
```

---

## 6. SourceHealthEvent

### 6.1 Purpose

`SourceHealthEvent` represents API failure, RSS failure, parser failure, schema drift, webpage redesign, missing attachment, empty result anomaly, or other source reliability event.

It supports MCP tools such as:

```text
check_source_health
list_source_failures
```

### 6.2 Field Definition

| Field | Type | Required | Description |
|---|---|---:|---|
| `failure_id` | string | Yes | Internal ID for the health event |
| `source_id` | string | Yes | Configured source ID |
| `agency_or_registry` | string | Yes | FDA, TFDA, ClinicalTrials.gov, EMA, NMPA, CDE, PMDA, etc. |
| `source_type` | enum | Yes | API, RSS, open_data, downloadable_file, official_html, parser, unknown |
| `endpoint_url` | string | Yes | API endpoint, RSS URL, webpage URL, or download URL |
| `status` | enum | Yes | open, resolved, monitoring, ignored |
| `failure_type` | enum | Yes | api_status, schema_validation, rss_status, html_selector, attachment_download, empty_result, date_parsing, encoding, data_volume_anomaly, duplicate_anomaly, unknown |
| `severity` | enum | Yes | low, medium, high, critical |
| `detected_at` | datetime | Yes | Datetime the failure was detected |
| `resolved_at` | datetime | Optional | Datetime the failure was resolved |
| `last_successful_check` | datetime | Optional | Last known successful source check |
| `error_message` | string | Optional | Error message or failure description |
| `suspected_cause` | string | Optional | Suspected cause, clearly marked as suspected |
| `suggested_fix` | string | Optional | Suggested next action |
| `suggested_connector_file` | string | Optional | File likely requiring review |
| `github_issue_url` | string | Optional | GitHub Issue URL, if created |
| `known_limitations` | list[string] | Optional | Limitations or uncertainty around the event |

### 6.3 Minimal MVP v1 Fields

For MVP v1, every `SourceHealthEvent` should include at minimum:

```text
failure_id
source_id
agency_or_registry
source_type
endpoint_url
status
failure_type
severity
detected_at
error_message
suggested_fix
```

---

## 7. DigestRecord

### 7.1 Purpose

`DigestRecord` represents a structured input or output record used to generate regulatory or clinical intelligence digests.

It supports:

```text
generate_regulatory_digest
```

### 7.2 Field Definition

| Field | Type | Required | Description |
|---|---|---:|---|
| `digest_id` | string | Yes | Internal digest ID |
| `digest_type` | enum | Yes | regulatory_update, clinical_trial_update, combined |
| `date_range` | string | Yes | 1m, 3m, 6m, 1y, 3y, 5y, or custom |
| `custom_date_range` | object | Optional | start_date and end_date for custom range |
| `generated_at` | datetime | Yes | Datetime digest was generated |
| `sources_searched` | list[string] | Yes | Agencies and registries searched |
| `search_criteria` | object | Yes | Search parameters used |
| `key_regulatory_updates` | list[object] | Optional | Selected RegulatoryUpdate records or summaries |
| `key_clinical_trial_updates` | list[object] | Optional | Selected ClinicalTrialRecord records or summaries |
| `impact_matrix` | list[object] | Optional | Impact assessment items |
| `source_health_summary` | object | Optional | Source health summary |
| `known_limitations` | list[string] | Optional | Known limitations and data gaps |

### 7.3 Minimal MVP v1 Fields

For MVP v1, every `DigestRecord` should include at minimum:

```text
digest_id
digest_type
date_range
generated_at
sources_searched
search_criteria
key_regulatory_updates
key_clinical_trial_updates
source_health_summary
known_limitations
```

---

## 8. Controlled Vocabulary

### 8.1 Agency Values

```text
FDA
EMA
TFDA
NMPA
CDE
PMDA
unknown
```

### 8.2 Registry Values

```text
ClinicalTrials.gov
TFDA
EU_CTR
CTIS
WHO_ICTRP
unknown
```

### 8.3 Source Type Values

```text
API
RSS
open_data
downloadable_file
official_html
parser
manual_import
unknown
```

### 8.4 Document Type Values

```text
guidance
regulation
notice
Q&A
news
safety_update
consultation
procedure
dataset
other
unknown
```

### 8.5 Document Status Values

```text
draft
final
consultation
updated
withdrawn
superseded
unknown
requires_manual_review
```

### 8.6 Regulatory Topic Values

```text
CMC
quality
clinical
nonclinical
GMP
GCP
GLP
pharmacovigilance
labeling
submission
eCTD
manufacturing
inspection
safety
post_approval
general
unknown
requires_manual_review
```

### 8.7 Impact Level Values

```text
low
medium
high
critical
unknown
requires_manual_review
```

### 8.8 Classification Confidence Values

```text
high
medium
low
requires_manual_review
```

### 8.9 Source Health Status Values

```text
open
resolved
monitoring
ignored
```

### 8.10 Source Health Failure Type Values

```text
api_status
schema_validation
rss_status
html_selector
attachment_download
empty_result
date_parsing
encoding
data_volume_anomaly
duplicate_anomaly
unknown
```

---

## 9. Data Quality Rules

### 9.1 Missing Required Fields

If a required field is missing:

1. Preserve the raw record if possible.
2. Mark the missing field as `null`.
3. Add a note to `known_limitations`.
4. Consider creating a `SourceHealthEvent` if the missing field suggests source or parser failure.

### 9.2 Duplicate Records

Potential duplicates should be detected using:

```text
agency / registry
official_url
title
publication_date or last_update_date
content_hash
```

Do not delete potential duplicates without preserving the reason for deduplication.

### 9.3 Low Confidence Classification

When product modality, topic, indication, or impact classification is uncertain:

```text
classification_confidence = low
```

or

```text
classification_confidence = requires_manual_review
```

The system should not convert weak keyword matches into high-confidence classification.

### 9.4 Official Source Priority

Fields extracted from official API or official open data should generally be preferred over fields extracted from HTML parser fallback.

When conflicts occur, preserve the conflict in `known_limitations` or `classification_notes`.

### 9.5 Language and Translation

For non-English sources:

- Preserve the original title.
- Preserve the original language.
- Store translated title separately.
- Do not overwrite official text with machine translation.
- Mark translation uncertainty when relevant.

---

## 10. Relationship to MCP Tools

The data dictionary supports the MCP tool contract as follows:

| MCP Tool | Primary Record Type |
|---|---|
| `search_regulatory_updates` | RegulatoryUpdate |
| `get_regulatory_document_detail` | RegulatoryUpdate |
| `compare_regulatory_updates` | RegulatoryUpdate |
| `search_clinical_trials_by_indication` | ClinicalTrialRecord |
| `compare_companies_by_indication` | ClinicalTrialRecord |
| `check_source_health` | SourceHealthEvent |
| `list_source_failures` | SourceHealthEvent |
| `generate_regulatory_digest` | DigestRecord, RegulatoryUpdate, ClinicalTrialRecord, SourceHealthEvent |

If the MCP tool contract requires a field that is missing from this data dictionary, update this document before implementing the tool.

---

## 11. MVP v1 Field Scope

MVP v1 should avoid overbuilding the data model.

### 11.1 MVP v1 Included Record Types

```text
RegulatoryUpdate
ClinicalTrialRecord
SourceHealthEvent
DigestRecord
```

### 11.2 MVP v1 Included Sources

```text
FDA
TFDA
ClinicalTrials.gov
```

### 11.3 MVP v1 Required Capabilities

MVP v1 data fields should support:

```text
search regulatory updates
retrieve regulatory document detail
search clinical trials by indication
check source health
list source failures
generate a basic digest
```

### 11.4 MVP v1 Exclusions

Do not add source-specific fields for EMA, NMPA, CDE, PMDA, WHO ICTRP, EU CTIS, literature, patents, or commercial intelligence until the relevant project phase is approved.

---

## 12. Maintenance Rule

This document must be updated before:

1. Adding a new normalized record type
2. Adding a new MCP output field
3. Adding a new controlled vocabulary value
4. Renaming an existing field
5. Changing field meaning
6. Adding a new source-specific field
7. Adding multilingual terminology mapping fields
8. Changing MVP v1 required fields

If this document conflicts with `PROJECT_INSTRUCTION.md`, `PROJECT_INSTRUCTION.md` governs project scope.

If this document conflicts with `docs/product_modality_taxonomy.md`, the taxonomy governs product modality labels.

If this document conflicts with `docs/mcp_tool_contract.md`, update both documents before implementation.

---

## 13. Current Build Instruction

For the current build stage, implement only the MVP v1 field scope.

Do not expand the data dictionary into a full database schema before the MVP v1 connector and MCP workflow are stable.

