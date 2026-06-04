# Project State Continuation

Created: 2026-06-04

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`

This file is a compact continuation handoff for starting a new chat.

Canonical detailed status remains in `.ai/PROJECT_STATE.md`.

## Current checkpoint

- Stable branch: `main`
- Latest confirmed main commit: `c56ca2630fb8c85a01b4203a34c043a23cf7b283`
- Latest completed release: `v0.2.15`
- Latest governance checkpoint: PR #86, long-context continuation checkpoint rule
- Open PRs at creation time: none confirmed

## Recent validation

After PR #86 was merged and `main` was synced:

- `pytest tests/test_project_state_release_tag_consistency.py -q`: 5 passed
- `pytest -q`: 202 passed

## Current guardrails

- Keep MVP source scope limited to FDA, TFDA, and ClinicalTrials.gov.
- Do not add new agencies, sources, MCP tools, transport modes, dashboards, schedulers, alerts, persistence, external integrations, or repository automation unless explicitly approved.
- Keep future work small and phase-controlled.
- Use Traditional Chinese for user-facing discussion.
- Avoid accidental Japanese output.
- After repeated similar PRs, pause for direction calibration before continuing.

## Recommended next step

Recommended next checkpoint:

`v0.2.16 — direction calibration and next product-value checkpoint`

Direction options:

1. Product-value / functionality check of the current MCP tools.
2. Source-health operator guidance.
3. Small governance cleanup only if a specific gap is identified.

Preferred next action:

Perform direction calibration before starting another documentation or project-state PR.

## New-chat opening prompt

請根據 GitHub repo `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`、`.ai/PROJECT_STATE.md`、以及 `PROJECT_STATE_CONTINUATION.md` 繼續。

請先確認 `main`、latest tag、open PR、測試狀態，再做 direction calibration。

除非我明確批准，不要新增來源、工具、scheduler、alerts、dashboard、persistence、HTTP/SSE、`.mcp.json`、GitHub automation、literature/patent/finance integration。
