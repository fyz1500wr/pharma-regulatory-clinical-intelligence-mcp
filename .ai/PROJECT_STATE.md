# Project State — Pharma Regulatory Clinical Intelligence MCP

Last updated: 2026-06-10

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`
Current stable branch: `main`
Current completed release: `v0.2.15-fda-abuse-detection-source-failure-diagnostics`
Latest post-release main checkpoint: PR #122 canonical dashboard data schema contract after PR #120 dashboard target architecture contract

Latest confirmed main commit:

```text
d32099f16a2b9f0b91268b7e01c7ca227db74675
```

---

## 1. Current Status

The repository remains at completed tagged release `v0.2.15-fda-abuse-detection-source-failure-diagnostics`. No new release tag has been created for the post-release docs/product workflow work after v0.2.15.

After the release baseline, the project completed PM/RA regulatory-clinical digest/report docs-spec work, a clean-source digest dry-run, CMC readiness extension docs, original-requirements calibration, requirements traceability, open-source Claude/Codex/MCP tool survey, EMA/NMPA/PMDA/ICH source and guidance expansion feasibility planning, and then re-anchored to a dashboard-first roadmap through PR #120 and PR #122.

Latest confirmed release tag:

```text
v0.2.15-fda-abuse-detection-source-failure-diagnostics
```

Latest completed dashboard checkpoint:

```text
PR #122 merge commit: d32099f16a2b9f0b91268b7e01c7ca227db74675
```

Latest validation recorded for PR #122:

```bash
git fetch origin
# fetched all remote branches and tags

git checkout dashboard-data-schema-contract
# on branch, already up to date

git pull origin dashboard-data-schema-contract
# already up to date

python -m pip install -e .
# installed successfully; mcp dependency installed in validation environment

python -m pytest tests/test_readme_documentation_index.py tests/test_project_state_release_tag_consistency.py -q
# 19 passed

python -m pytest -q
# 216 passed

git status --short
# clean; no output
```

Validation environment note: PR #122 full-suite validation required the existing `mcp` dependency to be installed in the validation environment. No repository files were modified by dependency installation or validation.

---

## 2. Completed Tagged Release Baseline

### v0.2.15 — FDA abuse-detection source failure diagnostics

PR: #82 Add FDA abuse-detection source failure diagnostics

Main commit: c940a4f70bd3017b02c133712a2e2608baa9e098 Add FDA abuse-detection source failure diagnostics (#82)

Release tag: v0.2.15-fda-abuse-detection-source-failure-diagnostics

Scope:

- Added diagnostics for FDA abuse-detection/apology source failures.
- Preserved FDA source-access limitations as `SOURCE_UNAVAILABLE` rather than `NO_MATCHING_RECORDS`.
- Did not add FDA source bypass or scraping workaround.

Important interpretation:

FDA abuse-detection/apology responses are source-access limitations. They must not be interpreted as evidence that no FDA records or updates exist.

---

## 3. Completed Post-Release Workstreams

### PR #97–#103 — PM/RA regulatory-clinical digest/report docs-spec workstream

Completed controlled PM/RA digest/report documentation artifacts:

```text
docs/regulatory_clinical_digest_report_workflow.md
docs/regulatory_clinical_digest_example_memo.md
docs/regulatory_clinical_digest_prompt_pack.md
docs/regulatory_clinical_digest_memo_validation_exercise.md
docs/regulatory_clinical_digest_report_template_contract.md
docs/regulatory_clinical_digest_clean_source_dry_run.md
```

Status:

- Regulatory-clinical digest memo workflow is usable for controlled PM/RA dry-run memo generation.
- Digest outputs remain working intelligence and require human review.
- No runtime report generator, template renderer, MCP-side report helper, new source, scheduler, dashboard, alert, persistence, HTTP/SSE transport, company alias database, corporate-family mapping, product ownership inference, or literature/patent/finance/news integration was added.

### PR #104–#112 — CMC submission readiness docs-spec extension

Completed controlled CMC readiness extension artifacts:

```text
docs/cmc_submission_readiness_mapping_workflow.md
docs/cmc_submission_readiness_mock_inventory.md
docs/cmc_submission_readiness_input_template.md
```

Status:

- The CMC readiness workflow remains docs/spec-only.
- It supports non-confidential Module 3 gap mapping, vendor follow-up, method/stability dependency review, critical path planning, PM next actions, and mock management summary stress testing.
- Second stress-test result after PR #111: `PASS`.
- Repository action recommendation after the second stress test: `No repo change needed`.
- Do not create `docs/cmc_management_weekly_report_template.md` at this time.

Interpretation:

CMC readiness is a useful extension module, not the original regulatory-clinical intelligence core. It should not keep pulling the repository toward CMC weekly-report documents unless the user explicitly approves that separate workstream.

### PR #113–#115 — Original requirements calibration, traceability, and state sync

Completed controlled re-anchoring artifacts:

```text
PROJECT_STATE_CONTINUATION.md
docs/original_requirements_traceability_matrix.md
README.md
.ai/PROJECT_STATE.md
```

Status:

- Re-anchored the project to the user's original full-system requirements.
- Mapped original requirements to current MVP, extension, missing, and approval-required workstreams.
- Clarified that PR #104–#112 CMC readiness work is extension work, not the original core system.
- Synchronized state/handoff files after PR #114.

### PR #116 — Open-source Claude/Codex tool survey

Added:

```text
docs/open_source_claude_codex_tool_survey.md
```

Also updated:

```text
README.md
tests/test_readme_documentation_index.py
```

Important interpretation:

The survey is a governance/specification artifact. It does not approve tool installation, dependency changes, `.mcp.json`, runtime implementation, new MCP tools, scheduler, alerts, dashboard, persistence, HTTP/SSE transport, GitHub automation, source expansion, or CMC weekly report template work.

### PR #117 — State sync after tool survey

Updated:

```text
.ai/PROJECT_STATE.md
PROJECT_STATE_CONTINUATION.md
```

Status:

- Synchronized project state after PR #116.
- Preserved the post-v0.2.15 release baseline and guardrails.

### PR #118 — EMA/NMPA/PMDA/ICH source and guidance expansion feasibility matrix

Added / updated:

```text
docs/source_expansion_feasibility_matrix_ema_nmpa_pmda.md
README.md
tests/test_readme_documentation_index.py
```

Purpose:

- Provide a docs/spec-only feasibility matrix for future EMA, NMPA/CDE, PMDA, and ICH expansion.
- Classify EMA, NMPA/CDE, and PMDA as regulatory agency / regulator-linked source candidates.
- Classify ICH as a global harmonisation guidance source, not a drug-review agency and not a clinical trial registry.
- Define feasibility ratings, official source evidence, blockers, activation gates, and recommended sequencing.

Important interpretation:

PR #118 is a feasibility/planning artifact only. It does not approve or implement EMA, NMPA/CDE, PMDA, or ICH connectors. It does not add runtime source or guidance expansion, MCP tools, dependencies, `.mcp.json`, scheduler, alerts, dashboard, persistence, HTTP/SSE transport, GitHub automation, literature/patent/finance/news integration, company alias database, corporate-family mapping, product ownership inference, CMC weekly report template, runtime generator, or implementation code.

### PR #119 — State sync after PR #118

Updated:

```text
.ai/PROJECT_STATE.md
PROJECT_STATE_CONTINUATION.md
```

Status:

- Synchronized project state after PR #118.
- Preserved source-expansion guardrails and recommended direction calibration.

### PR #120 — Dashboard target architecture contract

Added / updated:

```text
docs/dashboard_target_architecture.md
README.md
tests/test_readme_documentation_index.py
.ai/PROJECT_STATE.md
```

Merge commit:

```text
b1ec886fa5fa4b9a8a0c7c6237334e0cc581e63b
```

Purpose:

- Re-anchored the project from source-expansion-only planning to the original dashboard intelligence-system target.
- Defined a dashboard-first, source-expansion-later architecture.
- Defined intended dashboard tabs for regulatory/guidance updates, biologic or therapeutic modality view, clinical trial tracker, and source health/source-change monitor.
- Clarified GitHub/Codex, GitHub Actions, MCP, Claude Project, and dashboard artifact roles without implementing any runtime dashboard work.

Validation:

```text
tests/test_project_state_release_tag_consistency.py -> 5 passed
tests/test_readme_documentation_index.py -> 13 passed
python -m pytest -q -> 215 passed
git status --short -> clean / no output
```

Important interpretation:

PR #120 is an architecture contract only. It does not add dashboard renderer, GitHub Actions workflow, scheduler, alerts, GitHub Pages publication, persistence layer, runtime connector, MCP tool, `.mcp.json`, source expansion, literature/patent/finance/news integration, company alias database, corporate-family mapping, product ownership inference, clinical success scoring, approval probability scoring, or CMC weekly management report template.

### PR #122 — Canonical dashboard data schema contract

Added / updated:

```text
docs/dashboard_data_schema_contract.md
README.md
tests/test_readme_documentation_index.py
```

Merge commit:

```text
d32099f16a2b9f0b91268b7e01c7ca227db74675
```

Purpose:

- Defined canonical dashboard schema families:
  - `RegulatoryGuidanceUpdate`
  - `ClinicalTrialUpdate`
  - `SourceHealthEvent`
  - `DashboardDigestSummary`
- Defined shared base fields, date-window values, modality/topic/indication tag contracts, source-health interpretation rules, and storage/artifact boundaries.
- Preserved ICH as a global harmonisation guidance source distinct from regulatory agency and clinical trial registry sources.
- Preserved the MVP runtime source scope: FDA, TFDA, and ClinicalTrials.gov.

Validation:

```text
tests/test_readme_documentation_index.py + tests/test_project_state_release_tag_consistency.py -> 19 passed
python -m pytest -q -> 216 passed
git status --short -> clean / no output
```

Important interpretation:

PR #122 is a schema contract only. It does not add dashboard renderer, GitHub Actions workflow, scheduler, alerts, GitHub Pages publication, persistence layer, runtime connector, new MCP tool, `.mcp.json`, source expansion, literature/patent/finance/news integration, company alias database, corporate-family mapping, product ownership inference, clinical success scoring, approval probability scoring, or CMC weekly management report template.

---

## 4. Current Product Status

Estimated progress against the user's broader target system after PR #122:

```text
Original Regulatory / Clinical Intelligence MCP system: about 52–56% complete
Project governance / GitHub + Claude/Codex workflow foundation: about 76–78% complete
Dashboard target architecture / schema foundation: about 35–40% complete
CMC readiness extension module: about 75% complete
Overall build-stage system: about 61–65% complete
```

What is now working:

- MVP source scope and guardrails are defined.
- FDA / TFDA / ClinicalTrials.gov MVP tools and safety interpretation rules exist.
- Source failure and source limitation wording is controlled.
- Regulatory-clinical digest memo workflow, prompt pack, validation exercise, template contract, and clean-source dry-run exist.
- CMC submission readiness mapping workflow, mock inventory, and input template exist as docs/spec-only extension artifacts.
- Original full-system requirements are recorded and mapped in `docs/original_requirements_traceability_matrix.md`.
- Open-source Claude/Codex/MCP tool candidates are surveyed in `docs/open_source_claude_codex_tool_survey.md`.
- EMA/NMPA/PMDA/ICH source and guidance expansion feasibility is documented in `docs/source_expansion_feasibility_matrix_ema_nmpa_pmda.md`.
- Dashboard-first target architecture is documented in `docs/dashboard_target_architecture.md`.
- Canonical dashboard data schema families are documented in `docs/dashboard_data_schema_contract.md`.

What remains intentionally not implemented:

- Runtime report generator.
- Template renderer.
- MCP-side report generation helper.
- Persistent source-failure event store.
- Runtime dashboard renderer.
- Static dashboard artifact generator.
- Scheduler, alerting, external integration, or GitHub automation.
- Additional runtime source or guidance expansion.
- Official eCTD publishing, EDMS, GMP/QA record, or submission record storage.
- Management decision automation.
- Dedicated `docs/cmc_management_weekly_report_template.md`.

What remains missing or only partial relative to the original full-system target:

- Active EMA, NMPA/CDE, PMDA, or ICH runtime source/guidance coverage.
- Runtime multi-agency source coverage across all original target agencies.
- Dashboard artifact generation and rendering.
- Persistent source-change tracking, scheduler, and notification design.
- Multi-registry clinical trial tracking beyond the current ClinicalTrials.gov MVP boundary.

---

## 5. Current Guardrails

MVP source scope remains limited to:

```text
FDA
TFDA
ClinicalTrials.gov
```

Do not add the following unless explicitly approved:

- Additional agencies such as EMA, NMPA, PMDA, WHO ICTRP, EU CTIS
- Runtime source or guidance expansion for EMA, NMPA/CDE, PMDA, ICH, WHO ICTRP, EU CTIS, or other sources
- Literature integration
- Patent integration
- Finance integration
- News integration
- Scheduler
- Alerts
- Persistence layer
- Dashboard
- HTTP/SSE transport
- GitHub issue automation
- New MCP tools
- `.mcp.json` changes
- Company alias database
- Corporate-family mapping
- Product ownership inference
- CMC weekly management report template
- Runtime report generator
- Tool installation or new dependency adoption based only on the tool survey

For uncertain work, keep the implementation smaller and document limitations clearly.

The repository is not a GMP, QA, EDMS, eCTD publishing, official system of record, clinical decision support, legal decision system, medical decision system, commercial intelligence platform, or management decision system.

Do not store confidential, signed, GMP raw, QA-approved, official submission, vendor confidential, or non-public company records in this repository.

---

## 6. Testing And Execution Environment Notes

Codespaces quota is near limit until July 2026. For upcoming code/test work, default to Claude Code Web and Codex Web workflows.

Do not assume Codespaces is available unless the user explicitly confirms availability.

When suggesting validation, provide complete copy-paste commands. Do not say only "switch to the PR branch" without the full command block.

If asking Codex or Claude Code only to validate, explicitly instruct:

```text
Do not modify files.
Do not commit.
Do not create a branch.
Do not create a pull request.
Only run the requested commands and report results.
```

If a Python environment is available and `pytest` or `mcp` is missing, install the project first:

```bash
python -m pip install -e .
```

Do not commit generated or accidental dependency files such as `poetry.lock` unless dependency management is explicitly approved as part of the task.

---

## 7. Workflow Correction And Direction Calibration Rule

Use this workflow for future PRs while Codespaces quota is limited:

```text
Create branch → implement small docs/spec or code change → validate through Claude Code Web or Codex Web when available → open PR → confirm mergeable/review comments → merge → update state/handoff when needed → tag only when a release tag is explicitly needed
```

When local or Codespaces validation is unavailable, clearly label validation as not run and provide copy-paste commands for the user or Claude Code / Codex Web to run.

Do not tag before confirming that the PR has actually been merged into `main`.

When the user explicitly confirms that a PR is already merged or approves the next step, do not repeatedly block progress by asking for the same confirmation again. For repo-changing work, perform at most one verification pass when needed, then continue with the approved next step.

After a sequence of similar PRs, pause for direction calibration before proposing or executing the next same-type PR. This rule is intended to prevent uncontrolled scope drift and over-narrowing around local documents.

The PR #104–#112 CMC readiness docs/spec set should be treated as a completed small extension workstream. Do not add a dedicated management weekly report template at this time because the updated Prompt 6 stress test returned PASS and recommended no repo change.

The PR #120–#122 dashboard architecture/schema set should be treated as the current re-anchor point for the original full-system regulatory-clinical intelligence roadmap.

---

## 8. Recommended Next Step

Do not immediately build runtime automation, add another CMC template document, install a surveyed tool, create `docs/cmc_management_weekly_report_template.md`, implement EMA/NMPA/PMDA/ICH connectors, add GitHub Actions, or add a runtime dashboard renderer.

Recommended next version:

```text
v0.2.16 — Dashboard dry-run artifact planning
```

Recommended next action after this state sync:

```text
Add static dashboard dry-run design using mock data, still docs/spec-only.
```

Recommended scope for the next docs/spec PR:

```text
1. Define a mock-data-only static dashboard dry-run design.
2. Show how RegulatoryGuidanceUpdate, ClinicalTrialUpdate, SourceHealthEvent, and DashboardDigestSummary records flow into static dashboard artifacts.
3. Define dashboard tab acceptance criteria.
4. Explicitly avoid GitHub Actions, dashboard renderer, scheduler, alerts, persistence, runtime connector, source expansion, and new MCP tools.
```

Preserve MVP runtime source scope: FDA, TFDA, ClinicalTrials.gov only.

Do not add new agencies, sources, guidance connectors, tools, scheduler, alerts, dashboard renderer, persistence, HTTP/SSE transport, `.mcp.json`, GitHub automation, company alias database, corporate-family mapping, product ownership inference, literature, patent, finance, or news integrations without explicit approval.
