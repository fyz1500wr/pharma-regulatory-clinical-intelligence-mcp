# Regulatory-Clinical Digest Prompt Pack

## Purpose

This prompt pack provides controlled prompts for turning MVP v1 MCP outputs into a PM/RA-facing regulatory-clinical intelligence memo.

Use these prompts with the workflow defined in `docs/regulatory_clinical_digest_report_workflow.md` and the example memo in `docs/regulatory_clinical_digest_example_memo.md`.

These prompts do not expand source scope, add MCP tools, automate decisions, or replace human review.

## Required Inputs Before Prompting

Before using the prompts, collect or paste outputs from the relevant MVP tools:

1. `check_source_health`
2. `generate_regulatory_digest`
3. `compare_companies_by_indication` when company context is included
4. `list_source_failures` when source limitations need explanation
5. `get_regulatory_document_detail` only for selected records requiring detail review

Always include the user-requested scope:

```text
Indication:
Companies:
Regulatory agencies:
Clinical registry:
Date range:
Product modality / topic filters:
```

## Core Prompt — PM/RA Memo Generation

```text
You are preparing a PM/RA-facing regulatory-clinical intelligence memo from MVP v1 MCP tool outputs.

Use only the provided MCP outputs. Do not browse the web. Do not infer facts that are not present in the tool outputs.

Scope:
- Indication: [insert indication]
- Companies: [insert companies, if any]
- Regulatory sources requested: [FDA and/or TFDA]
- Clinical registry requested: ClinicalTrials.gov
- Date range: [insert date range]
- Filters: [insert topic/product modality filters, if any]

Required rules:
1. Source unavailable is not zero activity.
2. If a requested source has `SOURCE_UNAVAILABLE`, `BLOCKED_SOURCE`, source error, or detected source block, state that coverage is partial.
3. Do not say “no FDA updates” when FDA was unavailable.
4. ClinicalTrials.gov returned records are query results, not confirmed sponsor-level company activity unless sponsor identity is reviewed.
5. Separate sponsor-name matches from non-sponsor returned records when company comparison output is available.
6. Do not infer company superiority, approval probability, commercial strength, ownership, or corporate family relationship.
7. Preserve all source limitations and known caveats in the executive summary and risks section.
8. The memo must state that it is working intelligence only, not a final regulatory, clinical, legal, medical, commercial, or management decision.

Memo structure:
1. Executive Summary
2. Source Coverage Status
3. Regulatory Update Findings
4. Clinical Trial Findings
5. Company / Sponsor Association Review
6. Key Risks and Caveats
7. PM/RA Recommended Follow-up Actions
8. Human Review Checklist
9. Raw MCP Tool Traceability

Now generate the memo.
```

## Prompt — Clean Requested Sources Scenario

Use when requested sources completed without source query errors, even if global source-health warnings exist for sources outside the requested set.

```text
Generate a PM/RA-facing regulatory-clinical intelligence memo from the attached MCP outputs.

Important source-coverage instruction:
- If the digest reports no query errors for the requested sources, state that no requested-source query errors occurred.
- If global source-health warnings exist for sources outside the requested source set, describe them separately as global source-health warnings.
- Do not let unrelated source-health warnings change the interpretation of the requested-source query result.

Keep the report inside MVP v1 scope: FDA, TFDA, and ClinicalTrials.gov only.
```

## Prompt — Partial Requested Source Coverage Scenario

Use when FDA, TFDA, or ClinicalTrials.gov was requested but returned a source query error.

```text
Generate a PM/RA-facing regulatory-clinical intelligence memo from the attached MCP outputs.

Important source-coverage instruction:
- At least one requested source has a source query error or unavailable-source condition.
- State clearly: “Coverage is partial for requested source(s): [source]. Zero returned updates must not be interpreted as no updates for unavailable sources.”
- In regulatory findings, separate unavailable-source status from zero returned records.
- Add a PM/RA follow-up action requiring manual verification of the unavailable requested source.

Do not infer source absence, company inactivity, clinical success, regulatory outcome, or commercial strength.
```

## Prompt — Company Comparison / Sponsor Association Scenario

Use when `compare_companies_by_indication` output is included.

```text
Generate the Company / Sponsor Association Review section from the attached `compare_companies_by_indication` output.

Required rules:
1. Treat returned records as ClinicalTrials.gov query results.
2. Do not call returned records confirmed company activity unless sponsor-name matching supports that statement.
3. Separate:
   - requested company
   - returned records
   - sponsor-name matches
   - non-sponsor records requiring manual review
   - activity evaluable / not evaluable
4. If source is unavailable for a company row, state that the row is not activity-evaluable.
5. Do not infer ownership, corporate family relationship, product association, company superiority, approval probability, or commercial strength.

Output a concise table and a short interpretation paragraph.
```

## Prompt — Executive Summary Only

Use when a short management-facing summary is needed, but limitations must remain visible.

```text
Write only the Executive Summary section for a PM/RA regulatory-clinical intelligence memo.

Include:
- indication
- companies, if any
- requested sources
- regulatory update count
- clinical trial update count
- requested-source coverage status
- whether any source was unavailable
- one to three PM/RA follow-up actions

Do not omit caveats. Do not overstate findings. Do not infer final regulatory, clinical, commercial, or competitive conclusions.
```

## Prompt — Human Review Checklist Only

Use when preparing an internal QC step before sharing the memo.

```text
Create a Human Review Checklist for the attached regulatory-clinical intelligence memo and MCP outputs.

The checklist must confirm:
- requested sources are listed
- source errors are visible
- zero counts are not caused by unavailable sources
- official URLs are manually verified for decision-critical findings
- ClinicalTrials.gov returned records are not over-interpreted as confirmed sponsor activity
- sponsor-name matches are separated from non-sponsor returned records
- limitations are preserved in downstream summaries

Keep the checklist concise and actionable.
```

## Prompt — Red Flag Review

Use to check whether a draft memo contains overstatements.

```text
Review the attached draft regulatory-clinical intelligence memo for overstatement risk.

Flag any sentence that:
1. Treats source unavailable as no updates or no activity.
2. Treats ClinicalTrials.gov query results as confirmed sponsor activity without sponsor review.
3. Infers company superiority, ownership, approval probability, commercial strength, or final regulatory status.
4. Omits source limitations from the executive summary.
5. Presents working intelligence as final advice.

For each flagged sentence, provide a safer replacement.
```

## Prompt — Minimal One-Page Memo

Use when the PM/RA audience needs a concise summary.

```text
Create a one-page PM/RA regulatory-clinical intelligence memo from the attached MVP v1 MCP outputs.

The memo must include:
1. Scope
2. Source Coverage Status
3. Key Findings
4. Key Limitations
5. Recommended Follow-up Actions

Keep it concise. Do not remove source coverage caveats. Do not infer facts beyond the MCP outputs.
```

## Prompting Guardrails

Do not ask the model to:

- determine whether a company is ahead or behind competitors based only on MVP query output
- infer product ownership from company names
- infer corporate family relationships
- treat unavailable sources as zero-result sources
- produce final regulatory strategy recommendations without human review
- browse outside the provided MCP outputs
- add non-MVP sources such as EMA, PMDA, NMPA, WHO ICTRP, EU CTIS, literature, patent, or finance sources unless separately approved

## Output Quality Check

A generated memo is acceptable only if the reader can answer:

1. Which sources were requested?
2. Which requested sources were unavailable or partial?
3. Whether zero returned updates mean no records or source unavailability?
4. Which trial records are sponsor-name matches?
5. Which records require manual association review?
6. What follow-up actions are needed before decision use?

If the memo does not answer these questions, revise before sharing.
