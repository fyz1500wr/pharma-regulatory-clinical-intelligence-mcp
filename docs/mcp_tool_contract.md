# MCP Tool Contract

## 1. Purpose

This document defines the stable MCP tool contract for the Pharmaceutical Regulatory and Clinical Intelligence System.

It specifies the intended Claude-facing tools, their purpose, core input parameters, expected output fields, and usage restrictions.

This file is a **tool interface governance document**. It is not implementation code, a database schema, a parser specification, or a Claude prompt library.

The MCP layer should allow Claude to query normalized and source-governed data without directly scraping raw agency websites.

---

## 2. Design Principles

### 2.1 Stable Tool Names

MCP tool names should remain stable once implemented.

Do not rename tools casually. If a tool must be renamed, provide a migration note and update all related documentation.

### 2.2 Claude Queries Processed Data

Claude should query processed, normalized, and source-traceable data through MCP tools.

Claude should not directly scrape FDA, EMA, TFDA, NMPA, PMDA, ClinicalTrials.gov, or other raw sources during normal project execution.

### 2.3 Source Traceability Required

Every MCP response should preserve source traceability.

At minimum, responses should include:

- Source agency or registry
- Official title
- Publication date or last update date
- Official source URL
- Retrieval date, where available
- Source type, such as API, RSS, open data, downloadable file, or HTML parser
- Known limitations, if applicable

### 2.4 Conservative Classification

Product modality, topic, indication, and impact classification must be conservative.

If confidence is insufficient, the tool response should use:

```text
unknown
```

or

```text
requires_manual_review
```

rather than forcing a classification.

### 2.5 Current Phase Control

MVP v1 tools should support only the approved MVP v1 source scope:

```text
FDA
TFDA
ClinicalTrials.gov
```

EMA, NMPA / CDE, PMDA, WHO ICTRP, EU CTIS, literature, patent, and commercial intelligence sources should not be exposed as active production sources until explicitly approved for a later phase.

---

## 3. Shared Parameter Conventions

### 3.1 Date Range

All date-range-aware tools should support:

```text
1m
3m
6m
1y
3y
5y
custom
```

For `custom`, tools should accept:

```json
{
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD"
}
```

Date filtering should use the most appropriate official date field:

1. Publication date
2. Last update date
3. Registry update date
4. Retrieval date only when no official date is available

### 3.2 Agencies

Approved agency values:

```text
FDA
EMA
TFDA
NMPA
CDE
PMDA
```

MVP v1 active agency values:

```text
FDA
TFDA
```

### 3.3 Registries

Approved registry values:

```text
ClinicalTrials.gov
TFDA
EU_CTR
CTIS
WHO_ICTRP
```

MVP v1 active registry values:

```text
ClinicalTrials.gov
TFDA
```

### 3.4 Product Modality

MCP tools should use:

```text
product_modality
```

Do not use:

```text
biologic_type
```

Approved top-level product modality labels are defined in:

```text
docs/product_modality_taxonomy.md
```

MVP v1 supported labels:

```text
small_molecule
peptide
oligonucleotide
mrna_rna
antibody
adc
recombinant_protein
biosimilar
vaccine
cell_therapy
gene_therapy
radiopharmaceutical
combination_product
unknown
requires_manual_review
```

### 3.5 Regulatory Topics

Recommended topic labels:

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

### 3.6 Impact Level

Recommended impact levels:

```text
low
medium
high
critical
unknown
requires_manual_review
```

### 3.7 Classification Confidence

Recommended confidence values:

```text
high
medium
low
requires_manual_review
```

---

## 4. Tool Inventory

MVP v1 should define the following MCP tools:

```text
search_regulatory_updates
get_regulatory_document_detail
compare_regulatory_updates
search_clinical_trials_by_indication
compare_companies_by_indication
check_source_health
list_source_failures
generate_regulatory_digest
```

Do not add new MCP tools unless the need cannot be met by these core tools.

---

## 5. Tool Contract: search_regulatory_updates

### 5.1 Purpose

Search normalized regulatory updates by agency, date range, product modality, regulatory topic, document status, and keyword.

### 5.2 Intended Claude Use

Claude may use this tool to answer questions such as:

- What FDA and TFDA regulatory updates were published in the last 6 months?
- Are there recent updates related to ADC, peptide, or oligonucleotide products?
- Which recent guidance documents may affect CMC or clinical strategy?

### 5.3 Input Parameters

```json
{
  "agencies": ["FDA", "TFDA"],
  "date_range": "6m",
  "custom_date_range": {
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  },
  "product_modality": ["antibody", "adc", "peptide"],
  "topics": ["CMC", "clinical", "quality"],
  "document_status": ["draft", "final", "consultation", "updated", "unknown"],
  "keywords": ["biosimilar", "comparability"],
  "limit": 50
}
```

### 5.3.1 MVP v0.2.0 Implementation Note

`search_regulatory_updates` supports `product_modality` filtering for active MVP sources FDA and TFDA.

The filter uses normalized `product_modality` values and approved labels from `docs/product_modality_taxonomy.md`. Classification remains conservative and may require manual verification. A no-result response after product modality filtering must not be interpreted as evidence that no regulatory activity exists outside the stated query scope.

### 5.4 Required Output Fields

```json
{
  "records": [
    {
      "id": "string",
      "agency": "FDA",
      "title": "string",
      "publication_date": "YYYY-MM-DD",
      "last_update_date": "YYYY-MM-DD",
      "document_status": "draft | final | consultation | updated | unknown",
      "document_type": "guidance | regulation | notice | Q&A | news | safety_update | other",
      "product_modality": ["antibody"],
      "topics": ["CMC"],
      "impact_level": "low | medium | high | critical | unknown",
      "summary": "string",
      "official_url": "string",
      "attachment_urls": ["string"],
      "source_type": "API | RSS | open_data | downloadable_file | official_html | parser",
      "retrieved_at": "datetime",
      "classification_confidence": "high | medium | low | requires_manual_review"
    }
  ],
  "query_metadata": {
    "date_range": "6m",
    "sources_searched": ["FDA", "TFDA"],
    "known_limitations": ["string"]
  }
}
```

### 5.5 Restrictions

- Do not return non-official sources as primary evidence.
- Do not infer product modality if confidence is low.
- Do not confuse retrieval date with publication date.
- Do not silently include out-of-phase sources.

---

## 6. Tool Contract: get_regulatory_document_detail

### 6.1 Purpose

Retrieve detailed information for a single regulatory update or document.

### 6.2 Intended Claude Use

Claude may use this tool after `search_regulatory_updates` to inspect a specific document in more detail.

### 6.3 Input Parameters

```json
{
  "document_id": "string",
  "include_attachments": true,
  "include_classification_notes": true
}
```

### 6.4 Required Output Fields

```json
{
  "document": {
    "id": "string",
    "agency": "FDA",
    "title": "string",
    "original_language": "string",
    "translated_title": "string",
    "publication_date": "YYYY-MM-DD",
    "last_update_date": "YYYY-MM-DD",
    "effective_date": "YYYY-MM-DD",
    "consultation_deadline": "YYYY-MM-DD",
    "document_type": "guidance | regulation | notice | Q&A | news | safety_update | other",
    "document_status": "draft | final | consultation | updated | withdrawn | unknown",
    "official_url": "string",
    "attachment_urls": ["string"],
    "source_type": "API | RSS | open_data | downloadable_file | official_html | parser",
    "retrieved_at": "datetime",
    "content_hash": "string",
    "product_modality": ["antibody", "adc"],
    "topics": ["CMC", "quality"],
    "summary": "string",
    "impact_assessment": {
      "impact_level": "low | medium | high | critical | unknown",
      "impacted_functions": ["CMC", "clinical", "QA", "RA"],
      "eCTD_module_mapping": ["Module 2", "Module 3"],
      "rationale": "string"
    },
    "classification_notes": "string",
    "known_limitations": ["string"]
  }
}
```

### 6.5 Restrictions

- Do not generate legal or regulatory advice as a final decision.
- Do not invent missing dates, titles, or source links.
- If detail is unavailable, return a clear limitation.

---

## 7. Tool Contract: compare_regulatory_updates

### 7.1 Purpose

Compare regulatory updates across agencies, topics, product modalities, or date ranges.

### 7.2 Intended Claude Use

Claude may use this tool to generate cross-agency comparison tables or impact summaries.

### 7.3 Input Parameters

```json
{
  "agencies": ["FDA", "EMA", "TFDA"],
  "date_range": "1y",
  "product_modality": ["biosimilar", "adc"],
  "topics": ["CMC", "clinical"],
  "comparison_axis": "agency | topic | product_modality | document_status",
  "include_impact_assessment": true
}
```

### 7.4 Required Output Fields

```json
{
  "comparison": [
    {
      "agency": "FDA",
      "record_count": 5,
      "key_updates": [
        {
          "id": "string",
          "title": "string",
          "publication_date": "YYYY-MM-DD",
          "official_url": "string",
          "impact_level": "medium",
          "summary": "string"
        }
      ],
      "common_themes": ["string"],
      "agency_specific_notes": ["string"],
      "known_limitations": ["string"]
    }
  ],
  "comparison_summary": {
    "overall_themes": ["string"],
    "major_differences": ["string"],
    "recommended_follow_up": ["string"]
  }
}
```

### 7.5 Restrictions

- Do not claim two agencies have identical requirements unless explicitly supported.
- Clearly distinguish document status, such as draft versus final.
- Clearly identify gaps when one agency has no relevant updates.

---

## 8. Tool Contract: search_clinical_trials_by_indication

### 8.1 Purpose

Search clinical trials by indication, company, product modality, phase, trial status, region, and date range.

### 8.2 Intended Claude Use

Claude may use this tool to track competitor clinical development by disease area.

### 8.3 Input Parameters

```json
{
  "indication": "NSCLC",
  "companies": ["Roche", "Merck", "BMS"],
  "registries": ["ClinicalTrials.gov"],
  "date_range": "1y",
  "product_modality": ["antibody", "adc", "small_molecule"],
  "phase": ["Phase 1", "Phase 2", "Phase 3"],
  "status": ["Recruiting", "Active, not recruiting", "Completed"],
  "countries": ["United States", "Taiwan"],
  "include_results": true,
  "limit": 100
}
```

### 8.4 Required Output Fields

```json
{
  "trials": [
    {
      "trial_id": "NCT00000000",
      "registry": "ClinicalTrials.gov",
      "official_url": "string",
      "title": "string",
      "indications": ["NSCLC"],
      "sponsor": "string",
      "collaborators": ["string"],
      "company_normalized": "string",
      "intervention_names": ["string"],
      "product_modality": ["antibody"],
      "phase": "Phase 2",
      "status": "Recruiting",
      "countries": ["United States"],
      "start_date": "YYYY-MM-DD",
      "primary_completion_date": "YYYY-MM-DD",
      "completion_date": "YYYY-MM-DD",
      "last_update_date": "YYYY-MM-DD",
      "results_available": false,
      "primary_outcomes": ["string"],
      "brief_summary": "string",
      "classification_confidence": "high | medium | low | requires_manual_review",
      "known_limitations": ["string"]
    }
  ],
  "query_metadata": {
    "indication": "NSCLC",
    "date_range": "1y",
    "registries_searched": ["ClinicalTrials.gov"],
    "known_limitations": ["string"]
  }
}
```

### 8.5 Restrictions

- Do not infer clinical success from trial existence.
- Do not equate trial status with regulatory approval probability.
- Do not merge company names without preserving original sponsor names.
- Do not use non-official trial databases as primary evidence during MVP v1.

---

## 9. Tool Contract: compare_companies_by_indication

### 9.1 Purpose

Compare company clinical trial activity within a specific indication.

### 9.2 Intended Claude Use

Claude may use this tool to generate competitor trial landscape summaries.

### 9.3 Input Parameters

```json
{
  "indication": "NSCLC",
  "companies": ["Roche", "Merck", "BMS", "AstraZeneca"],
  "registries": ["ClinicalTrials.gov"],
  "date_range": "3y",
  "product_modality": ["antibody", "adc", "small_molecule"],
  "phase": ["Phase 1", "Phase 2", "Phase 3"],
  "include_completed_trials": true,
  "include_results": true
}
```

### 9.4 Required Output Fields

```json
{
  "company_comparison": [
    {
      "company": "Roche",
      "trial_count": 10,
      "active_trial_count": 6,
      "completed_trial_count": 4,
      "modalities": ["antibody", "adc"],
      "highest_phase": "Phase 3",
      "key_trials": [
        {
          "trial_id": "NCT00000000",
          "title": "string",
          "phase": "Phase 3",
          "status": "Recruiting",
          "intervention_names": ["string"],
          "last_update_date": "YYYY-MM-DD",
          "official_url": "string",
          "results_available": false
        }
      ],
      "summary": "string",
      "known_limitations": ["string"]
    }
  ],
  "landscape_summary": {
    "indication": "NSCLC",
    "companies_compared": ["Roche", "Merck", "BMS", "AstraZeneca"],
    "overall_trends": ["string"],
    "data_gaps": ["string"]
  }
}
```

### 9.5 Restrictions

- Do not rank companies by superiority unless evidence supports it.
- Do not treat all trials as comparable without considering phase, status, endpoints, and population.
- Clearly mark data gaps.

---

## 10. Tool Contract: check_source_health

### 10.1 Purpose

Check the current health status of configured data sources.

### 10.2 Intended Claude Use

Claude may use this tool to explain whether a source, connector, API, RSS feed, or parser appears healthy.

### 10.3 Input Parameters

```json
{
  "sources": ["FDA_openFDA", "TFDA_DataAction", "ClinicalTrialsGov_API"],
  "include_recent_failures": true,
  "include_suggested_fix": true
}
```

### 10.4 Required Output Fields

```json
{
  "source_health": [
    {
      "source_id": "FDA_openFDA",
      "agency_or_registry": "FDA",
      "source_type": "API",
      "endpoint_url": "string",
      "status": "pass | warning | failed | unknown",
      "last_successful_check": "datetime",
      "last_checked_at": "datetime",
      "failure_type": "api_status | schema_validation | rss_status | html_selector | attachment_download | empty_result | unknown",
      "error_message": "string",
      "suggested_fix": "string",
      "suggested_connector_file": "string",
      "severity": "low | medium | high | critical"
    }
  ]
}
```

### 10.5 Restrictions

- Do not hide source failures.
- Do not report a source as healthy if only part of the check succeeded.
- Clearly distinguish warnings from failures.

---

## 11. Tool Contract: list_source_failures

### 11.1 Purpose

List recent source failures, parser failures, schema drift events, or webpage change alerts.

### 11.2 Intended Claude Use

Claude may use this tool to support maintenance planning or Codex debugging.

### 11.3 Input Parameters

```json
{
  "date_range": "1m",
  "agencies_or_registries": ["FDA", "TFDA", "ClinicalTrials.gov"],
  "failure_types": ["schema_validation", "html_selector", "api_status"],
  "severity": ["medium", "high", "critical"],
  "include_resolved": false
}
```

### 11.4 Required Output Fields

```json
{
  "failures": [
    {
      "failure_id": "string",
      "source_id": "string",
      "agency_or_registry": "FDA",
      "detected_at": "datetime",
      "resolved_at": "datetime",
      "status": "open | resolved | monitoring",
      "failure_type": "api_status | schema_validation | rss_status | html_selector | attachment_download | empty_result | unknown",
      "severity": "low | medium | high | critical",
      "error_message": "string",
      "suspected_cause": "string",
      "suggested_fix": "string",
      "suggested_connector_file": "string",
      "github_issue_url": "string"
    }
  ],
  "summary": {
    "open_failure_count": 0,
    "critical_failure_count": 0,
    "known_limitations": ["string"]
  }
}
```

### 11.5 Restrictions

- Do not mark a failure as resolved unless a successful check confirms it.
- Do not create speculative causes without marking them as suspected.

---

## 12. Tool Contract: generate_regulatory_digest

### 12.1 Purpose

Generate a structured regulatory or clinical intelligence digest from normalized records.

### 12.2 Intended Claude Use

Claude may use this tool to produce weekly, monthly, or custom reports based on approved sources.

### 12.3 Input Parameters

```json
{
  "digest_type": "regulatory_update | clinical_trial_update | combined",
  "date_range": "1m",
  "agencies": ["FDA", "TFDA"],
  "registries": ["ClinicalTrials.gov"],
  "product_modality": ["antibody", "adc", "peptide"],
  "topics": ["CMC", "clinical", "quality"],
  "indications": ["NSCLC"],
  "companies": ["Roche", "Merck"],
  "include_impact_matrix": true,
  "include_source_health_summary": true
}
```

### 12.4 Required Output Fields

```json
{
  "digest": {
    "title": "string",
    "date_range": "1m",
    "generated_at": "datetime",
    "sources_searched": ["FDA", "TFDA", "ClinicalTrials.gov"],
    "search_criteria": {
      "agencies": ["FDA", "TFDA"],
      "registries": ["ClinicalTrials.gov"],
      "product_modality": ["antibody", "adc", "peptide"],
      "topics": ["CMC", "clinical"],
      "indications": ["NSCLC"],
      "companies": ["Roche", "Merck"]
    },
    "executive_summary": "string",
    "key_regulatory_updates": [
      {
        "title": "string",
        "agency": "FDA",
        "publication_date": "YYYY-MM-DD",
        "impact_level": "medium",
        "official_url": "string",
        "summary": "string"
      }
    ],
    "key_clinical_trial_updates": [
      {
        "trial_id": "NCT00000000",
        "title": "string",
        "sponsor": "string",
        "phase": "Phase 2",
        "status": "Recruiting",
        "last_update_date": "YYYY-MM-DD",
        "official_url": "string",
        "summary": "string"
      }
    ],
    "impact_matrix": [
      {
        "item": "string",
        "impact_level": "low | medium | high | critical",
        "impacted_functions": ["CMC", "clinical", "QA", "RA"],
        "recommended_follow_up": "string"
      }
    ],
    "source_health_summary": {
      "status": "pass | warning | failed | unknown",
      "open_failures": 0,
      "notes": ["string"]
    },
    "known_limitations": ["string"]
  }
}
```

### 12.5 Restrictions

- Do not include records outside the requested date range unless clearly marked as background.
- Do not omit source URLs for key updates.
- Do not present uncertain classifications as confirmed.
- Do not generate unsupported regulatory strategy recommendations.

---

## 13. Error Handling Standard

All tools should return structured errors.

Recommended error format:

```json
{
  "error": {
    "code": "SOURCE_UNAVAILABLE | INVALID_PARAMETER | NO_RESULTS | PARTIAL_RESULTS | INTERNAL_ERROR",
    "message": "string",
    "details": "string",
    "suggested_next_action": "string"
  }
}
```

Use `PARTIAL_RESULTS` when some sources succeeded but others failed.

Do not silently return incomplete results without warning.

---

## 14. No-Result Handling Standard

When a query returns no results, tools should clearly distinguish:

1. No matching records exist.
2. Source was not searched because it is out of phase.
3. Source was unavailable.
4. Search parameters were too narrow.
5. Data has not yet been ingested.

Recommended no-result response:

```json
{
  "records": [],
  "no_result_reason": "NO_MATCHING_RECORDS | SOURCE_OUT_OF_PHASE | SOURCE_UNAVAILABLE | QUERY_TOO_NARROW | DATA_NOT_INGESTED",
  "suggested_next_action": "string"
}
```

---

## 15. Implementation Rules for Codex

When implementing MCP tools, Codex must follow these rules:

1. Do not change tool names without updating this document.
2. Do not add new tools without updating this document.
3. Do not expose raw parser outputs directly to Claude.
4. Do not bypass source priority rules.
5. Do not use non-official sources as primary evidence.
6. Do not implement out-of-phase sources unless explicitly approved.
7. Preserve source URL, publication date, retrieval date, and source type.
8. Return structured errors instead of vague failures.
9. Add tests for normal results, no results, partial results, and source failures.
10. Keep MCP responses concise enough for Claude to use effectively.

---

## 16. Usage Rules for Claude

Claude should follow these rules when using MCP tools:

1. Use MCP tools before making source-based claims.
2. Report date range and sources searched.
3. Cite or reference official URLs from tool outputs.
4. Distinguish publication date, last update date, and retrieval date.
5. Flag uncertain classifications.
6. Avoid regulatory, legal, or medical final-decision claims.
7. Clearly state when results are partial or limited.
8. Do not infer approval success or clinical superiority from trial status alone.
9. Ask for narrower criteria only when the MCP result set is too large or ambiguous.
10. Do not bypass MCP tools by directly scraping raw official websites during normal execution.

---

## 17. Relationship to Other Documents

This document depends on:

```text
PROJECT_INSTRUCTION.md
docs/source_priority_matrix.md
docs/product_modality_taxonomy.md
```

This document supports:

```text
docs/data_dictionary.md
workflows/regulatory_clinical_intelligence_workflow.md
CLAUDE.md
AGENTS.md
README.md
```

If this document conflicts with `PROJECT_INSTRUCTION.md`, the project instruction governs overall scope.

If this document conflicts with `docs/source_priority_matrix.md`, the source priority matrix governs source selection.

If this document conflicts with `docs/product_modality_taxonomy.md`, the product modality taxonomy governs modality labels.

---

## 18. Current MVP v1 Tool Scope

For MVP v1, implement the following active source coverage:

```text
FDA
TFDA
ClinicalTrials.gov
```

For MVP v1, implement these tools first:

```text
search_regulatory_updates
get_regulatory_document_detail
search_clinical_trials_by_indication
check_source_health
list_source_failures
generate_regulatory_digest
```

The following may be implemented after the first MVP v1 tools are stable:

```text
compare_regulatory_updates
compare_companies_by_indication
```

Do not implement EMA, NMPA / CDE, PMDA, WHO ICTRP, EU CTIS, literature, patent, or commercial intelligence tools until the user explicitly approves moving to a later phase.

