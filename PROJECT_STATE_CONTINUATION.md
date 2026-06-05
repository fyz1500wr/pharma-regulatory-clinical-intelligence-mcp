# Project State Continuation

Created: 2026-06-04  
Updated: 2026-06-05

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`

This file is a compact continuation handoff for starting a new chat.

Canonical detailed status remains in `.ai/PROJECT_STATE.md`.

## Current checkpoint

- Stable branch: `main`
- Latest confirmed main checkpoint: PR #94 merged into `main`
- PR #94 merge commit: `5144cfc3b282206a8840091f8716eb6399b2aae2`
- Latest completed workstream: source-limitation / usability hardening for company comparison and digest outputs
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

### PR #93

Updated this continuation file from the prior PR #88 checkpoint to the PR #92 usability checkpoint.

### PR #94

Clarified digest source coverage wording and added regression tests.

Changed areas:

- `src/mcp_server/tools_digest.py`
- `tests/test_digest_source_coverage_wording.py`

Interpretation rule:

- If requested sources return query errors, digest output must state that coverage is partial.
- Zero returned regulatory updates must not be interpreted as no updates for unavailable requested sources.
- If there are global source-health failures but no query errors for the requested digest sources, digest output must say that no source query errors occurred for the requested sources.

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

### Digest result before PR #94

Digest status: `PARTIAL`

Reason:

- Digest generated 0 regulatory updates and 5 clinical trial updates.
- FDA had 1 source query error.
- Source health reported 1 open failure.
- Digest warned that it is rule-based aggregation, not final regulatory or clinical assessment.
- Usability gap: executive summary did not directly state that FDA source unavailability makes requested-source coverage partial.

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

## Post-PR #94 digest re-test

Scenario used:

- Indication: gastric cancer
- Companies: AstraZeneca, Merck
- Clean digest sources: TFDA + ClinicalTrials.gov
- Partial digest sources: FDA + TFDA + ClinicalTrials.gov
- Date range: 1y

### Clean scenario result

Clean scenario status: `PASS_WITH_GLOBAL_HEALTH_WARNING`

Observed behavior:

- Digest generated 0 regulatory updates and 5 clinical trial updates.
- `source_errors_count` was 0.
- Executive summary stated that 1 open source failure was reported by source health tools, but no source query errors occurred for the requested sources in this digest.
- Known limitations stated that open source failures may include sources outside the requested digest source set and that `query_metadata.source_errors` identifies requested source query failures.

Interpretation:

- This avoids implying that TFDA or ClinicalTrials.gov failed when the open failure comes from global source health.

### Partial scenario result

Partial scenario status: `PASS_WITH_SOURCE_LIMITATION`

Observed behavior:

- Digest generated 0 regulatory updates and 5 clinical trial updates.
- FDA returned `SOURCE_UNAVAILABLE`.
- `source_errors_count` was 1.
- Executive summary stated: `Coverage is partial for requested source(s): FDA`.
- Executive summary also stated that zero returned updates must not be interpreted as no updates for unavailable sources.
- Known limitations repeated that coverage is partial because FDA returned query errors.

Interpretation:

- This directly addresses the prior PM/RA misreading risk.

## Current overall usability status

Overall status: `PASS_WITH_SOURCE_LIMITATIONS`

Reason:

- Company comparison association ambiguity is now clearly labeled.
- Digest partial-source coverage is now clearly labeled.
- FDA remains unavailable in the current runtime, so live FDA coverage is still not complete.

Remaining limitations:

- FDA source access may be blocked by abuse-detection/apology path in current runtime.
- Date range is recorded in company-comparison query metadata only; date-based trial filtering is not applied in MVP v1 company comparison.
- ClinicalTrials.gov-only comparison does not include EU CTIS, WHO ICTRP, literature, patent, finance, or commercial intelligence sources.
- Company matching is sponsor-name based and does not infer corporate family relationships.

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

`post-PR #94 — direction calibration before any feature expansion`

Direction options:

1. Stop and treat PR #89–#94 as a completed source-limitation/usability hardening phase.
2. Run a final `main` status check and review whether `.ai/PROJECT_STATE.md` also needs a compact checkpoint update.
3. If continuing runtime work, prioritize only concrete MVP interpretation gaps; do not add new data sources yet.
4. Defer company alias database, corporate-family mapping, product ownership inference, dashboard, scheduler, alerts, persistence, and external source expansion until explicitly approved.

Preferred next action:

Hold direction calibration before further implementation.

## New-chat opening prompt

請根據 GitHub repo `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`、`.ai/PROJECT_STATE.md`、以及 `PROJECT_STATE_CONTINUATION.md` 繼續。

請先確認 `main`、latest tag、open PR、測試狀態，再做 direction calibration。

除非我明確批准，不要新增來源、工具、scheduler、alerts、dashboard、persistence、HTTP/SSE、`.mcp.json`、GitHub automation、literature/patent/finance integration。
