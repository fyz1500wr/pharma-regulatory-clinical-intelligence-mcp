# Dashboard Query and Filter Contract

Status: Draft contract / docs-spec only  
Last updated: 2026-06-11

## 1. Purpose

This document defines the MVP dashboard query and filter contract that bridges existing MVP runtime tools to future dashboard filtering.

It defines:

- dashboard filter names;
- allowed MVP values;
- runtime tool and parameter mappings;
- display caveats required when rendering query results;
- minimum dashboard row fields for MVP runtime output families.

This contract is intentionally docs/spec-only. It does not implement a dashboard, dashboard renderer, static artifact generator, scheduler, persistence layer, GitHub Actions workflow, HTTP/SSE transport, new MCP tool, new source connector, or source expansion.

## 2. MVP Source Boundary

Active MVP runtime sources remain limited to:

```text
FDA
TFDA
ClinicalTrials.gov
```

The following sources and evidence domains remain future / approval-required and must not be exposed as active dashboard filters until separately approved through the repository governance process:

```text
EMA
NMPA / CDE
PMDA
ICH
EU CTIS
WHO ICTRP
literature
patent
finance
news
```

Dashboard labels may mention future sources only as inactive roadmap context in documentation. Runtime filter controls must not present them as selectable active MVP sources.

## 3. Filter Contract Table

| Filter name | Dashboard label | Allowed MVP values | Runtime tool / parameter mapping | Display caveat |
|---|---|---|---|---|
| `source` | Source | `fda`, `tfda`, `clinicaltrials_gov` | Use as source selection context for `search_regulatory_updates`, `get_regulatory_document_detail`, `compare_regulatory_updates`, `search_clinical_trials_by_indication`, `compare_companies_by_indication`, `check_source_health`, `list_source_failures`, and `generate_regulatory_digest` where supported by the tool contract. | Non-MVP sources must not appear as active values. Source unavailable must be displayed separately from no matching records. |
| `agency` | Agency | `FDA`, `TFDA` | Maps to regulatory update source filters for `search_regulatory_updates`, document lookup context for `get_regulatory_document_detail`, comparison scope for `compare_regulatory_updates`, health checks for `check_source_health`, failure listing for `list_source_failures`, and digest source selection for `generate_regulatory_digest`. | Agency filters are for regulatory/guidance updates only and must not be treated as clinical trial registry filters. |
| `registry` | Registry | `ClinicalTrials.gov` | Maps to registry scope for `search_clinical_trials_by_indication`, `compare_companies_by_indication`, `check_source_health`, `list_source_failures`, and clinical sections of `generate_regulatory_digest`. | ClinicalTrials.gov records are registry-reported records, not regulatory approval evidence. |
| `date_window` | Date window | `7_days`, `30_days`, `90_days`, `6_months`, `1_year`, `custom`, `unknown` | Maps to date range parameters supported by regulatory search, clinical trial search, comparison, source health, failure listing, and digest tools. | Missing or unknown dates must not be treated as negative evidence or as proof that no update exists. |
| `product_modality` | Product modality | `small_molecule`, `peptide`, `oligonucleotide`, `mrna_rna`, `antibody`, `adc`, `recombinant_protein`, `biosimilar`, `vaccine`, `cell_therapy`, `gene_therapy`, `radiopharmaceutical`, `combination_product`, `unknown`, `requires_manual_review` | Maps to product modality filtering or tags for `search_regulatory_updates`, `compare_regulatory_updates`, clinical trial query context where available, and digest grouping. | Classification uncertainty must remain visible. Do not force modality classification from weak keywords. |
| `topic` | Topic | `regulatory_update`, `guidance`, `safety`, `quality`, `cmc`, `clinical`, `labeling`, `inspection`, `source_health`, `other`, `unknown` | Maps to keyword/topic parameters for regulatory search, comparison, document detail context, source-health grouping, and digest sections. | Topic tags are search/display aids and are not final regulatory interpretations. |
| `indication` | Indication / condition | Free-text user query; normalized display value may be `unknown` when absent. | Maps to `indication` or condition query parameters for `search_clinical_trials_by_indication`, `compare_companies_by_indication`, and clinical sections of `generate_regulatory_digest`. | Indication values may be registry-reported condition terms and should not be reinterpreted as approved indications. |
| `company_or_sponsor` | Company or sponsor | Free-text user query; registry-reported sponsor names; `unknown` when absent. | Maps to sponsor/company query parameters for `search_clinical_trials_by_indication`, `compare_companies_by_indication`, and digest grouping where supported. | Sponsor/company names are registry-reported only. Do not infer aliases, corporate families, ownership, or product control. |
| `trial_phase` | Trial phase | `early_phase_1`, `phase_1`, `phase_1_phase_2`, `phase_2`, `phase_2_phase_3`, `phase_3`, `phase_4`, `not_applicable`, `unknown` | Maps to phase filters for `search_clinical_trials_by_indication` and comparison grouping for `compare_companies_by_indication`. | Trial phase is not evidence of clinical success, approval probability, or commercial strength. |
| `trial_status` | Trial status | `not_yet_recruiting`, `recruiting`, `enrolling_by_invitation`, `active_not_recruiting`, `suspended`, `terminated`, `withdrawn`, `completed`, `unknown` | Maps to recruitment/status filters for `search_clinical_trials_by_indication` and clinical comparison/digest grouping. | Status must be displayed as registry-reported and may lag real-world changes. |
| `results_available` | Results available | `true`, `false`, `unknown` | Maps to results availability extraction from `search_clinical_trials_by_indication` and comparison/digest output grouping. | Missing posted results are not evidence that a study failed or succeeded. |
| `source_health_status` | Source health status | `pass`, `warning`, `failed`, `source_unavailable`, `partial_results`, `unknown` | Maps to `check_source_health`, `list_source_failures`, warnings returned by search/detail/compare tools, and digest source coverage summaries. | `source_unavailable` and `partial_results` must be displayed distinctly from `no_matching_records`. |
| `human_review_required` | Human review required | `true`, `false` | Maps to normalized record caveats and digest/review flags returned by runtime tools. Default to `true` for regulatory and clinical intelligence outputs when uncertainty exists. | A false value does not make the output final advice; human verification remains required before regulatory, clinical, legal, or management-facing use. |

## 4. Runtime Tool Mapping

| MCP tool | Dashboard use | Filter inputs / context | Required display behavior |
|---|---|---|---|
| `search_regulatory_updates` | Populate Regulatory / Guidance Updates rows. | `source`, `agency`, `date_window`, `product_modality`, `topic`, and query keywords where supported. | Show source, date evidence, official URL, partial-result warnings, and source-health caveats. |
| `get_regulatory_document_detail` | Open detail view for a selected regulatory/guidance row. | Selected document identifier, `source`, `agency`, and official URL context. | Preserve official source links and display missing attachments or unavailable detail as source limitations. |
| `compare_regulatory_updates` | Compare regulatory/guidance rows across active MVP agencies or topics. | `source`, `agency`, `date_window`, `product_modality`, and `topic`. | Do not imply regulatory equivalence where source metadata is incomplete or unavailable. |
| `search_clinical_trials_by_indication` | Populate Clinical Trial Tracker rows. | `registry`, `indication`, `company_or_sponsor`, `trial_phase`, `trial_status`, `results_available`, and `date_window` where supported. | Display registry-reported fields only and avoid success, approval, ownership, alias, or corporate-family inference. |
| `compare_companies_by_indication` | Group ClinicalTrials.gov records by registry-reported sponsor/company within an indication. | `registry`, `indication`, `company_or_sponsor`, `trial_phase`, `trial_status`, and `results_available`. | Comparison is descriptive only and must not rank clinical success, commercial strength, or company superiority. |
| `check_source_health` | Populate Source Health rows and source-health badges on other dashboard rows. | `source`, `agency`, `registry`, `date_window`, and `source_health_status`. | Show failures, schema drift, empty-result anomalies, and unavailable-source states explicitly. |
| `list_source_failures` | Populate Source Health failure detail rows and troubleshooting views. | `source`, `agency`, `registry`, `date_window`, and `source_health_status`. | Preserve failure type and timestamp. Do not collapse source failures into no-result messaging. |
| `generate_regulatory_digest` | Populate Digest Summary rows and dashboard digest sections. | `source`, `agency`, `registry`, `date_window`, `product_modality`, `topic`, `indication`, and sponsor/company context where supported. | Include source coverage, partial-result warnings, human-review flags, and source limitations in the digest display. |

## 5. Display Rules

Future dashboard surfaces that use this contract must preserve the following rules:

1. `source_unavailable` is not the same as `no_matching_records`.
2. Missing metadata is not negative evidence.
3. Sponsor and company names are registry-reported only.
4. Clinical trial rows must not infer clinical success.
5. Regulatory or clinical rows must not include approval probability scoring.
6. Dashboard rows must not include commercial strength ranking.
7. Dashboard rows must not infer product ownership.
8. Dashboard rows must not infer corporate-family relationships or company aliases.
9. Non-MVP sources must remain inactive unless a later approved change updates the source boundary and runtime implementation.
10. Human review remains required for regulatory, clinical, legal, medical, or management-facing use.

## 6. Dashboard Row Mapping

### 6.1 Regulatory / Guidance Updates

Minimum row fields:

```text
record_id
source
agency
title
document_type
publication_date
last_update_date
official_url
product_modality
topic
query_context
source_health_status
result_state
human_review_required
display_caveats
```

`result_state` should distinguish at least:

```text
matching_record
no_matching_records
source_unavailable
partial_results
metadata_missing
unknown
```

### 6.2 Clinical Trial Tracker

Minimum row fields:

```text
record_id
registry
registry_id
brief_title
condition_or_indication
sponsor_or_collaborator
intervention_name
trial_phase
trial_status
start_date
primary_completion_date
completion_date
last_update_posted
results_available
registry_url
query_context
source_health_status
result_state
human_review_required
display_caveats
```

Clinical trial rows must not contain fields for:

```text
approval_probability
clinical_success_score
commercial_strength_score
product_ownership
company_alias
corporate_family
```

### 6.3 Source Health

Minimum row fields:

```text
record_id
source
source_type
status
failure_type
failure_message
first_observed_at
last_observed_at
last_success_at
http_status
schema_drift_detected
empty_result_anomaly
record_count_anomaly
recommended_action
human_review_required
```

### 6.4 Digest Summary

Minimum row fields:

```text
digest_id
date_window
included_sources
excluded_or_unavailable_sources
regulatory_update_count
clinical_trial_count
source_failure_count
key_topics
product_modalities
indications
source_coverage_summary
partial_result_warnings
human_review_required
display_caveats
```

## 7. Acceptance Criteria

The contract is acceptable only if all of the following statements remain true:

1. Non-MVP sources must not appear as active filters.
2. FDA, TFDA, and ClinicalTrials.gov are the only active MVP sources.
3. `source_unavailable` must be displayed distinctly from `no_matching_records`.
4. Clinical trial dashboard rows must not contain approval probability, clinical success, commercial strength, product ownership, alias, or corporate-family fields.
5. The contract remains docs/spec-only.
6. The contract does not add a dashboard renderer, static artifact generator, scheduler, persistence layer, GitHub Actions workflow, HTTP/SSE transport, new MCP tool, new source connector, or source expansion.
7. Sponsor/company filters and displays remain based on registry-reported names only.
8. Missing metadata must be displayed as uncertainty or limitation, not negative evidence.
