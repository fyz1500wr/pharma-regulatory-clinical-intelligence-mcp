# Regulatory-Clinical Digest Report Workflow

## Purpose

This workflow defines how to turn MVP v1 MCP outputs into a PM/RA-readable regulatory-clinical intelligence memo.

It is a workflow and reporting specification. It does not add new MCP tools, runtime behavior, data sources, scheduler, alerts, dashboard, persistence, HTTP/SSE transport, `.mcp.json`, or external integrations.

## MVP v1 Source Scope

Use only the approved MVP v1 sources:

```text
FDA
TFDA
ClinicalTrials.gov
```

Do not infer coverage from sources that were not queried, unavailable, or out of scope.

## Intended Users

Primary users:

- Regulatory affairs project managers
- Clinical intelligence reviewers
- CMC/RA cross-functional PMs who need a controlled intelligence brief

The report is intended to support review and follow-up planning. It is not a final regulatory, clinical, legal, medical, commercial, or management decision.

## Required Inputs

A report run should document the following inputs:

| Input | Requirement |
|---|---|
| Indication | Required for clinical trial search and company comparison. |
| Companies | Optional; if used, sponsor-name association limitations must be shown. |
| Regulatory agencies | Must remain FDA and/or TFDA in MVP v1. |
| Clinical registry | Must remain ClinicalTrials.gov in MVP v1. |
| Date range | Required for digest context; limitations must be disclosed where filtering is metadata-only. |
| Topics | Optional regulatory topic filter. |
| Product modality | Optional product modality filter. |
| Limit/page size | Required for traceability and bounded review. |

## Recommended MCP Tool Sequence

Use the existing MVP v1 tools in this order:

1. `check_source_health`
2. `generate_regulatory_digest`
3. `compare_companies_by_indication` when company context is requested
4. `get_regulatory_document_detail` only for selected regulatory records requiring detail review
5. `list_source_failures` when source-health context needs to be expanded

This workflow should not introduce new tools.

## Report Structure

The report should use the following sections.

### 1. Executive Summary

Purpose:

- State what was queried.
- State whether the result is clean, partial, or blocked by source limitations.
- State the highest-priority follow-up actions.

Required content:

- Indication and company scope
- Regulatory and clinical sources requested
- Regulatory update count
- Clinical trial update count
- Source coverage status
- Explicit warning that the memo is working intelligence only

Do not write:

- “No FDA updates” when FDA was unavailable
- “No company activity” when sponsor/company activity is not evaluable
- “Company A is ahead of Company B” based only on query-returned records

### 2. Source Coverage Status

Classify source coverage before presenting findings.

| Status | Meaning | Required wording |
|---|---|---|
| `CLEAN_REQUESTED_SOURCES` | No query errors occurred for requested sources. | “No source query errors occurred for requested sources.” |
| `PARTIAL_REQUESTED_SOURCE_COVERAGE` | At least one requested source returned a query error. | “Coverage is partial for requested source(s): [source]. Zero returned updates must not be interpreted as no updates for unavailable sources.” |
| `GLOBAL_HEALTH_WARNING_ONLY` | Global source health has open failures, but requested sources had no query errors in this run. | “Open source failures may include sources outside the requested source set.” |
| `BLOCKED_SOURCE` | A requested source is blocked or unavailable. | “This is a source-access limitation, not a no-result finding.” |

### 3. Regulatory Update Findings

For regulatory updates, present:

- agency
- title or update name
- date or publication/update metadata if available
- source URL
- topic/product modality classification where available
- whether detail retrieval was reviewed

If regulatory update count is zero, the report must distinguish:

- zero records returned from an available source
- zero records because a source was unavailable
- zero records because filters were narrow

### 4. Clinical Trial Findings

For clinical trial findings, present:

- registry
- NCT ID or trial identifier
- title
- phase
- status
- sponsor/collaborator fields when available
- results availability if available
- source URL

Do not convert a ClinicalTrials.gov query result into confirmed competitive strength or superiority.

### 5. Company / Sponsor Association Review

When using `compare_companies_by_indication`, report the distinction between:

- returned query records
- sponsor-name matches
- non-sponsor returned records requiring manual review
- unavailable source rows that are not activity-evaluable

Required wording:

```text
Returned records are MVP query results. They are not confirmed sponsor-level company activity unless sponsor identity is reviewed.
```

For each company, include:

| Field | Meaning |
|---|---|
| requested company | Company entered by the user. |
| returned records | Records returned by the ClinicalTrials.gov query. |
| sponsor-name matches | Returned records where sponsor name matches the requested company. |
| non-sponsor returned records | Returned records requiring manual association review. |
| activity evaluable | Whether available source data supports activity interpretation. |

### 6. Key Risks and Caveats

Always include caveats relevant to the run:

- source unavailable is not zero activity
- source health pass does not prove complete recall
- ClinicalTrials.gov query results may include non-sponsor-associated records
- date range behavior may be metadata-only where applicable
- official URLs and key findings require human verification
- output is not final regulatory, clinical, legal, medical, commercial, or management advice

### 7. PM/RA Recommended Follow-up Actions

Recommended actions should be concrete and reviewable.

Examples:

- Verify FDA manually when FDA is unavailable or source-blocked.
- Review source URLs for any high-impact regulatory records.
- Manually confirm sponsor identity for company-associated clinical trial records.
- Escalate source-health limitation if it affects a decision deadline.
- Record caveats in management-facing summaries.

Do not recommend decisions that require evidence not present in MVP v1 output.

### 8. Human Review Checklist

Before using the report externally, confirm:

- [ ] Requested sources are listed.
- [ ] Source errors are visible.
- [ ] Zero-count findings are not caused by unavailable sources.
- [ ] Company/trial association caveats are present.
- [ ] Official URLs are checked for decision-critical findings.
- [ ] All limitations are preserved in management-facing summaries.

### 9. Raw MCP Tool Traceability

Append a concise tool traceability section:

| Tool | Purpose | Output reviewed |
|---|---|---|
| `check_source_health` | Confirm live source availability. | source health status and open failures |
| `generate_regulatory_digest` | Produce combined regulatory/clinical digest. | executive summary, source errors, findings, limitations |
| `compare_companies_by_indication` | Review company/trial query output. | sponsor-name matches and manual-review records |
| `get_regulatory_document_detail` | Review selected document metadata. | title, URL, date, source metadata |

## Example Report Skeleton

```text
# Regulatory-Clinical Intelligence Memo

## Executive Summary
- Indication:
- Companies:
- Requested sources:
- Coverage status:
- Regulatory update count:
- Clinical trial update count:
- Key PM/RA takeaway:

## Source Coverage Status
- Requested sources:
- Source query errors:
- Global source-health warnings:
- Interpretation:

## Regulatory Update Findings
- Finding 1:
- Finding 2:
- No-record interpretation:

## Clinical Trial Findings
- Trial 1:
- Trial 2:
- Results availability:

## Company / Sponsor Association Review
- Company A:
  - returned records:
  - sponsor-name matches:
  - manual-review records:
- Company B:
  - returned records:
  - sponsor-name matches:
  - manual-review records:

## Risks and Caveats
- Source limitations:
- Association limitations:
- Decision-use limitations:

## PM/RA Recommended Follow-up Actions
1.
2.
3.

## Human Review Checklist
- [ ] Source errors reviewed
- [ ] Official URLs verified
- [ ] Sponsor association reviewed
- [ ] Caveats preserved

## Raw MCP Tool Traceability
- Tool:
- Parameters:
- Output section used:
```

## Acceptance Criteria

This workflow is considered usable when a reviewer can answer:

1. Which sources were requested?
2. Which requested sources were unavailable or partial?
3. Whether a zero count means no records or source unavailability?
4. Which clinical trial records are sponsor-name matches?
5. Which returned records require manual sponsor/product association review?
6. What actions PM/RA should take next?

If any of these cannot be answered, the report is not ready for management-facing use.
