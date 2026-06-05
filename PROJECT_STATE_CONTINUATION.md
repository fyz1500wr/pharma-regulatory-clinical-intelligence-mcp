# Project State Continuation

Created: 2026-06-04  
Updated: 2026-06-05

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`

This file is a compact continuation handoff for starting a new chat.

Canonical detailed status remains in `.ai/PROJECT_STATE.md`.

## Current checkpoint

- Stable branch: `main`
- Latest confirmed main checkpoint: PR #92 merged into `main`
- PR #92 merge commit: `51b388d2db5304f2fda8e35df8cd7b8d59b4a056`
- Latest completed workstream: product-value / usability calibration and company-comparison association hardening
- Open PRs at this checkpoint: none confirmed before this continuation update

## Recent PR sequence

### PR #89

Added validation traceability metadata.

### PR #90

Clarified `compare_companies_by_indication` behavior when ClinicalTrials.gov sponsor lookups return `SOURCE_UNAVAILABLE`.

Interpretation rule:

- Source unavailable is not zero activity.
- A company row with unavailable source must be marked not evaluable.

### PR #91

Added `docs/product_value_usability_calibration.md`.

Purpose:

- Provide a product-value / usability calibration workflow.
- Help users test whether MVP outputs are readable, source-aware, and not misleading.

### PR #92

Clarified company comparison association labels and synchronized contract documentation.

Changed areas:

- `src/mcp_server/tools_clinical_trials.py`
- `tests/test_company_comparison_source_unavailable_display.py`
- `docs/mcp_tool_contract.md`
- `CLAUDE.md`

Key added or clarified fields:

- `association_mode`
- `sponsor_name_match_count`
- `non_sponsor_record_count`
- `requested_company`
- `record_sponsor`
- `sponsor_matches_requested_company`
- `association_basis`

Interpretation rule:

- Returned ClinicalTrials.gov query records are MVP query results.
- They must not be described as confirmed sponsor-level company activity unless sponsor identity is reviewed.
- Records with `association_basis = returned_by_clinicaltrials_gov_query_requires_manual_review` require manual sponsor or product-association review.

## Post-PR #92 usability re-test

Scenario used:

- Indication: gastric cancer
- Companies: AstraZeneca, Merck
- Regulatory sources: FDA, TFDA
- Registry: ClinicalTrials.gov
- Digest date range: 1y
- Company comparison date range: 3y

### Source health result

Overall source health was degraded because FDA returned `SOURCE_UNAVAILABLE` through an abuse-detection/apology path.

TFDA and ClinicalTrials.gov were available.

Interpretation:

- FDA failure is a source-access limitation.
- It must not be interpreted as FDA having zero matching regulatory updates.

### Digest result

Digest status: `PARTIAL`

Reason:

- Digest generated 0 regulatory updates and 5 clinical trial updates.
- FDA had 1 source query error.
- Source health reported 1 open failure.
- Digest correctly warned that it is rule-based aggregation, not final regulatory or clinical assessment.

### Company comparison result

Company comparison status: `PASS_WITH_LIMITATIONS`

Reason:

- ClinicalTrials.gov was available.
- Both AstraZeneca and Merck were activity-evaluable.
- Output exposed sponsor-name matches and non-sponsor returned records.

Observed results:

- AstraZeneca: 5 returned records; 4 sponsor-name matches; 1 record requires manual association review.
- Merck: 5 returned records; 1 sponsor-name match; 4 records require manual association review.
- Landscape summary explicitly stated that 5 returned records do not have sponsor names matching the requested company and require manual association review.

Remaining limitations:

- Date range is recorded in query metadata only; date-based trial filtering is not applied in MVP v1.
- ClinicalTrials.gov-only comparison does not include EU CTIS, WHO ICTRP, literature, patent, finance, or commercial intelligence sources.
- Company matching is sponsor-name based and does not infer corporate family relationships.

## Current overall usability status

Overall status: `PARTIAL_PASS`

Reason:

- Company comparison association ambiguity was materially improved and is now usable with clear caveats.
- Digest remains partial because FDA source access is unavailable in the current runtime.

## Current guardrails

- Keep MVP source scope limited to FDA, TFDA, and ClinicalTrials.gov.
- Do not add new agencies, sources, MCP tools, transport modes, dashboards, schedulers, alerts, persistence, external integrations, or repository automation unless explicitly approved.
- Keep future work small and phase-controlled.
- Use Traditional Chinese for user-facing discussion.
- Avoid accidental Japanese output.
- After repeated similar PRs, pause for direction calibration before continuing.

## Recommended next step

Do not immediately add new sources or new tools.

Recommended next discussion checkpoint:

`post-PR #92 — digest output usability calibration before feature expansion`

Direction options:

1. Evaluate `generate_regulatory_digest` output wording, especially:
   - `source_errors` visibility
   - partial source success
   - FDA unavailable handling in executive summary
   - whether regulatory update count could be misread when FDA is unavailable
2. Run a TFDA + ClinicalTrials.gov-only digest scenario to separate source-access limitation from digest wording issues.
3. Update digest documentation or runtime wording only if a concrete usability gap is confirmed.

Preferred next action:

Discuss whether the next practical test should focus on digest output wording while preserving the no-expansion guardrails.

## New-chat opening prompt

請根據 GitHub repo `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`、`.ai/PROJECT_STATE.md`、以及 `PROJECT_STATE_CONTINUATION.md` 繼續。

請先確認 `main`、latest tag、open PR、測試狀態，再做 direction calibration。

除非我明確批准，不要新增來源、工具、scheduler、alerts、dashboard、persistence、HTTP/SSE、`.mcp.json`、GitHub automation、literature/patent/finance integration。
