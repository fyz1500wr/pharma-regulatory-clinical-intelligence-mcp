# Regulatory-Clinical Digest Clean-Source Dry-Run Memo

## Purpose

This document records a controlled clean-source dry-run memo for the PM/RA regulatory-clinical digest workflow.

The purpose is to validate whether the digest report workflow, prompt pack, validation exercise, and template contract remain readable and safe when the requested sources are available and no FDA source-unavailable condition is part of the scenario.

This is a documentation and review exercise only. It does not add a runtime report generator, MCP tool, template renderer, scheduler, dashboard, alerting, persistence, HTTP/SSE transport, `.mcp.json`, source expansion, company alias database, corporate-family mapping, product ownership inference, or literature/patent/finance/news integration.

## Scenario Status

| Item | Value |
|---|---|
| Exercise type | Controlled clean-source dry-run |
| Live source run | Not performed in this document |
| Runtime generator | Not implemented |
| Template renderer | Not implemented |
| New MCP tool | Not added |
| Source expansion | Not added |
| Decision use | Working intelligence only |

This dry-run is intentionally written as a controlled memo validation artifact, not as live regulatory or clinical evidence.

## Relationship To Existing Documents

Use this document together with:

| Document | Role |
|---|---|
| `docs/regulatory_clinical_digest_report_workflow.md` | Defines the memo workflow and section logic. |
| `docs/regulatory_clinical_digest_example_memo.md` | Provides a prior controlled memo example with partial source coverage. |
| `docs/regulatory_clinical_digest_prompt_pack.md` | Provides copy-paste prompts for controlled memo drafting and review. |
| `docs/regulatory_clinical_digest_memo_validation_exercise.md` | Defines pass / pass-with-limitations / fail criteria. |
| `docs/regulatory_clinical_digest_report_template_contract.md` | Defines the required input/output contract and acceptance criteria. |

## Clean-Source Dry-Run Scope

| Field | Controlled Value |
|---|---|
| Purpose | Clean requested-source digest memo dry-run |
| Indication | Gastric cancer |
| Companies | AstraZeneca, Merck |
| Regulatory sources requested | TFDA only |
| Clinical registry requested | ClinicalTrials.gov |
| FDA | Not requested in this clean-source dry-run |
| Date range | 1 year |
| Limit | 5 |
| Reviewer role | Human PM/RA reviewer |

Rationale for excluding FDA:

- A prior dry-run already validated partial source coverage where FDA was unavailable.
- This clean-source exercise is intended to validate memo behavior when requested sources are available.
- Excluding FDA is not a statement about FDA relevance, activity, or regulatory updates.

## Controlled Tool Output Assumptions

This document uses a controlled clean-source assumption set to test memo wording and template structure.

| Output Area | Controlled Assumption |
|---|---|
| `check_source_health` | TFDA pass; ClinicalTrials.gov pass; FDA not requested. |
| `generate_regulatory_digest` | Returns a bounded digest using TFDA and ClinicalTrials.gov outputs only. |
| `compare_companies_by_indication` | Returns bounded ClinicalTrials.gov-style company/sponsor association output. |
| Requested-source query errors | None for TFDA or ClinicalTrials.gov. |
| Global source-health warnings | None included in the clean-source memo body unless separately reported by tool output. |

Important limitation:

```text
This document does not claim that a live TFDA or ClinicalTrials.gov search was performed. It validates the memo contract and wording behavior under a clean requested-source scenario.
```

## Source Coverage Status

Primary source coverage label:

```text
CLEAN_REQUESTED_SOURCES
```

Interpretation:

- TFDA and ClinicalTrials.gov are the requested sources for this exercise.
- FDA is not requested and must not be summarized as unavailable, zero-result, or no-update in this memo.
- Clean requested-source coverage means no requested-source error is included in the controlled assumption set.
- Clean requested-source coverage does not prove complete recall.

Required wording:

```text
This memo covers the requested clean-source scenario: TFDA and ClinicalTrials.gov only. FDA was not requested for this exercise, so no FDA conclusion should be drawn.
```

Prohibited wording:

```text
No FDA updates were found.
```

Reason:

FDA was not requested, and a not-requested source cannot be interpreted as a zero-result source.

## Controlled PM/RA Memo

### Executive Summary

This controlled dry-run memo evaluates a clean-source regulatory-clinical digest scenario for gastric cancer using TFDA and ClinicalTrials.gov only, with AstraZeneca and Merck included for company/sponsor association review.

The source coverage status is `CLEAN_REQUESTED_SOURCES` for the controlled assumption set. No requested-source query error is included for TFDA or ClinicalTrials.gov in this exercise. FDA was intentionally excluded from this clean-source dry-run, so this memo does not provide FDA coverage or FDA conclusions.

The memo is suitable as a controlled PM/RA review example for validating structure, source coverage language, company/sponsor association caution, and human review checklist behavior. It is not suitable as live regulatory evidence or a final clinical, commercial, or management decision.

### Query Scope

| Field | Value |
|---|---|
| Indication | Gastric cancer |
| Companies | AstraZeneca, Merck |
| Requested regulatory source | TFDA |
| Requested clinical registry | ClinicalTrials.gov |
| Excluded source | FDA not requested |
| Date range | 1 year |
| Limit | 5 |
| Output type | Controlled PM/RA memo dry-run |

### Source Coverage Review

| Source | Requested? | Controlled Status | Memo Interpretation |
|---|---:|---|---|
| TFDA | Yes | Pass | TFDA is treated as available in this controlled clean-source scenario. |
| ClinicalTrials.gov | Yes | Pass | ClinicalTrials.gov is treated as available in this controlled clean-source scenario. |
| FDA | No | Not requested | No FDA conclusion should be drawn. |

Requested-source query errors:

```text
None included in this controlled clean-source assumption set.
```

Global source-health warnings:

```text
None included in this controlled clean-source memo body.
```

### Regulatory Update Findings

Controlled interpretation:

- TFDA is the only requested regulatory source in this dry-run.
- Any TFDA findings in a live run would need official URL and date metadata review before decision use.
- A zero TFDA count, if produced by an available-source live run, would be an available-source zero-result finding only for the queried scope and date range.
- This controlled document does not assert actual TFDA update counts.

Required PM/RA wording for a future live run:

```text
TFDA was queried as the requested regulatory source for this clean-source scenario. Any returned TFDA records require official URL and date-metadata review before decision use.
```

### Clinical Trial Findings

Controlled interpretation:

- ClinicalTrials.gov is the requested clinical registry in this dry-run.
- Returned trial records in a live run would be query results, not automatically confirmed sponsor-level company activity.
- Sponsor, collaborator, intervention, indication, phase, status, and results-availability fields would require human review before PM/RA or management-facing interpretation.
- This controlled document does not assert actual ClinicalTrials.gov trial counts.

Required PM/RA wording for a future live run:

```text
ClinicalTrials.gov returned records, if any, should be treated as query results until sponsor/collaborator and intervention fields are manually reviewed.
```

### Company / Sponsor Association Review

| Requested Company | Controlled Review Requirement | Interpretation Boundary |
|---|---|---|
| AstraZeneca | Separate sponsor-name matches from non-sponsor returned records. | Do not infer product ownership, corporate-family relationship, clinical success, approval probability, commercial strength, or superiority. |
| Merck | Separate sponsor-name matches from non-sponsor returned records. | Do not infer product ownership, corporate-family relationship, clinical success, approval probability, commercial strength, or superiority. |

Required wording:

```text
Returned records are MVP query results. They are not confirmed sponsor-level company activity unless sponsor identity is reviewed.
```

### Key Risks And Caveats

- Clean requested-source status does not prove complete recall.
- FDA was not requested in this clean-source exercise; no FDA conclusion should be drawn.
- TFDA findings, if any in a live run, require official URL and date-metadata review.
- ClinicalTrials.gov query results require sponsor/collaborator/intervention review before company-association interpretation.
- Sponsor-name matching does not infer product ownership or corporate-family relationship.
- Returned record counts must not be used to infer company superiority, approval probability, clinical success, or commercial strength.
- This controlled memo is working intelligence only.

### PM/RA Follow-Up Actions

For a future live clean-source run, the reviewer should:

1. Confirm TFDA returned records have official URLs and date metadata.
2. Confirm ClinicalTrials.gov returned records have sponsor/collaborator and intervention fields reviewed.
3. Separate sponsor-name matches from non-sponsor returned records for each requested company.
4. Preserve the statement that FDA was not requested and no FDA conclusion should be drawn.
5. Confirm that executive-summary wording does not imply complete market, regulatory, or clinical coverage.

### Human Review Checklist

- [ ] Query scope is explicit.
- [ ] TFDA and ClinicalTrials.gov are the only requested sources.
- [ ] FDA is clearly marked as not requested.
- [ ] No FDA zero-result wording is used.
- [ ] Requested-source errors are absent or explicitly listed.
- [ ] Source health is not over-interpreted as complete recall.
- [ ] TFDA official URLs and date metadata would be reviewed in a live run.
- [ ] ClinicalTrials.gov sponsor/collaborator/intervention fields would be reviewed in a live run.
- [ ] Sponsor-name matches are separated from non-sponsor returned records.
- [ ] No company superiority, ownership, approval, success, or commercial inference is made.
- [ ] Memo is labeled working intelligence only.

### Raw MCP Tool Traceability Placeholder

For a future live run, traceability should include:

| Tool | Expected Traceability |
|---|---|
| `check_source_health` | Confirm TFDA and ClinicalTrials.gov source status. |
| `generate_regulatory_digest` | Map returned regulatory and clinical findings to memo sections. |
| `compare_companies_by_indication` | Map company/sponsor association output to the company review section. |
| `get_regulatory_document_detail` | Optional for selected TFDA records requiring detail review. |

This controlled dry-run does not attach live raw tool outputs.

## Validation Against Template Contract

| Contract Area | Dry-Run Result | Notes |
|---|---|---|
| Required scope | Pass | Indication, companies, sources, date range, and limit are explicit. |
| Source coverage label | Pass | Uses `CLEAN_REQUESTED_SOURCES`. |
| Requested-source errors | Pass | None included in controlled assumption set. |
| FDA handling | Pass | FDA is not requested; no FDA conclusion is drawn. |
| Regulatory findings | Pass with controlled limitation | Structure is validated, but no live TFDA evidence is asserted. |
| Clinical findings | Pass with controlled limitation | Structure is validated, but no live ClinicalTrials.gov evidence is asserted. |
| Company/sponsor association | Pass | Required caution language is preserved. |
| PM/RA follow-up | Pass | Actions are review-oriented, not decision-oriented. |
| Human review checklist | Pass | Checklist preserves source and association cautions. |
| Runtime implementation readiness | Not approved | This dry-run does not approve runtime generator implementation. |

Overall validation result:

```text
PASS_WITH_CONTROLLED_LIMITATIONS
```

Reason:

- The clean-source memo structure is readable and aligned with the report template contract.
- Requested-source interpretation is clearer than the prior FDA-unavailable dry-run.
- FDA is correctly treated as not requested, not as zero-result.
- Company/sponsor association caveats are preserved.
- The exercise does not validate live TFDA or ClinicalTrials.gov availability or recall.

## Decision Gate

This clean-source dry-run supports the conclusion that the memo template contract can handle a clean requested-source scenario.

It does not by itself authorize runtime generator work.

Before runtime generator design, the project should still decide whether the next product priority is:

1. another dry-run using live or tool-generated outputs,
2. CMC/IND readiness mapping workflow,
3. source-health operator workflow,
4. or an explicitly approved runtime report generator.

## Explicit Non-Goals

This document does not:

- run live TFDA queries
- run live ClinicalTrials.gov queries
- add runtime code
- add a new MCP tool
- add new sources
- add scheduler, alerts, dashboard, persistence, or HTTP/SSE transport
- add `.mcp.json`
- add company alias or corporate-family mapping
- infer product ownership
- infer company superiority
- infer clinical success or approval probability
- replace PM/RA, clinical, legal, medical, commercial, or management review
