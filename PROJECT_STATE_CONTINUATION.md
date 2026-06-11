# Project State Continuation

Created: 2026-06-04  
Updated: 2026-06-10

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`

This file is a compact continuation handoff for starting a new chat. Canonical detailed status remains in `.ai/PROJECT_STATE.md`.

## Current checkpoint

- Stable branch: `main`
- Latest confirmed merged PR: PR #125
- PR #120 merge commit: `b1ec886fa5fa4b9a8a0c7c6237334e0cc581e63b`
- PR #122 merge commit: `d32099f16a2b9f0b91268b7e01c7ca227db74675`
- PR #124 merge commit: `116c648dfc195d60f9c05f375e205ebbf24d3b54`
- PR #125 merge commit: `4aa607dcc577eb714aef237b01213cbff88cf4a9`
- Latest completed workstream: dashboard-first target architecture, canonical dashboard schema contract, and mock-data-only static dashboard dry-run design.
- Latest validation status: `PASS`
- Latest validation evidence for PR #125:
  - `python -m pytest tests/test_readme_documentation_index.py -q` → `15 passed`
  - `python -m pytest tests/test_project_state_release_tag_consistency.py -q` → `5 passed`
  - `python -m pytest -q` → `217 passed`
  - `git status --short` → clean / no output
- Current tagged release: remains `v0.2.15-fda-abuse-detection-source-failure-diagnostics`; no new release tag was created for PR #97–#125 docs/product workflow work.
- Execution environment note: Codespaces quota is near limit until July 2026. For upcoming code/test work, default to Claude Code Web and Codex Web workflows. Do not assume Codespaces is available unless the user explicitly says it is available again.

## Original user requirement baseline

The project is in build-stage and must be evaluated against the user's original full-system requirements, not only the CMC workstream, digest workstream, source-expansion planning, or dashboard documentation.

Original target system:

1. Build a GitHub-based system architecture where project and code construction happen in Codex/GitHub, then the final usable knowledge/workflow is moved into Claude Project for execution.
2. Track updates from FDA, EMA, TFDA, NMPA, PMDA, and high-priority harmonised guidance sources such as ICH, including dates and official document links, over date windows from 1 month to 5 years.
3. Support regulatory/guidance retrieval by biologic product modality or guidance topic.
4. Track clinical trial progress and results by indication and sponsor/company, preferably using official registry APIs.
5. Detect source, webpage, API, or parser changes and support correction through source-health diagnostics before any future notification design.
6. Prefer official APIs where available and use MCP-based retrieval.
7. Evaluate open-source or openly documented tools that can support Claude/Codex for at least one original-system function.
8. Preserve the longer-term dashboard / dashboard-artifact goal, but implement it only through controlled docs/spec steps until runtime work is explicitly approved.

## Current alignment to original requirements

Current rough alignment after PR #125:

```text
Original Regulatory / Clinical Intelligence MCP system: about 54–58% complete
Project governance / GitHub + Claude/Codex workflow foundation: about 77–79% complete
Dashboard target architecture / schema / dry-run foundation: about 42–47% complete
CMC readiness extension module: about 75% complete
Overall build-stage system: about 63–67% complete
```

Interpretation:

- The repo has a useful MVP regulatory-clinical intelligence subset using FDA, TFDA, and ClinicalTrials.gov.
- The repo has a useful CMC readiness docs/spec extension.
- The repo has an original requirements traceability matrix.
- The repo has a docs/spec-only open-source Claude/Codex/MCP tool survey.
- The repo has a docs/spec-only EMA/NMPA/PMDA/ICH source and guidance expansion feasibility matrix.
- The repo has a dashboard-first target architecture contract.
- The repo has canonical dashboard data schema families.
- The repo has a mock-data-only static dashboard dry-run design.
- EMA, NMPA/CDE, PMDA, and ICH are not active MVP runtime sources.
- Scheduler, alerts, persistence, runtime dashboard, static artifact generator, GitHub Actions, and multi-source runtime automation are not implemented.

## Current MVP source scope and deliberate limitation

Approved MVP v1 active source scope remains:

```text
FDA
TFDA
ClinicalTrials.gov
```

This is a deliberate MVP subset, not the full original source/guidance scope.

Do not add EMA, NMPA/CDE, PMDA, ICH, EU CTIS, WHO ICTRP, literature, patent, finance, news, company alias database, corporate-family mapping, product ownership inference, scheduler, alerts, persistence, dashboard renderer, static artifact generator, HTTP/SSE transport, `.mcp.json`, GitHub automation, tool installation, or other integrations unless explicitly approved.

If the next workstream involves dashboard work, keep it docs/spec-only unless runtime dashboard implementation or artifact generation is explicitly approved.

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

### PR #117 — State sync after tool survey

Updated project state/handoff files after PR #116.

### PR #118 — EMA/NMPA/PMDA/ICH source and guidance expansion feasibility matrix

Completed a docs/spec-only source/guidance feasibility matrix:

```text
docs/source_expansion_feasibility_matrix_ema_nmpa_pmda.md
README.md
tests/test_readme_documentation_index.py
```

Important decisions:

```text
EMA, NMPA/CDE, and PMDA are regulatory agency / regulator-linked source candidates.
ICH is a global harmonisation guidance source, not a drug-review agency and not a clinical trial registry.
PR #118 does not authorize implementing any connector or runtime source/guidance expansion.
```

### PR #119 — State sync after PR #118

Updated project state/handoff files after PR #118.

### PR #120 — Dashboard target architecture contract

Completed a docs/spec-only dashboard target architecture contract:

```text
docs/dashboard_target_architecture.md
README.md
tests/test_readme_documentation_index.py
.ai/PROJECT_STATE.md
```

Important decisions:

```text
Dashboard-first, source-expansion-later.
No runtime dashboard renderer.
No GitHub Actions workflow.
No scheduler, alerts, persistence, runtime connector, MCP tool, or .mcp.json changes.
```

Validation evidence:

```text
tests/test_project_state_release_tag_consistency.py -> 5 passed
tests/test_readme_documentation_index.py -> 13 passed
python -m pytest -q -> 215 passed
git status --short -> clean / no output
```

### PR #122 — Canonical dashboard data schema contract

Completed a docs/spec-only dashboard data schema contract:

```text
docs/dashboard_data_schema_contract.md
README.md
tests/test_readme_documentation_index.py
```

Defined canonical schema families:

```text
RegulatoryGuidanceUpdate
ClinicalTrialUpdate
SourceHealthEvent
DashboardDigestSummary
```

Important decisions:

```text
Defines dashboard schema contracts only.
No runtime dashboard renderer.
No artifact generator.
No GitHub Actions workflow.
No scheduler, alerts, persistence, runtime connector, MCP tool, source expansion, or .mcp.json changes.
```

Validation evidence:

```text
python -m pytest tests/test_readme_documentation_index.py tests/test_project_state_release_tag_consistency.py -q -> 19 passed
python -m pytest -q -> 216 passed
git status --short -> clean / no output
```

### PR #124 — State sync after dashboard schema contract

Updated project state/handoff files after PR #120 and PR #122.

### PR #125 — Static dashboard dry-run design

Completed a docs/spec-only mock-data-only static dashboard dry-run design:

```text
docs/static_dashboard_dry_run_design.md
README.md
tests/test_readme_documentation_index.py
```

Defined intended dashboard tabs:

```text
Overview
Regulatory / Guidance Updates
Clinical Trial Tracker
Source Health
Digest Summary
```

Important decisions:

```text
Defines static dashboard dry-run design only.
No runtime dashboard renderer.
No static artifact generator.
No GitHub Actions workflow.
No scheduler, alerts, persistence, runtime connector, MCP tool, source expansion, or .mcp.json changes.
```

Validation evidence:

```text
python -m pytest tests/test_readme_documentation_index.py -q -> 15 passed
python -m pytest tests/test_project_state_release_tag_consistency.py -q -> 5 passed
python -m pytest -q -> 217 passed
git status --short -> clean / no output
```

## Current guardrails

- Keep MVP runtime source scope limited to FDA, TFDA, and ClinicalTrials.gov unless source/guidance expansion is explicitly approved.
- Keep future work small and phase-controlled.
- Use Traditional Chinese for user-facing discussion.
- Avoid accidental Japanese output.
- Give complete copy-paste validation command blocks; do not tell the user only to switch branches without exact commands.
- If merge is blocked by system/tooling once, stop retrying and ask the user to merge manually with clear instructions.
- After repeated related PRs, pause for direction calibration before continuing.
- The repo is not a GMP, QA, EDMS, eCTD publishing, official submission, clinical decision support, legal decision, medical decision, commercial intelligence, or management decision system.
- Do not store confidential, signed, GMP raw, QA-approved, official submission, vendor confidential, or non-public company records in this repo.
- If validation is requested, use Claude Code Web or Codex Web first due to Codespaces quota limits.
- If asking Claude Code/Codex only to validate, explicitly instruct: do not modify files, do not commit, do not create branch, do not create PR.
- If the user explicitly confirms merge/approval, do not repeatedly ask for the same confirmation. Perform at most one verification pass when needed, then proceed.

## Recommended immediate next step

Recommended next action after this state sync:

```text
Direction calibration before adding mock dashboard record examples or static artifact acceptance tests.
```

Recommended calibration options:

```text
1. Add mock dashboard record examples and static artifact acceptance tests, still docs/spec-only.
2. Pause dashboard docs and return to MVP runtime hardening.
3. Revisit source/guidance expansion feasibility sequencing without implementing connectors.
4. Stop new PRs until the user explicitly selects one direction.
```

Do not implement EMA/NMPA/PMDA/ICH connectors, GitHub Actions, dashboard renderer, artifact generator, scheduler, alerts, persistence, source expansion, new MCP tools, or `.mcp.json` changes unless the user explicitly approves those runtime changes.
