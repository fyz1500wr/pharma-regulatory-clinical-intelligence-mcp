# Project State Continuation

Created: 2026-06-04  
Updated: 2026-06-10

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`

This file is a compact continuation handoff for starting a new chat. Canonical detailed status remains in `.ai/PROJECT_STATE.md`.

## Current checkpoint

- Stable branch: `main`
- Latest confirmed merged PR: PR #116
- PR #116 merge commit: `0fe5ab259e2502e925cdf367d5c3f0cfb66d12ef`
- Latest completed workstream: Open-source Claude/Codex/MCP tool survey after original requirements traceability.
- Latest validation status: `PASS`
- Latest validation evidence:
  - `python -m pytest tests/test_readme_documentation_index.py -q` → `10 passed`
  - `python -m pytest -q` → `212 passed`
  - `git status --short` → clean / no output
- Current tagged release: remains `v0.2.15-fda-abuse-detection-source-failure-diagnostics`; no new release tag was created for PR #97–#116 docs/product workflow work.
- Open PRs after PR #116 merge: none known at checkpoint.
- Execution environment note: Codespaces quota is near limit until July 2026. For upcoming code/test work, default to Claude Code Web and Codex Web workflows. Do not assume Codespaces is available unless the user explicitly says it is available again.

## Original user requirement baseline

The project is in build-stage and must be evaluated against the user's original full-system requirements, not only the recent CMC workstream.

Original target system:

1. Build a GitHub-based system architecture where project and code construction happen in Codex/GitHub, then the final usable knowledge/workflow is moved into Claude Project for execution.
2. Track updates from FDA, EMA, TFDA, NMPA, and PMDA, including dates and official document links, over date windows from 1 month to 5 years.
3. Support regulatory/guidance retrieval by biologic product modality.
4. Track clinical trial progress and results by indication and sponsor/company, preferably using official registry APIs.
5. Detect source, webpage, API, or parser changes and support correction through source-health diagnostics before any future notification design.
6. Prefer official APIs where available and use MCP-based retrieval.
7. Evaluate open-source or openly documented tools that can support Claude/Codex for at least one original-system function.

## Current alignment to original requirements

Current rough alignment after PR #116:

```text
Original Regulatory / Clinical Intelligence MCP system: about 45–50% complete
Project governance / GitHub + Claude/Codex workflow foundation: about 72% complete
CMC readiness extension module: about 75% complete
Overall build-stage system: about 56–60% complete
```

Interpretation:

- The repo has a useful MVP regulatory-clinical intelligence subset using FDA, TFDA, and ClinicalTrials.gov.
- The repo has a useful CMC readiness docs/spec extension.
- The repo now has an original requirements traceability matrix.
- The repo now has a docs/spec-only open-source Claude/Codex/MCP tool survey.
- EMA, NMPA/CDE, and PMDA are not active MVP sources.
- Scheduler, alerts, persistence, dashboard, and multi-source runtime automation are not implemented.

## Current MVP source scope and deliberate limitation

Approved MVP v1 active source scope remains:

```text
FDA
TFDA
ClinicalTrials.gov
```

This is a deliberate MVP subset, not the full original source scope.

Do not add EMA, NMPA/CDE, PMDA, EU CTIS, WHO ICTRP, literature, patent, finance, news, company alias database, corporate-family mapping, product ownership inference, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, `.mcp.json`, GitHub automation, tool installation, or other integrations unless explicitly approved.

If the next workstream requires source expansion, first create or update a source feasibility / traceability document. Do not immediately implement connectors.

## Recent relevant PR sequence

### PR #97–#103 — Regulatory-clinical digest/report docs-spec workstream

Completed a controlled PM/RA digest/report documentation workstream.

### PR #104–#112 — CMC submission readiness docs/spec workstream

Completed a controlled CMC readiness extension. The current decision remains:

```text
Do not create docs/cmc_management_weekly_report_template.md at this time.
```

### PR #113–#115 — Original requirements calibration, traceability, and state sync

Completed a controlled re-anchoring sequence:

```text
PROJECT_STATE_CONTINUATION.md
docs/original_requirements_traceability_matrix.md
README.md
.ai/PROJECT_STATE.md
```

### PR #116 — Open-source Claude/Codex/MCP tool survey

Completed a docs/spec-only tool survey:

```text
docs/open_source_claude_codex_tool_survey.md
README.md
tests/test_readme_documentation_index.py
```

Important decision:

```text
The survey does not authorize installing, integrating, or configuring any tool.
```

## Current guardrails

- Keep MVP source scope limited to FDA, TFDA, and ClinicalTrials.gov unless source expansion is explicitly approved.
- Keep future work small and phase-controlled.
- Use Traditional Chinese for user-facing discussion.
- Avoid accidental Japanese output.
- After repeated related PRs, pause for direction calibration before continuing.
- The repo is not a GMP, QA, EDMS, eCTD publishing, official submission, clinical decision support, legal decision, medical decision, commercial intelligence, or management decision system.
- Do not store confidential, signed, GMP raw, QA-approved, official submission, vendor confidential, or non-public company records in this repo.
- If validation is requested, use Claude Code Web or Codex Web first due to Codespaces quota limits.
- If asking Claude Code/Codex only to validate, explicitly instruct: do not modify files, do not commit, do not create branch, do not create PR.

## Recommended immediate next step

Recommended next action:

```text
Create a docs/spec-only source expansion feasibility matrix for EMA/NMPA/PMDA before implementing any connector or runtime source expansion.
```

Recommended scope:

```text
1. Compare EMA, NMPA/CDE, and PMDA official source options.
2. Identify official API/RSS/open-data availability where applicable.
3. Capture licensing and access limitations.
4. Define what evidence would be needed before activating each source.
5. Preserve MVP runtime scope as FDA, TFDA, and ClinicalTrials.gov until explicit approval.
```

Do not implement EMA/NMPA/PMDA connectors unless the user explicitly approves source expansion after reviewing the feasibility matrix.
