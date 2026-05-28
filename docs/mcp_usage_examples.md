# MCP Usage Examples

## Purpose

This document provides practical MVP v1 usage examples for the MCP tools in this repository.

It is intended for Claude Project, Codex, MCP clients, and future maintainers who need to call the tools safely and interpret their outputs conservatively.

This document is not a final regulatory, clinical, legal, or medical assessment procedure. Tool outputs should be treated as source-grounded working intelligence that requires human review before use in decisions.

---

## MVP v1 Active Scope

MVP v1 active sources are intentionally limited to:

- FDA
- TFDA
- ClinicalTrials.gov

The following are out of scope unless approved in a later phase:

- EMA
- NMPA / CDE
- PMDA
- WHO ICTRP
- EU CTIS
- Literature
- Patents
- Finance data
- Commercial intelligence
- Database persistence
- Scheduler
- Alerting
- Automated GitHub issue creation
- Advanced report generation

---

## General Usage Rules

Before using any output, inspect:

- `query_metadata`
- `known_limitations`
- `official_url` when available
- source health status if the output may depend on live sources

Do not infer:

- Clinical success
- Regulatory approval probability
- Commercial strength
- Company superiority
- Final agency equivalence
- Final regulatory requirement mapping

A source health `pass` means the current connector check passed. It does not prove the source data is complete.

A source failure result in MVP v1 is a current health snapshot. It is not a historical failure trend database.

---

## Tool: `search_regulatory_updates`

### When to use

Use this tool to search FDA and/or TFDA regulatory update records.

Use it before document detail lookup, comparison, or digest generation when the user asks about recent or topic-specific regulatory updates.

### Example input

```json
{
  "agency": "FDA",
  "query": "quality",
  "limit": 10
}
```

### Expected output shape

```text
records[]
query_metadata
known_limitations
```

Important record fields:

```text
records[].id
records[].title
records[].agency
records[].publication_date
records[].document_type
records[].document_status
records[].topics
records[].product_modality
records[].official_url
records[].summary
records[].known_limitations
```

### Fields to inspect

- `records[].official_url`
- `records[].publication_date`
- `records[].topics`
- `records[].document_status`
- `query_metadata.filters_applied`
- `known_limitations`

### Do not infer

Do not treat search results as a complete regulatory universe.

Do not conclude that the absence of a TFDA result means Taiwan has no relevant requirement.

Do not conclude that an FDA update automatically applies to TFDA or another agency.

### Practical next action

For an important record, call `get_regulatory_document_detail` using the record `id` and agency.

---

## Tool: `get_regulatory_document_detail`

### When to use

Use this tool after `search_regulatory_updates` when a specific regulatory record needs more structured detail.

MVP v1 detail is metadata-backed. It reconstructs detail from normalized search metadata and does not parse full document bodies or attachments.

### Example input

```json
{
  "document_id": "fda-example-id",
  "agency": "FDA"
}
```

### Expected output shape

```text
document
query_metadata
```

Important fields:

```text
document.id
document.title
document.agency
document.official_url
document.document_type
document.document_status
document.impact_assessment
document.known_limitations
query_metadata.lookup_mode
query_metadata.known_limitations
```

### Fields to inspect

- `document.official_url`
- `document.known_limitations`
- `document.impact_assessment.rationale`
- `query_metadata.lookup_mode`

### Do not infer

Do not treat metadata-backed detail as full-text document review.

Do not treat `impact_assessment` as a final CMC, regulatory, legal, or compliance conclusion.

### Practical next action

Use the official URL for manual verification before making any regulatory or CMC decision.

---

## Tool: `compare_regulatory_updates`

### When to use

Use this tool to compare FDA and TFDA regulatory update records by agency, topic, product modality, or document status.

### Example input

```json
{
  "agencies": ["FDA", "TFDA"],
  "comparison_axis": "agency",
  "query": "quality"
}
```

### Expected output shape

```text
comparison[]
comparison_summary
query_metadata
```

Important fields:

```text
comparison[].comparison_axis
comparison[].comparison_value
comparison[].record_count
comparison[].key_updates
comparison[].common_themes
comparison[].known_limitations
comparison_summary.overall_themes
comparison_summary.major_differences
comparison_summary.recommended_follow_up
query_metadata.known_limitations
```

### Fields to inspect

- `comparison[].key_updates[].official_url`
- `comparison_summary.recommended_follow_up`
- `query_metadata.partial_lookup_failures`
- `query_metadata.known_limitations`

### Do not infer

Do not treat the comparison as final agency equivalence.

Do not treat a missing agency result as proof that no relevant requirement exists.

Do not treat descriptive differences as final regulatory requirement mapping.

### Practical next action

For important differences, call `get_regulatory_document_detail` for each key update and perform manual review.

---

## Tool: `search_clinical_trials_by_indication`

### When to use

Use this tool to search ClinicalTrials.gov trial records for a specific indication.

Use sponsor filtering when the user is interested in one company or sponsor name.

### Example input

```json
{
  "indication": "NSCLC",
  "sponsor": "Acme Pharma",
  "page_size": 10
}
```

### Expected output shape

```text
trials[]
query_metadata
```

Important fields:

```text
trials[].trial_id
trials[].title
trials[].sponsor
trials[].phase
trials[].status
trials[].indications
trials[].intervention_names
trials[].product_modality
trials[].official_url
trials[].results_available
trials[].known_limitations
query_metadata.registries_searched
query_metadata.known_limitations
```

### Fields to inspect

- `trials[].official_url`
- `trials[].phase`
- `trials[].status`
- `trials[].sponsor`
- `trials[].known_limitations`
- `query_metadata.known_limitations`

### Do not infer

Do not treat trial phase as approval probability.

Do not treat recruiting, active, completed, terminated, or withdrawn status as clinical success or failure.

Do not treat ClinicalTrials.gov activity as complete global clinical activity.

### Practical next action

Use the official trial URL for manual verification. For multi-company comparison, call `compare_companies_by_indication`.

---

## Tool: `compare_companies_by_indication`

### When to use

Use this tool to compare sponsor-name-based ClinicalTrials.gov trial activity across companies for a specific indication.

This is a trial activity comparison only. It is not a competitive superiority, clinical success, approval probability, or commercial strength assessment.

### Example input

```json
{
  "indication": "NSCLC",
  "companies": ["Acme Pharma", "Beta Bio"],
  "registries": ["ClinicalTrials.gov"],
  "date_range": "3y",
  "page_size": 10
}
```

### Expected output shape

```text
company_comparison[]
landscape_summary
query_metadata
```

Important fields:

```text
company_comparison[].company
company_comparison[].trial_count
company_comparison[].active_trial_count
company_comparison[].completed_trial_count
company_comparison[].highest_phase
company_comparison[].phase_distribution
company_comparison[].status_distribution
company_comparison[].key_trials
company_comparison[].known_limitations
landscape_summary.data_gaps
query_metadata.lookup_mode
query_metadata.date_range_filter_applied
query_metadata.known_limitations
```

### Fields to inspect

- `company_comparison[].key_trials[].official_url`
- `company_comparison[].phase_distribution`
- `company_comparison[].status_distribution`
- `landscape_summary.data_gaps`
- `query_metadata.date_range_filter_applied`

### Do not infer

Do not infer company superiority.

Do not infer clinical success.

Do not infer regulatory approval probability.

Do not infer commercial strength.

Do not infer corporate family relationships from sponsor-name matching.

### MVP v1 date range limitation

`date_range` is recorded in query metadata only. Date-based trial filtering is not applied in MVP v1.

### Practical next action

Use this output to frame a conservative landscape summary. For decisions, manually verify key trials and sponsors.

---

## Tool: `check_source_health`

### When to use

Use this tool to check whether MVP v1 sources are currently reachable or degraded.

### Example input

```json
{
  "sources": ["FDA_openFDA", "TFDA_DataAction", "ClinicalTrialsGov_API"]
}
```

### Expected output shape

```text
overall_status
source_health[]
sources[]
query_metadata
known_limitations
```

Important fields:

```text
source_health[].source_id
source_health[].status
source_health[].severity
source_health[].failure_type
source_health[].error_message
source_health[].suggested_fix
source_health[].suggested_connector_file
query_metadata.sources_checked
query_metadata.known_limitations
```

### Fields to inspect

- `overall_status`
- `source_health[].status`
- `source_health[].severity`
- `source_health[].suggested_fix`
- `query_metadata.sources_checked`

### Do not infer

Do not treat a `pass` status as proof of complete data coverage.

Do not treat a degraded source as proof that all related outputs are invalid. Instead, lower confidence and inspect source-specific failures.

### Practical next action

If a source is degraded or failed, call `list_source_failures` and downgrade confidence in any dependent digest or comparison.

---

## Tool: `list_source_failures`

### When to use

Use this tool to convert current source health results into structured failure records.

This is useful for debugging, operational review, and deciding whether output confidence should be downgraded.

### Example input

```json
{
  "sources": ["FDA_openFDA", "TFDA_DataAction", "ClinicalTrialsGov_API"]
}
```

### Expected output shape

```text
failures[]
summary
query_metadata
```

Important fields:

```text
failures[].failure_id
failures[].source_id
failures[].agency_or_registry
failures[].failure_type
failures[].severity
failures[].status
failures[].error_message
failures[].suggested_fix
summary.open_failure_count
summary.high_failure_count
summary.critical_failure_count
query_metadata.lookup_mode
query_metadata.known_limitations
```

### Fields to inspect

- `summary.open_failure_count`
- `summary.high_failure_count`
- `summary.critical_failure_count`
- `failures[].suggested_fix`
- `query_metadata.lookup_mode`

### Do not infer

Do not treat this as a historical source failure database.

Do not use `date_range` as if it queries historical failure trends in MVP v1.

### Practical next action

If open failures exist, include them in the final user-facing caveats and lower confidence in affected outputs.

---

## Tool: `generate_regulatory_digest`

### When to use

Use this tool to generate a rule-based MVP v1 digest that combines regulatory search, clinical trial search, source health, and source failure outputs.

Use it for weekly summaries, management-style briefings, or quick regulatory-clinical intelligence snapshots.

### Example input

```json
{
  "digest_type": "combined",
  "date_range": "1m",
  "agencies": ["FDA"],
  "registries": ["ClinicalTrials.gov"],
  "indications": ["NSCLC"],
  "companies": ["Acme Pharma"],
  "limit": 10,
  "include_impact_matrix": true,
  "include_source_health_summary": true
}
```

### Expected output shape

```text
digest
query_metadata
```

Important fields:

```text
digest.title
digest.date_range
digest.generated_at
digest.sources_searched
digest.search_criteria
digest.executive_summary
digest.key_regulatory_updates
digest.key_clinical_trial_updates
digest.impact_matrix
digest.source_health_summary
digest.known_limitations
query_metadata.lookup_mode
query_metadata.source_errors
query_metadata.known_limitations
```

### Fields to inspect

- `digest.executive_summary`
- `digest.search_criteria`
- `digest.source_health_summary`
- `digest.known_limitations`
- `query_metadata.source_errors`

### Do not infer

Do not treat digest output as a final regulatory assessment.

Do not treat digest output as a final clinical assessment.

Do not treat the impact matrix as validated cross-functional impact mapping.

### Practical next action

Use the digest as a structured first draft. Verify key regulatory updates and key clinical trials manually before executive reporting.

---

## Recommended Workflows

### Regulatory update workflow

1. `search_regulatory_updates`
2. `get_regulatory_document_detail`
3. `compare_regulatory_updates` if multiple agencies or topics are involved
4. `generate_regulatory_digest` for summary output

### Clinical trial landscape workflow

1. `search_clinical_trials_by_indication`
2. `compare_companies_by_indication` when multiple companies are involved
3. `generate_regulatory_digest` for combined regulatory-clinical summary

### Source reliability workflow

1. `check_source_health`
2. `list_source_failures`
3. Downgrade confidence if sources are degraded or failures are open
4. Include source caveats in the final response

---

## Bad Usage Examples and Safer Alternatives

### Bad company comparison inference

Bad:

```text
Company A has more Phase 3 trials than Company B, therefore Company A is clinically superior.
```

Safer:

```text
Company A has more ClinicalTrials.gov Phase 3 trial activity in this query result. This does not establish clinical superiority, approval probability, or commercial strength.
```

### Bad regulatory absence inference

Bad:

```text
No TFDA result was found, therefore Taiwan has no relevant requirement.
```

Safer:

```text
No TFDA result was found in this MVP v1 query. Manual verification is needed before concluding that no relevant Taiwan requirement exists.
```

### Bad source health inference

Bad:

```text
Source health passed, therefore the dataset is complete.
```

Safer:

```text
Source health passed for the current connector check. This does not prove the dataset is complete.
```

### Bad digest inference

Bad:

```text
The digest says the impact is low, so no action is needed.
```

Safer:

```text
The MVP digest is a rule-based first-pass aggregation. Impact and follow-up actions require manual review.
```
