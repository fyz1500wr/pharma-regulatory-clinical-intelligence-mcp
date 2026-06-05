# Regulatory-Clinical Digest Report Template Contract

## Purpose

This document defines the controlled report template contract for PM/RA regulatory-clinical digest memos generated from MVP v1 tool outputs.

It is a documentation and specification contract only. It does not add a runtime report generator, MCP tool, template renderer, scheduler, alerting, dashboard, persistence, HTTP/SSE transport, `.mcp.json`, new source, company alias database, corporate-family mapping, product ownership inference, or external literature/patent/finance/news integration.

## Relationship To Existing Digest Documents

Use this contract with:

| Document | Role |
|---|---|
| `docs/regulatory_clinical_digest_report_workflow.md` | Defines the human workflow and memo section logic. |
| `docs/regulatory_clinical_digest_example_memo.md` | Shows a controlled example memo. |
| `docs/regulatory_clinical_digest_prompt_pack.md` | Provides copy-paste prompts for memo drafting and review. |
| `docs/regulatory_clinical_digest_memo_validation_exercise.md` | Defines dry-run validation before runtime implementation. |

This contract converts the workflow into a fixed set of required inputs, output fields, section requirements, source coverage labels, company/sponsor association fields, and acceptance criteria.

## MVP v1 Scope Boundary

The contract is limited to the approved MVP v1 source scope:

```text
FDA
TFDA
ClinicalTrials.gov
```

Do not add or imply coverage for EMA, PMDA, NMPA, CTIS, WHO ICTRP, literature, patent, finance, news, company alias data, corporate-family mapping, product ownership inference, commercial intelligence, or other external sources unless separately approved.

## Contract Status

| Item | Status |
|---|---|
| Contract type | Docs/spec only |
| Runtime implementation | Not implemented |
| Template renderer | Not implemented |
| MCP-side report generation helper | Not implemented |
| Persistent storage | Not implemented |
| Source expansion | Not approved |
| Decision authority | Human PM/RA review required |

## Required Input Object

A future runtime implementation, if separately approved later, should not proceed unless these inputs can be provided or explicitly marked as not applicable.

| Field | Required | Allowed / Expected Value | Notes |
|---|---:|---|---|
| `run_purpose` | Yes | Free text | Example: regulatory-clinical digest memo dry-run. |
| `run_date` | Yes | ISO date or clearly stated date | Date the tool outputs were generated or reviewed. |
| `reviewer` | Optional | Free text | Human reviewer or role. |
| `indication` | Yes | Free text | Required for clinical trial search and company comparison. |
| `companies` | Conditional | List of company names | Required when company comparison or sponsor association review is included. |
| `regulatory_sources_requested` | Yes | `FDA`, `TFDA`, or both | Must remain inside MVP v1 source scope. |
| `clinical_registry_requested` | Conditional | `ClinicalTrials.gov` | Required when clinical trial findings are included. |
| `date_range` | Yes | Free text or structured range | Must be preserved in the memo scope. |
| `topic_filters` | Optional | List or free text | Preserve exactly as queried. |
| `product_modality_filters` | Optional | List or free text | Preserve exactly as queried. |
| `limit_or_page_size` | Yes | Integer or text description | Required for traceability and bounded review. |
| `tool_outputs_reviewed` | Yes | List of MVP tool outputs | At minimum, include the relevant tool names and output sections reviewed. |

## Required Tool Output Inputs

The memo contract expects the following existing MVP v1 tool outputs where applicable.

| Tool output | Required? | Purpose |
|---|---:|---|
| `check_source_health` | Yes | Provides requested-source and global source-health context. |
| `generate_regulatory_digest` | Yes | Provides executive summary, regulatory findings, clinical findings, source query errors, and limitations. |
| `compare_companies_by_indication` | Conditional | Required when company or sponsor association review is included. |
| `list_source_failures` | Conditional | Required when source failures need explanation beyond the digest. |
| `get_regulatory_document_detail` | Optional | Used only for selected regulatory records requiring detail review. |

This contract does not introduce new tools.

## Required Output Object

A completed memo should be reviewable against the following output object.

| Field | Required | Notes |
|---|---:|---|
| `memo_title` | Yes | Should identify the memo as regulatory-clinical intelligence. |
| `query_scope` | Yes | Must include indication, companies if any, sources, date range, filters, and limit/page size. |
| `source_coverage_status` | Yes | Must use one of the contract labels below. |
| `requested_source_errors` | Yes | Empty list allowed only if no requested-source query errors occurred. |
| `global_source_health_warnings` | Yes | Must be separated from requested-source errors. |
| `regulatory_update_findings` | Yes | May be empty only with a clear no-record or unavailable-source interpretation. |
| `clinical_trial_findings` | Conditional | Required when ClinicalTrials.gov was requested. |
| `company_sponsor_association_review` | Conditional | Required when companies are included. |
| `key_risks_and_caveats` | Yes | Must include all material interpretation limitations. |
| `pm_ra_follow_up_actions` | Yes | Actions must be specific and evidence-linked. |
| `human_review_checklist` | Yes | Must preserve source, URL, and association review checks. |
| `raw_tool_traceability` | Yes | Must map memo sections to reviewed tool outputs. |
| `decision_use_statement` | Yes | Must state that the memo is working intelligence only. |

## Source Coverage Status Labels

Use exactly one primary source coverage label, with supplemental notes as needed.

| Label | Required Condition | Required Interpretation |
|---|---|---|
| `CLEAN_REQUESTED_SOURCES` | Requested sources completed without query errors. | No requested-source query errors occurred. Source-health pass does not prove complete recall. |
| `PARTIAL_REQUESTED_SOURCE_COVERAGE` | At least one requested source returned a query error or unavailable condition. | Coverage is partial for requested source(s). Zero returned updates must not be interpreted as no updates for unavailable sources. |
| `GLOBAL_HEALTH_WARNING_ONLY` | Requested sources completed, but global source-health warnings exist for sources outside the requested query result. | Open source failures may include sources outside the requested source set and must not be mixed into requested-source findings. |
| `BLOCKED_SOURCE` | A requested source was blocked or otherwise source-unavailable. | This is a source-access limitation, not a no-result finding. Manual verification is required. |
| `INSUFFICIENT_OUTPUT_FOR_MEMO` | Required tool outputs, scope, or traceability are missing. | Memo is not ready for PM/RA or management-facing use. |

If both `PARTIAL_REQUESTED_SOURCE_COVERAGE` and `BLOCKED_SOURCE` apply, use `PARTIAL_REQUESTED_SOURCE_COVERAGE` as the primary label and explicitly name the blocked source in the interpretation.

## Fixed Memo Sections

A compliant memo must use these sections unless a section is marked not applicable with a reason.

### 1. Executive Summary

Required fields:

| Field | Requirement |
|---|---|
| Scope statement | State indication, companies if any, requested sources, date range, and limit/page size. |
| Coverage statement | State the source coverage label and requested-source limitations. |
| Finding summary | Summarize regulatory and clinical counts without overstating completeness. |
| Follow-up summary | List the highest-priority PM/RA follow-up actions. |
| Decision-use statement | State that the memo is working intelligence only. |

Required safety rule:

```text
Do not write “No FDA updates” when FDA was unavailable.
```

### 2. Source Coverage Status

Required fields:

| Field | Requirement |
|---|---|
| Requested sources | List all requested MVP sources. |
| Source status by source | Show pass, unavailable, blocked, error, or not requested. |
| Requested-source query errors | List errors for requested sources only. |
| Global source-health warnings | List separately from requested-source query errors. |
| Interpretation | Explain whether zero counts are evaluable or affected by source limitations. |

### 3. Regulatory Update Findings

Required fields for each regulatory finding:

| Field | Requirement |
|---|---|
| `agency` | FDA or TFDA. |
| `title_or_update_name` | Preserve title or update name when available. |
| `date_metadata` | Publication/update date when available. |
| `source_url` | Official source URL when available. |
| `topic_or_product_modality` | Include when available from tool output. |
| `detail_review_status` | State whether detail retrieval was reviewed. |
| `interpretation_limitations` | State no-record, partial-coverage, or narrow-filter caveats. |

If records are not returned, the section must distinguish:

1. available source with zero returned records
2. unavailable requested source
3. narrow filter or metadata limitation
4. out-of-scope source not queried

### 4. Clinical Trial Findings

Required fields for each clinical trial finding:

| Field | Requirement |
|---|---|
| `registry` | ClinicalTrials.gov. |
| `trial_identifier` | NCT ID or available identifier. |
| `title` | Trial title when available. |
| `phase` | Reported phase when available. |
| `status` | Recruitment or trial status when available. |
| `sponsor_collaborator_fields` | Preserve fields used for association review. |
| `results_availability` | Report only when present in tool output. |
| `source_url` | ClinicalTrials.gov URL when available. |
| `interpretation_limitations` | State that returned records are query results until sponsor/product association is reviewed. |

Do not convert ClinicalTrials.gov query returns into confirmed company pipeline ownership, clinical success, approval probability, or competitive superiority.

### 5. Company / Sponsor Association Review

Required when companies are included.

For each requested company, include:

| Field | Required Interpretation |
|---|---|
| `requested_company` | Company name exactly as queried. |
| `returned_records` | Records returned by the query, not automatically confirmed company activity. |
| `sponsor_name_matches` | Returned records where sponsor name matches the requested company. |
| `non_sponsor_returned_records` | Records requiring manual sponsor/product association review. |
| `activity_evaluable` | Whether source data supports limited activity interpretation. |
| `association_review_required` | Yes unless sponsor/product association has been manually reviewed. |
| `limitations` | Must state no ownership, corporate-family, superiority, approval, or commercial inference. |

Required wording:

```text
Returned records are MVP query results. They are not confirmed sponsor-level company activity unless sponsor identity is reviewed.
```

### 6. Key Risks and Caveats

The section must include applicable caveats:

- source unavailable is not zero activity
- source health pass does not prove complete recall
- ClinicalTrials.gov returned records may include non-sponsor records
- sponsor-name matching does not infer ownership or corporate-family relationship
- date range behavior may be metadata-limited
- official URLs require manual verification for decision-critical findings
- memo is working intelligence only

### 7. PM/RA Recommended Follow-up Actions

Actions must be:

- linked to a source, finding, or limitation
- specific enough for a PM/RA reviewer to assign or track
- phrased as verification or follow-up, not final decision-making

Allowed examples:

- Manually verify FDA because FDA was unavailable in the run.
- Review ClinicalTrials.gov sponsor and collaborator fields for returned company-associated records.
- Confirm official URLs for decision-critical regulatory findings.
- Preserve source limitation language in any management-facing summary.

Disallowed examples:

- Approve a regulatory strategy based only on this memo.
- Conclude one company is ahead based only on returned query counts.
- Infer product ownership or corporate-family relationship from company names.

### 8. Human Review Checklist

Minimum checklist:

- [ ] Query scope is explicit.
- [ ] Requested sources are listed.
- [ ] Requested-source errors are visible.
- [ ] Global source-health warnings are separated from requested-source errors.
- [ ] Zero counts are not caused by unavailable sources.
- [ ] Official URLs are reviewed for decision-critical findings.
- [ ] ClinicalTrials.gov returned records are not over-interpreted.
- [ ] Sponsor-name matches are separated from non-sponsor returned records.
- [ ] Limitations are preserved in downstream summaries.
- [ ] Memo is labeled working intelligence only.

### 9. Raw MCP Tool Traceability

Required fields:

| Field | Requirement |
|---|---|
| `tool_name` | Existing MVP v1 tool name. |
| `tool_purpose` | Why the output was reviewed. |
| `parameters_or_scope` | Query scope or parameters used. |
| `output_sections_used` | Memo sections supported by the output. |
| `limitations_preserved` | Caveats carried into the memo. |

## Minimum Compliance Checklist

A memo complies with this contract only if a reviewer can answer all of the following:

1. What indication, companies, sources, date range, filters, and limit/page size were used?
2. Which requested sources completed, failed, or were unavailable?
3. Are requested-source errors separated from global source-health warnings?
4. Does any zero count represent an available-source zero result, an unavailable-source limitation, or a narrow-filter result?
5. Which regulatory findings have official URLs and date metadata?
6. Which ClinicalTrials.gov records are sponsor-name matches?
7. Which returned trial records require manual sponsor/product association review?
8. What PM/RA follow-up actions are required before decision use?
9. Are all material caveats preserved in the executive summary and risks section?
10. Is the memo clearly labeled as working intelligence only?

## Acceptance Criteria Before Runtime Implementation

Do not design or implement a runtime report generator, template renderer, or MCP-side report generation helper unless all criteria below are satisfied in a separate approved scope decision.

| Criterion | Required Evidence |
|---|---|
| Dry-run memo validation | At least one dry-run memo has passed or passed with limitations under `docs/regulatory_clinical_digest_memo_validation_exercise.md`. |
| Source limitation preservation | The memo preserves unavailable-source language and does not treat unavailable sources as zero-result sources. |
| Requested-source separation | Requested-source query errors are separated from global source-health warnings. |
| Company association control | Sponsor-name matches are separated from non-sponsor returned records. |
| No prohibited inference | The memo does not infer company superiority, ownership, corporate-family relationship, approval probability, clinical success, or commercial strength. |
| Human review workflow | PM/RA follow-up actions and human review checklist are present. |
| Scope approval | Runtime implementation has been explicitly approved as a new scope decision. |

## Explicit Non-Goals

This contract does not authorize:

- runtime report generation
- automated template rendering
- new MCP tools
- new data sources
- persistent source-failure history
- dashboards, alerts, or schedulers
- HTTP/SSE transport
- `.mcp.json` changes
- company alias databases
- corporate-family mapping
- product ownership inference
- literature, patent, finance, or news integration
- final regulatory, clinical, medical, legal, commercial, or management decision-making

## Change Control

Future changes to this contract should remain documentation/specification-only unless a separate scope decision explicitly authorizes implementation.

Any runtime implementation proposal should reference this contract and explain which acceptance criteria are already satisfied and which remain open.
