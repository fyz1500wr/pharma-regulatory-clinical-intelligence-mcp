# Project State Continuation

Created: 2026-06-04  
Updated: 2026-06-12

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`

This file is the compact continuation handoff for starting a new chat. Canonical detailed status remains in `.ai/PROJECT_STATE.md`, while this file should be read first when resuming the project in a fresh conversation.

## Current checkpoint

- Stable branch: `main`
- Latest confirmed merged PR: PR #137
- Latest main merge commit: `65d276de8dbf55618954887306055a418091c76e`
- Current tagged release: remains `v0.2.15-fda-abuse-detection-source-failure-diagnostics`; no new release tag has been created for PR #97–#137 docs/product/test workflow work.
- Latest validation status: `PASS`
- Latest validation evidence for PR #137 main validation baseline:
  - `python -m pytest tests/test_mvp_runtime_output_contract_semantics.py -q` → `11 passed`
  - `python -m pytest tests/test_mvp_runtime_hardening.py -q` → `18 passed`
  - `python -m pytest tests/test_project_state_release_tag_consistency.py -q` → `5 passed`
  - `python -m pytest -q` → `248 passed`
  - `git status --short` → clean / no output
- Execution environment note: Codespaces quota is near limit until July 2026. For upcoming validation or code/test work, default to Claude Code Web and Codex Web workflows unless the user explicitly says Codespaces is available again.

## Major direction change to preserve

This project has undergone a major direction adjustment. It should no longer be treated only as a narrow MVP source-ingestion repo, a CMC readiness extension, or a digest-memo workflow repo.

The project is now in a **dashboard-first build-stage architecture phase**.

The intended system should be considered across the whole repository architecture, including:

```text
PROJECT_INSTRUCTION.md
CLAUDE.md
AGENTS.md
README.md
.ai/PROJECT_STATE.md
PROJECT_STATE_CONTINUATION.md
docs/*.md
workflows/*.md
tests/*.py
src/*
```

The current priority is to keep the project aligned with the original full-system goal:

```text
Regulatory / guidance / clinical-trial intelligence system
→ source-aware normalization
→ schema contracts
→ dashboard-oriented intelligence outputs
→ Claude Project / MCP-assisted analysis
```

Dashboard work must remain docs/spec-only until the user explicitly approves runtime implementation.

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

Current rough alignment after PR #137:

```text
Original Regulatory / Clinical Intelligence MCP system: about 56–60% complete
Project governance / GitHub + Claude/Codex workflow foundation: about 78–80% complete
Dashboard target architecture / schema / query-filter / dry-run / mock examples foundation: about 52–56% complete
MVP runtime output contract / source-state hardening: about 60–65% complete
CMC readiness extension module: about 75% complete
Overall build-stage system: about 66–70% complete
```

Interpretation:

- The repo has a useful MVP regulatory-clinical intelligence subset using FDA, TFDA, and ClinicalTrials.gov.
- The repo has a useful CMC readiness docs/spec extension.
- The repo has an original requirements traceability matrix.
- The repo has a docs/spec-only open-source Claude/Codex/MCP tool survey.
- The repo has a docs/spec-only EMA/NMPA/PMDA/ICH source and guidance expansion feasibility matrix.
- The repo has a dashboard-first target architecture contract.
- The repo has canonical dashboard data schema families.
- The repo has a docs/spec-only dashboard query/filter contract mapping MVP runtime outputs to future dashboard filters and row fields.
- The repo has a mock-data-only static dashboard dry-run design.
- The repo has fictional mock dashboard record examples and static artifact acceptance criteria.
- The repo now has test-only MVP runtime output contract semantics coverage.
- The repo now locks no-result vs source-unavailable distinction for regulatory and clinical search outputs.
- The repo now locks partial-failure metadata for regulatory comparison and document detail.
- The repo now locks digest source-error preservation and non-inference guardrails for clinical/company/digest outputs.
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

### PR #128 — Mock dashboard record examples and static artifact acceptance criteria

Completed a docs/spec-only mock dashboard record examples and static artifact acceptance criteria contract:

```text
docs/mock_dashboard_record_examples.md
README.md
tests/test_readme_documentation_index.py
```

Defined fictional mock examples for:

```text
RegulatoryGuidanceUpdate
ClinicalTrialUpdate
SourceHealthEvent
DashboardDigestSummary
```

Important decisions:

```text
Defines mock dashboard examples and acceptance criteria only.
No runtime dashboard renderer.
No static artifact generator.
No GitHub Actions workflow.
No scheduler, alerts, persistence, runtime connector, MCP tool, source expansion, or .mcp.json changes.
```

Validation evidence:

```text
python -m pytest tests/test_readme_documentation_index.py -q -> 16 passed
python -m pytest tests/test_project_state_release_tag_consistency.py -q -> 5 passed
python -m pytest -q -> 218 passed
git status --short -> clean / no output
```

### PR #130 — State sync after mock dashboard record examples

Updated:

```text
.ai/PROJECT_STATE.md
PROJECT_STATE_CONTINUATION.md
```

Merge commit:

```text
f38fc53c9248925688a4f0e5986772c78aecef47
```

Validation evidence:

```text
python -m pytest tests/test_project_state_release_tag_consistency.py -q -> 5 passed in 0.03s
python -m pytest -q -> 218 passed in 5.27s
git status --short -> clean / no output
```

### PR #133 — MVP runtime hardening contract tests

Summary:

* Added `tests/test_mvp_runtime_hardening.py`
* Test-only runtime hardening PR
* No production code changes
* Locks down existing MVP runtime contract behavior for the current 8 MCP tools
* Verifies source-unavailable is not treated as no records
* Verifies non-MVP sources are rejected conservatively
* Verifies digest output preserves `source_errors` and known limitations
* Verifies clinical trial and company comparison outputs do not expose approval probability, clinical success, commercial strength, product ownership, alias, or corporate-family inference fields

Merge commit:

```text
98ef655a768f54f37369c20f4eb505c5bae4c32d
```

Validation evidence:

* `python -m pytest tests/test_mvp_runtime_hardening.py -q` → `18 passed in 0.10s`
* `python -m pytest -q` → `236 passed in 3.85s`
* `python -m pytest tests/test_project_state_release_tag_consistency.py -q` → `5 passed in 0.02s`
* `python -m pytest tests/test_readme_documentation_index.py -q` → `16 passed in 0.02s`
* `git status --short` → clean / no output

Important decision:

* This PR does not authorize new sources, new MCP tools, dashboard runtime implementation, static artifact generation, scheduling, alerts, persistence, HTTP/SSE, `.mcp.json`, or source expansion.

### PR #135 — Dashboard query/filter contract

Summary:

* Added `docs/dashboard_query_filter_contract.md`.
* Updated `README.md` Post-MVP Documentation Index.
* Updated `tests/test_readme_documentation_index.py` with the new expected entry and row-specific assertion.
* Defines docs/spec-only mapping from existing MVP runtime MCP outputs to future dashboard query/filter behavior.
* Establishes MVP active filter boundary for FDA, TFDA, and ClinicalTrials.gov only.
* Defines display rules for source unavailable versus no matching records, missing metadata, sponsor/company caveats, and no inference of clinical success, approval probability, commercial strength, product ownership, alias, or corporate-family relationships.

Merge commit:

```text
1b9cca67e46f71cab9a5a333f40984756d257676
```

Validation evidence:

* `python -m pytest tests/test_readme_documentation_index.py tests/test_project_state_release_tag_consistency.py -q` → `22 passed`
* `python -m pytest -q` → `237 passed`
* `git status --short` → clean / no output

Important decision:

* This PR does not authorize runtime dashboard rendering, static artifact generation, GitHub Actions workflow, scheduler, alerts, persistence, HTTP/SSE, `.mcp.json`, new MCP tools, source connectors, or source expansion.

### PR #137 — MVP runtime output contract semantics tests

Summary:

* Added `tests/test_mvp_runtime_output_contract_semantics.py`.
* Test-only runtime output contract semantics PR.
* No production code changes.
* Locks the exact approved 8-tool MVP registry.
* Verifies `NO_MATCHING_RECORDS` is not conflated with `SOURCE_UNAVAILABLE`.
* Verifies partial-failure metadata is preserved for regulatory comparison and document detail.
* Verifies company comparison treats unavailable sources as not evaluable rather than zero activity.
* Verifies digest output preserves `query_metadata.source_errors` and conservative zero-update limitations.
* Recursively verifies clinical search, company comparison, and digest outputs do not expose non-MVP inference fields such as approval probability, clinical success, commercial strength, product ownership, company alias, corporate-family relationship, or ownership inference.

Merge commit:

```text
65d276de8dbf55618954887306055a418091c76e
```

Validation evidence:

* `python -m pytest tests/test_mvp_runtime_output_contract_semantics.py -q` → `11 passed`
* `python -m pytest tests/test_mvp_runtime_hardening.py -q` → `18 passed`
* `python -m pytest tests/test_project_state_release_tag_consistency.py -q` → `5 passed`
* `python -m pytest -q` → `248 passed`
* `git status --short` → clean / no output

Important decision:

* This PR does not authorize runtime dashboard rendering, static artifact generation, GitHub Actions workflow, scheduler, alerts, persistence, HTTP/SSE, `.mcp.json`, new MCP tools, source connectors, or source expansion.

## Current guardrails

- Use Traditional Chinese for user-facing discussion.
- Avoid accidental Japanese output.
- Keep MVP runtime source scope limited to FDA, TFDA, and ClinicalTrials.gov unless source/guidance expansion is explicitly approved.
- Keep future work small and phase-controlled.
- Give complete copy-paste validation command blocks; do not tell the user only to switch branches without exact commands.
- If merge is blocked by system/tooling once, stop retrying and ask the user to merge manually with clear instructions.
- After repeated related PRs, pause for direction calibration before continuing.
- The repo is not a GMP, QA, EDMS, eCTD publishing, official submission, clinical decision support, legal decision, medical decision, commercial intelligence, or management decision system.
- Do not store confidential, signed, GMP raw, QA-approved, official submission, vendor confidential, or non-public company records in this repo.
- If validation is requested, use Claude Code Web or Codex Web first due to Codespaces quota limits.
- If asking Claude Code/Codex only to validate, explicitly instruct: do not modify files, do not commit, do not create branch, do not create PR.
- If the user explicitly confirms merge/approval, do not repeatedly ask for the same confirmation. Perform at most one verification pass when needed, then proceed.

## Recommended immediate next step

Before opening more PRs, perform direction calibration.

Recommended calibration options:

```text
1. Continue docs/spec-only dashboard artifact planning.
2. Pause dashboard docs and return to MVP runtime hardening.
3. Revisit source/guidance expansion feasibility sequencing without implementing connectors.
4. Stop new PRs until the user explicitly selects one direction.
```

Current recommendation:

```text
Option 2 — Pause dashboard docs and return to MVP runtime hardening.
```

Rationale:

- Dashboard docs/spec now has a coherent foundation: target architecture, schema families, query/filter contract, static dry-run design, and mock records/acceptance criteria.
- The repo is still in build-stage and should be evaluated across the entire architecture, including `src/`, `tests/`, `docs/`, `workflows/`, `README.md`, `CLAUDE.md`, `AGENTS.md`, `.ai/PROJECT_STATE.md`, and this continuation file.
- The MVP runtime hardening test-only PR (#133), dashboard query/filter contract (#135), and MVP runtime output contract semantics tests (#137) are now complete without authorizing runtime dashboard implementation.
- MVP runtime hardening is likely more valuable than adding more dashboard documents immediately.

Do not implement the next candidate runtime fixes in this state-only PR. Candidate directions for later calibration include small runtime fix assessment for clinical trial query parameter validation and `compare_regulatory_updates` source_types behavior clarification. Do not implement EMA/NMPA/PMDA/ICH connectors, GitHub Actions, dashboard renderer, artifact generator, scheduler, alerts, persistence, source expansion, new MCP tools, or `.mcp.json` changes unless the user explicitly approves those runtime changes.

## New chat kickoff prompt

Use the following prompt when starting a new conversation:

```text
請根據 GitHub repo `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`、`.ai/PROJECT_STATE.md`、以及 `PROJECT_STATE_CONTINUATION.md` 繼續。

請用繁體中文回覆，不要輸出日文。

請先確認：
1. `main` 是否已包含 PR #137；
2. `PROJECT_STATE_CONTINUATION.md` 是否已記錄 PR #137 和 248-passed validation baseline；
3. 是否有 open PR，若有，先判斷是否為 stale duplicate，不要直接 merge；
4. 最新測試狀態；
5. 是否需要先做 direction calibration。

目前專案是在建置階段，不要只看單一功能或單一 md 檔。請全盤考慮 repo 內所有架構與狀態檔案，包括但不限於：

- `PROJECT_INSTRUCTION.md`
- `CLAUDE.md`
- `AGENTS.md`
- `README.md`
- `.ai/PROJECT_STATE.md`
- `PROJECT_STATE_CONTINUATION.md`
- `docs/*.md`
- `workflows/*.md`
- `tests/*.py`
- `src/*`

目前 dashboard-first / MVP runtime foundation 文件與測試基礎已完成：

- PR #120 — dashboard target architecture contract
- PR #122 — dashboard data schema contract
- PR #125 — static dashboard dry-run design
- PR #128 — mock dashboard record examples and static artifact acceptance criteria
- PR #130 — state sync after mock dashboard record examples
- PR #133 — MVP runtime hardening contract tests and 236-passed validation baseline
- PR #135 — dashboard query/filter contract and 237-passed validation baseline
- PR #137 — MVP runtime output contract semantics tests and 248-passed validation baseline

目前建議下一步是先做 direction calibration，優先考慮：

`Option 2 — Pause dashboard docs and return to MVP runtime hardening`

除非我明確批准，不要新增 runtime dashboard renderer、static artifact generator、GitHub Actions workflow、scheduler、alerts、persistence、HTTP/SSE、`.mcp.json`、new MCP tool、EMA/NMPA/PMDA/ICH connectors、WHO ICTRP、EU CTIS、literature/patent/finance/news integration、company alias database、corporate-family mapping、product ownership inference、clinical success scoring、approval probability scoring、commercial strength scoring、CMC weekly management report template。

如果要改 repo，請維持小 PR、明確 scope、先提供 validation 指令。若 merge 被工具或系統擋一次，請停止重試並請我手動 merge。
```
