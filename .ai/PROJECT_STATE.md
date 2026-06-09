# Project State — Pharma Regulatory Clinical Intelligence MCP

Last updated: 2026-06-09

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`
Current stable branch: `main`
Current completed release: `v0.2.15-fda-abuse-detection-source-failure-diagnostics`
Latest post-release main checkpoint: PR #111 CMC readiness management summary prompt revision

Latest confirmed main commit:

```text
605b2dc819852a90874ee8016ec64c37f87e5e7b
```

---

## 1. Current Status

The repository remains at completed tagged release `v0.2.15-fda-abuse-detection-source-failure-diagnostics`. After that release, the `main` branch completed source-limitation/usability hardening, PM/RA regulatory-clinical digest/report docs-spec work, a clean-source digest dry-run, and a CMC submission readiness docs/spec workstream through PR #111.

No new release tag has been created for the post-release docs/product workflow work after v0.2.15.

Latest confirmed release tag:

```text
v0.2.15-fda-abuse-detection-source-failure-diagnostics
```

Latest completed CMC checkpoint:

```text
PR #111 merge commit: 605b2dc819852a90874ee8016ec64c37f87e5e7b
```

Latest validation recorded for PR #111:

```bash
python -m pytest tests/test_readme_documentation_index.py -q
# 10 passed in 0.02s

python -m pytest -q
# 212 passed in 2.89s

git status --short
# clean; no output
```

Validation environment note: PR #111 was validated in Claude Code on branch `revise-cmc-readiness-management-summary-prompt` at HEAD `2dce4d1`. `pytest` and `mcp` were installed only into the execution environment. No repository dependency files were modified, and no repository files, commits, branches, or pull requests were created during validation.

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

## 3. Post-Release PM/RA Digest/Report Docs-Spec Workstream

PR #97–#103 completed a controlled PM/RA regulatory-clinical digest/report docs-spec workstream.

Key outputs:

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
- A docs/spec-only report template contract exists.
- A clean-source dry-run scenario exists.
- Digest outputs remain working intelligence and require human review.
- No runtime report generator, template renderer, MCP-side report helper, new source, scheduler, dashboard, alert, persistence, HTTP/SSE transport, company alias database, corporate-family mapping, product ownership inference, or literature/patent/finance/news integration was added.

---

## 4. CMC Submission Readiness Docs-Spec Workstream

### PR #104 — CMC submission readiness mapping workflow

Added:

```text
docs/cmc_submission_readiness_mapping_workflow.md
```

Purpose:

- Define a docs/spec-only workflow for mapping CMC project work into submission-readiness planning.
- Cover Module 3 gap mapping, vendor dependencies, method/stability dependencies, critical path rules, PM follow-up actions, and human review checklist.
- Preserve that the repository is not an official IND/eCTD submission system, eCTD publisher, GMP/QA record system, or EDMS.

### PR #105 — Project state update after CMC readiness workflow

Updated project-state handoff after the CMC readiness workflow checkpoint.

### PR #106 — CMC submission readiness mock inventory

Added:

```text
docs/cmc_submission_readiness_mock_inventory.md
```

Purpose:

- Provide a synthetic, non-confidential CMC readiness mock inventory.
- Validate whether the PR #104 workflow can produce a practical Module 3 gap matrix, vendor follow-up list, method/stability dependency map, critical path summary, PM next-action list, and human review checklist.
- Keep the exercise documentation/specification-only and avoid storing confidential, GMP, QA-approved, signed, official submission, or vendor confidential records.

Validation recorded for PR #106:

```bash
python -m pytest tests/test_readme_documentation_index.py -q
# passed

python -m pytest -q
# 210 passed
```

### PR #107 — CMC submission readiness input template and prompt pack

Added:

```text
docs/cmc_submission_readiness_input_template.md
```

Also updated:

```text
README.md
tests/test_readme_documentation_index.py
```

Purpose:

- Define a reusable docs/spec-only input template and prompt pack for non-confidential CMC readiness information.
- Support consistent generation of Module 3 gap matrix, vendor follow-up list, method/stability dependency map, decision log, PM next-action list, human review checklist, and management-ready readiness drafting.
- Absorb duplicate README-index wording from PR #108 and PR #109.

Validation recorded for PR #107:

```bash
python -m pytest tests/test_readme_documentation_index.py -q
# 10 passed in 0.03s

python -m pytest -q
# 212 passed in 3.47s

git status --short
# clean; no output
```

### PR #108 and PR #109 — Closed duplicate README-index wording PRs

PR #108 and PR #109 only updated the README wording for `docs/cmc_submission_readiness_mock_inventory.md`. That wording was absorbed into PR #107.

Status:

```text
PR #108: closed as superseded, not merged
PR #109: closed as superseded, not merged
```

### PR #110 — Project state sync after CMC readiness input template

Updated:

```text
.ai/PROJECT_STATE.md
PROJECT_STATE_CONTINUATION.md
```

Purpose:

- Synchronize the detailed and compact state files after the completed CMC readiness input template checkpoint.
- Record PR #105, PR #106, PR #107, and closed duplicate PR #108 / PR #109.
- Preserve test-contract fields in `.ai/PROJECT_STATE.md`.

Validation recorded for PR #110:

```bash
python -m pytest tests/test_project_state_release_tag_consistency.py -q
# 5 passed in 0.03s

python -m pytest tests/test_readme_documentation_index.py -q
# 10 passed in 0.02s

python -m pytest -q
# 212 passed in 3.37s

git status --short
# clean; no output
```

### PR #111 — CMC readiness management summary prompt revision

Updated:

```text
docs/cmc_submission_readiness_input_template.md
```

Purpose:

- Revise Prompt 6 from a brief one-time management summary prompt into a controlled management summary and weekly reporting stress-test prompt.
- Add required fields for report context, one-sentence executive summary, current/prior R/Y/G status, status movement reason, top management concerns, critical path movement, decisions needed this week, vendor escalations, completed this week, next-week priorities, items not suitable for management escalation, assumptions/caveats, and template adequacy check.
- Keep the correction inside the existing input template instead of immediately adding `docs/cmc_management_weekly_report_template.md`.

Validation recorded for PR #111:

```bash
python -m pytest tests/test_readme_documentation_index.py -q
# 10 passed in 0.02s

python -m pytest -q
# 212 passed in 2.89s

git status --short
# clean; no output
```

### Second Claude Project stress test after PR #111

A second Claude Project stress test used the updated Prompt 6 and the non-confidential mock CMC readiness case.

Result:

```text
Prompt 6 adequacy assessment: PASS
Repository action recommendation: No repo change needed
```

Interpretation:

- Updated Prompt 6 is sufficient for recurring weekly management reporting under the current mock-case stress test.
- No recurring structural gap was found that justifies creating `docs/cmc_management_weekly_report_template.md` at this time.
- Do not create `docs/cmc_management_weekly_report_template.md` unless future repeated stress tests or real non-confidential/de-identified use show a structural gap that cannot reasonably fit in the existing input template.

---

## 5. Current Product Status

Estimated progress against the user's broader target system:

```text
Overall CMC PM + regulatory-clinical intelligence system: about 62% complete
MVP regulatory-clinical intelligence prototype: about 70% complete
CMC readiness docs/spec workflow: usable for non-confidential dry-run, prompt-based assessment, and mock weekly management reporting
```

What is now working:

- MVP source scope and guardrails are defined.
- FDA / TFDA / ClinicalTrials.gov MVP tools and safety interpretation rules exist.
- Source failure and source limitation wording is controlled.
- Regulatory-clinical digest memo workflow, prompt pack, validation exercise, template contract, and clean-source dry-run exist.
- CMC submission readiness mapping workflow exists as docs/spec-only.
- CMC submission readiness mock inventory exists as docs/spec-only.
- CMC submission readiness input template and prompt pack exist as docs/spec-only.
- Prompt 6 now supports mock management weekly reporting stress-test output.
- README documentation index tests pass after PR #111.

What remains intentionally not implemented:

- Runtime report generator.
- Template renderer.
- MCP-side report generation helper.
- Persistent source-failure event store.
- Dashboard, scheduler, alerting, external integration, or GitHub automation.
- Additional source expansion.
- Official eCTD publishing, EDMS, GMP/QA record, or submission record storage.
- Management decision automation.
- Dedicated `docs/cmc_management_weekly_report_template.md`.

---

## 6. Current Guardrails

MVP source scope remains limited to:

```text
FDA
TFDA
ClinicalTrials.gov
```

Do not add the following unless explicitly approved:

- Additional agencies such as EMA, NMPA, PMDA, WHO ICTRP, EU CTIS
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

For uncertain work, keep the implementation smaller and document limitations clearly.

The repository is not a GMP, QA, EDMS, eCTD publishing, official system of record, clinical decision support, legal decision system, medical decision system, commercial intelligence platform, or management decision system.

Do not store confidential, signed, GMP raw, QA-approved, official submission, vendor confidential, or non-public company records in this repository.

---

## 7. Testing And Execution Environment Notes

Codespaces quota is near limit until July 2026. For upcoming code/test work, default to Claude Code Web and Codex Web workflows.

Do not assume Codespaces is available unless the user explicitly confirms availability.

When suggesting validation, prefer:

```text
Claude Code Web or Codex Web validation on the PR branch
```

If asking Codex or Claude Code only to validate, explicitly instruct:

```text
Do not modify files.
Do not commit.
Do not create a branch.
Do not create a pull request.
Only run the requested commands and report results.
```

If a Python environment is available and `pytest` is missing, install the project with dev dependencies first:

```bash
python -m pip install -e ".[dev]"
```

Do not commit generated or accidental dependency files such as `poetry.lock` unless dependency management is explicitly approved as part of the task.

---

## 8. Workflow Correction And Direction Calibration Rule

Use this workflow for future PRs while Codespaces quota is limited:

```text
Create branch → implement small docs/spec or code change → validate through Claude Code Web or Codex Web when available → open PR → confirm mergeable/review comments → merge → update state/handoff when needed → tag only when a release tag is explicitly needed
```

When local or Codespaces validation is unavailable, clearly label validation as not run and provide copy-paste commands for the user or Claude Code / Codex Web to run.

Do not tag before confirming that the PR has actually been merged into `main`.

After a sequence of similar PRs, pause for direction calibration before proposing or executing the next same-type PR. This rule is intended to prevent uncontrolled scope drift and over-narrowing around local documents.

The PR #104–#111 CMC readiness docs/spec set should be treated as a completed small workstream. Do not add a dedicated management weekly report template at this time because the updated Prompt 6 stress test returned PASS and recommended no repo change.

---

## 9. Recommended Next Step

Do not immediately build runtime automation, add another CMC template document, or create `docs/cmc_management_weekly_report_template.md`.

Recommended next version:

```text
v0.2.16 — Direction calibration after CMC management summary prompt stress test
```

Recommended next action:

```text
Pause for direction calibration. Choose the next workstream deliberately rather than adding more CMC weekly-report documents.
```

Recommended options for direction calibration:

```text
1. Use the current CMC readiness workflow with future non-confidential/de-identified inputs without new repo changes.
2. Return to regulatory-clinical digest workflow refinement only if a concrete recurring PM/RA use case is defined.
3. Consider source expansion only through the documented decision matrix and only after explicit user approval.
4. Consider runtime/report automation only after a separate approval decision covering workflow, fields, limitations, testing, and maintenance scope.
```

Explicit non-goal:

```text
Do not add a management weekly report template because the current stress-test evidence does not justify it.
```

Preserve MVP source scope: FDA, TFDA, ClinicalTrials.gov only.

Do not add new agencies, sources, tools, scheduler, alerts, dashboard, persistence, HTTP/SSE transport, `.mcp.json`, GitHub automation, company alias database, corporate-family mapping, product ownership inference, literature, patent, finance, or news integrations without explicit approval.
