# Project State Continuation

Created: 2026-06-04  
Updated: 2026-06-12 (post PR #141)

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`

This file is the compact continuation handoff for starting a new chat. Canonical detailed status remains in `.ai/PROJECT_STATE.md`, while this file should be read first when resuming the project in a fresh conversation.

## Current checkpoint

- Stable branch: `main`
- Latest confirmed merged PR: PR #141
- Latest main merge commit: `930d3378f2d74821a193cdeabcfeb4dee8eced53`
- Current tagged release: remains `v0.2.15-fda-abuse-detection-source-failure-diagnostics`; no new release tag has been created for PR #97–#141 docs/product/test/runtime workflow work.
- Latest validation status: `PASS`
- Latest validation evidence for PR #141 main validation baseline:
  - `python -m pytest tests/test_mvp_dashboard_export_fixture.py -q` → `12 passed`
  - `python -m pytest tests/test_mvp_runtime_hardening.py -q` → `28 passed`
  - `python -m pytest tests/test_mvp_runtime_output_contract_semantics.py -q` → `11 passed`
  - `python -m pytest -q` → `270 passed`
  - `git diff --check` → clean
  - `git status --short` → clean / no output after commit
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

Dashboard work remains phase-controlled. PR #141 added a fixture-only, manual dashboard export artifact prototype, but it does not authorize live-source ingestion, a runtime dashboard renderer, scheduling, persistence, GitHub Actions, HTTP/SSE, GitHub Pages, new MCP tools, new source connectors, or source expansion.

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

Current rough alignment after PR #141:

```text
Original Regulatory / Clinical Intelligence MCP system: about 58–62% complete
Project governance / GitHub + Claude/Codex workflow foundation: about 78–80% complete
Dashboard target architecture / schema / query-filter / dry-run / mock examples foundation: about 60–65% complete
MVP runtime output contract / source-state hardening: about 63–68% complete
ClinicalTrials.gov query parameter validation hardening: complete for MVP phase/status/page_size inputs
MVP dashboard export artifact prototype: fixture-only manual prototype complete
CMC readiness extension module: about 75% complete
Overall build-stage system: about 68–72% complete
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
- The repo now includes a small runtime fix for ClinicalTrials.gov query parameter validation.
- `search_clinical_trials_by_indication()` now normalizes `phase` and `status` string inputs into single-item lists before calling the client.
- `phase` / `status` strings are no longer passed as iterable character sequences to the ClinicalTrials.gov query builder.
- `page_size` is now validated at the tool layer using the MVP policy `1 <= page_size <= 100`.
- Invalid `phase`, `status`, or `page_size` inputs return structured `INVALID_PARAMETER` errors and do not call the client.
- The repo now includes the first fixture-only MVP dashboard export artifact prototype.
- The prototype can manually export five dashboard artifacts:
  - `dashboard_snapshot.json`
  - `dashboard_summary.md`
  - `regulatory_updates.csv`
  - `clinical_trials.csv`
  - `source_health.json`
- The exporter is fixture/mock-data-only and does not call live FDA, TFDA, or ClinicalTrials.gov sources.
- The exporter preserves source-unavailable and partial-result caveats instead of collapsing them into no matching records.
- The exporter strips forbidden non-MVP inference fields from output artifacts.
- Clinical trial sponsor/company values remain registry-reported only; no alias, ownership, or corporate-family inference is applied.
- This prototype does not authorize GitHub Actions, scheduler, persistence, HTTP/SSE, GitHub Pages, runtime dashboard renderer, new MCP tools, new source connectors, or source expansion.
- Candidate B, `compare_regulatory_updates(source_types=...)`, remains unresolved and should be handled later through characterization/spec clarification.
- EMA, NMPA/CDE, PMDA, and ICH are not active MVP runtime sources.
- Scheduler, alerts, persistence, runtime dashboard renderer, GitHub Actions, GitHub Pages, HTTP/SSE, and multi-source runtime automation are not implemented.

## Current MVP source scope and deliberate limitation

Approved MVP v1 active source scope remains:

```text
FDA
TFDA
ClinicalTrials.gov
```

This is a deliberate MVP subset, not the full original source/guidance scope.

Do not add EMA, NMPA/CDE, PMDA, ICH, EU CTIS, WHO ICTRP, literature, patent, finance, news, company alias database, corporate-family mapping, product ownership inference, scheduler, alerts, persistence, dashboard renderer, HTTP/SSE transport, GitHub Pages, `.mcp.json`, GitHub automation, tool installation, or other integrations unless explicitly approved.

PR #141 approved only a fixture/mock-data-only, manual dashboard export artifact prototype. Do not connect it to live source ingestion, scheduled automation, persistence, HTTP/SSE, GitHub Pages, a runtime dashboard renderer, new MCP tools, new source connectors, or source expansion unless explicitly approved.

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

### PR #139 — ClinicalTrials.gov query parameter validation

Summary:

* Updated `src/mcp_server/tools_clinical_trials.py`.
* Updated `tests/test_mvp_runtime_hardening.py`.
* Small runtime fix for existing MVP ClinicalTrials.gov tool behavior.
* Adds tool-layer validation for `page_size`.
* Normalizes `phase` and `status` inputs before calling `ClinicalTrialsGovClient.search_studies`.
* Prevents `phase="PHASE2"` and `status="RECRUITING"` from being treated as iterable character sequences.
* Returns structured `INVALID_PARAMETER` errors for invalid `page_size`, `phase`, or `status`.
* Adds regression tests using a fake client to verify normalized parameters and invalid-input behavior.

Merge commit:

```text
317663d1cbea6cb26035e8e199f2125619d85bbd
```

Validation evidence:

* `python -m pytest tests/test_mvp_runtime_hardening.py -q` → `28 passed`
* `python -m pytest tests/test_mvp_runtime_output_contract_semantics.py -q` → `11 passed`
* `python -m pytest -q` → `258 passed`
* `git diff --check` → passed
* `git status --short` → clean / no output

Important decision:

* This PR does not authorize new sources, new MCP tools, dashboard runtime implementation, static artifact generation, scheduling, alerts, persistence, HTTP/SSE, `.mcp.json`, GitHub Actions workflow, source expansion, company alias mapping, corporate-family mapping, product ownership inference, clinical success scoring, approval probability scoring, commercial strength scoring, or CMC weekly management report template.
* `compare_regulatory_updates(source_types=...)` remains a separate candidate issue and was not changed in PR #139.

### PR #141 — MVP dashboard export artifact prototype

Summary:

* Added `src/dashboard_export/__init__.py`.
* Added `src/dashboard_export/mvp_fixture_export.py`.
* Added `tests/fixtures/dashboard_mvp_fixture.json`.
* Added `tests/test_mvp_dashboard_export_fixture.py`.
* Adds the first fixture-only, manual-execution dashboard artifact prototype.
* Exports:
  * `dashboard_snapshot.json`
  * `dashboard_summary.md`
  * `regulatory_updates.csv`
  * `clinical_trials.csv`
  * `source_health.json`
* Uses fictional/mock fixture records only.
* Does not call live FDA, TFDA, or ClinicalTrials.gov sources.
* Preserves source unavailable and partial-result caveats.
* Strips forbidden inference fields including approval probability, clinical success score, commercial strength score, product ownership, company alias, and corporate-family fields.
* Keeps ClinicalTrials.gov sponsor/company values registry-reported only.
* Provides CLI usage:

```bash
python -m src.dashboard_export.mvp_fixture_export --out /tmp/dashboard_mvp
```

Merge commit:

```text
930d3378f2d74821a193cdeabcfeb4dee8eced53
```

Validation evidence:

* `python -m pytest tests/test_mvp_dashboard_export_fixture.py -q` → `12 passed`
* `python -m pytest tests/test_mvp_runtime_hardening.py -q` → `28 passed`
* `python -m pytest tests/test_mvp_runtime_output_contract_semantics.py -q` → `11 passed`
* `python -m pytest -q` → `270 passed`
* `git diff --check` → clean
* `git status --short` → clean after commit

Important decision:

* This PR provides a dashboard artifact prototype, not a runtime dashboard renderer.
* This PR does not authorize live-source ingestion, GitHub Actions, scheduler, alerts, persistence, HTTP/SSE, GitHub Pages, `.mcp.json`, new MCP tools, new source connectors, source expansion, company alias mapping, corporate-family mapping, product ownership inference, clinical success scoring, approval probability scoring, commercial strength scoring, or CMC weekly management report template.

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

Before adding live source ingestion or GitHub Actions, validate the fixture-only dashboard export artifacts and decide the next gate:
1. add fixture artifact acceptance tests / snapshots,
2. connect exporter to existing MVP runtime outputs manually,
3. or perform focused characterization assessment for `compare_regulatory_updates(source_types=...)`.

Current recommendation:

```text
Option 1 — Validate fixture-only dashboard export artifacts before live-source or scheduler work.
```

Rationale:

- Dashboard docs/spec now has a coherent foundation: target architecture, schema families, query/filter contract, static dry-run design, mock records/acceptance criteria, and a fixture-only manual artifact prototype.
- The repo is still in build-stage and should be evaluated across the entire architecture, including `src/`, `tests/`, `docs/`, `workflows/`, `README.md`, `CLAUDE.md`, `AGENTS.md`, `.ai/PROJECT_STATE.md`, and this continuation file.
- The MVP runtime hardening test-only PR (#133), dashboard query/filter contract (#135), MVP runtime output contract semantics tests (#137), ClinicalTrials.gov validation hardening (#139), and fixture-only MVP dashboard export artifact prototype (#141) are now complete without authorizing live-source ingestion or runtime dashboard implementation.
- Validating fixture-only artifacts is the safest next gate before any live-source, scheduler, or automation work.

Do not implement live source ingestion, GitHub Actions, dashboard renderer, scheduler, alerts, persistence, HTTP/SSE, GitHub Pages, new MCP tools, new source connectors, or source expansion unless the user explicitly approves those runtime changes.

Candidate B, `compare_regulatory_updates(source_types=...)`, remains unresolved and should be handled later through characterization/spec clarification before runtime changes.

## New chat kickoff prompt

Use the following prompt when starting a new conversation:

```text
請根據 GitHub repo `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`、`.ai/PROJECT_STATE.md`、以及 `PROJECT_STATE_CONTINUATION.md` 繼續。

請用繁體中文回覆，不要輸出日文。

請先確認：
1. `main` 是否已包含 PR #141；
2. `PROJECT_STATE_CONTINUATION.md` 是否已記錄 PR #141 和 270-passed validation baseline；
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
- PR #139 — ClinicalTrials.gov query parameter validation and 258-passed validation baseline
- PR #141 — MVP dashboard export artifact prototype and 270-passed validation baseline

目前建議下一步是先 validate fixture-only dashboard export artifacts，或決定下一個受控 gate：

- validate fixture-only dashboard export artifacts
- or decide whether to connect exporter to existing MVP runtime outputs manually
- or focused characterization assessment for `compare_regulatory_updates(source_types=...)`

除非我明確批准，不要新增 runtime dashboard renderer、GitHub Actions workflow、scheduler、alerts、persistence、HTTP/SSE、`.mcp.json`、new MCP tool、new source connector、EMA/NMPA/PMDA/ICH connectors、WHO ICTRP、EU CTIS、literature/patent/finance/news integration、company alias database、corporate-family mapping、product ownership inference、clinical success scoring、approval probability scoring、commercial strength scoring、CMC weekly management report template。

如果要改 repo，請維持小 PR、明確 scope、先提供 validation 指令。若 merge 或 fetch GitHub main 被工具、網路或系統擋一次，請停止重試並請我手動處理。
```
