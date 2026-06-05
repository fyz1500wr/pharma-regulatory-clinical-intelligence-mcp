# Project State Continuation

Created: 2026-06-04  
Updated: 2026-06-05

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`

This file is a compact continuation handoff for starting a new chat.

Canonical detailed status remains in `.ai/PROJECT_STATE.md`.

## Current checkpoint

- Stable branch: `main`
- Latest confirmed main checkpoint: PR #88 merged into `main`
- PR #88 merge commit: `8aecccce4fee51b70b06b2ed9e7a144d545b3ce2`
- Validation record added by PR #88: `docs/validation_records/mvp_live_acceptance_validation_2026-06-04.md`
- Repository commit under v0.2.16 live validation: `3c9522d5014456f21d30c34dbf56c6c2c3a1572a`
- Latest completed release baseline: `v0.2.15-fda-abuse-detection-source-failure-diagnostics`
- v0.2.15 release tag commit: `c940a4f70bd3017b02c133712a2e2608baa9e098`
- Open PRs at this checkpoint: none confirmed before this continuation update

## Recent validation

v0.2.16 MVP live acceptance validation evidence has been recorded.

Regression baseline before live validation:

- `pytest tests/test_project_state_release_tag_consistency.py -q`: 5 passed
- `pytest -q`: 202 passed

Live validation result:

- Final decision: `ACCEPT_WITH_SOURCE_LIMITATIONS`
- Tool registry loaded all 8 MVP tools.
- FDA live source access was blocked by FDA abuse-detection/apology path and surfaced as `SOURCE_UNAVAILABLE`, not `NO_MATCHING_RECORDS`.
- TFDA source health passed; TFDA regulatory query returned a structured no-result for the selected query/date range.
- ClinicalTrials.gov indication search and company-by-indication comparison returned structured live outputs.
- Digest primary check preserved FDA source limitation in `query_metadata.source_errors`.
- Digest fallback check with TFDA + ClinicalTrials.gov generated structured output with empty `source_errors` for the requested source set.

## Current guardrails

- Keep MVP source scope limited to FDA, TFDA, and ClinicalTrials.gov.
- Do not add new agencies, sources, MCP tools, transport modes, dashboards, schedulers, alerts, persistence, external integrations, or repository automation unless explicitly approved.
- Keep future work small and phase-controlled.
- Use Traditional Chinese for user-facing discussion.
- Avoid accidental Japanese output.
- After repeated similar PRs, pause for direction calibration before continuing.

## Recommended next step

Recommended next discussion checkpoint:

`post-v0.2.16 — product-value / usability calibration before any feature expansion`

Direction options:

1. Product-value / functionality usability test of the current MCP tools using a realistic regulatory-clinical intelligence question.
2. Source-health operator guidance for FDA blocked-source handling without bypassing source controls.
3. Small governance cleanup only if a concrete traceability or consistency gap is identified.

Preferred next action:

Discuss whether the next practical test should simulate a real user-facing digest/report task using the current MVP tools, while preserving the no-expansion guardrails.

## New-chat opening prompt

請根據 GitHub repo `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`、`.ai/PROJECT_STATE.md`、以及 `PROJECT_STATE_CONTINUATION.md` 繼續。

請先確認 `main`、latest tag、open PR、測試狀態，再做 direction calibration。

除非我明確批准，不要新增來源、工具、scheduler、alerts、dashboard、persistence、HTTP/SSE、`.mcp.json`、GitHub automation、literature/patent/finance integration。