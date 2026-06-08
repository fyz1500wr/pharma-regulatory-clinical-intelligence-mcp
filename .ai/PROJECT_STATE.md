# Project State — Pharma Regulatory Clinical Intelligence MCP

Last updated: 2026-06-08

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`
Current stable branch: `main`
Current completed release: `v0.2.15-fda-abuse-detection-source-failure-diagnostics`
Latest post-release main checkpoint: PR #104 CMC submission readiness mapping workflow

---

## 1. Current Status

The repository remains at completed tagged release `v0.2.15-fda-abuse-detection-source-failure-diagnostics`. After that release, the main branch completed source-limitation/usability hardening, PM/RA regulatory-clinical digest/report docs-spec work, a clean-source digest dry-run, and the first CMC submission readiness mapping workflow.

Latest confirmed main commit:

```text
bdabd104a86e4f0e32f13fe1013940bd6ed2363f
```

Latest confirmed release tag:

```text
v0.2.15-fda-abuse-detection-source-failure-diagnostics
```

Important release and checkpoint status:

- v0.2.15 remains the latest confirmed completed and tagged release.
- The latest confirmed release tag is `v0.2.15-fda-abuse-detection-source-failure-diagnostics`.
- No new release tag was created for PR #97–#104 docs/product workflow work.
- PR #103 has been merged into `main`.
- PR #103 merge commit is `7b1c95ecb41dadb517718f3d2b431b7d776c0abb`.
- PR #104 has been merged into `main`.
- PR #104 merge commit is `bdabd104a86e4f0e32f13fe1013940bd6ed2363f`.
- Final PR #104 validation passed: README documentation index test 7 passed and full test suite 209 passed.
- The current digest/report and CMC readiness workstreams remain docs/spec-only and do not add runtime report generation.

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

Validation:

```text
python -m pytest -q
202 passed
```

Important interpretation:

FDA abuse-detection/apology responses are source-access limitations. They must not be interpreted as evidence that no FDA records or updates exist.

---

## 3. Post-Release Source-Limitation / Usability Hardening Checkpoint

PR #89–#95 completed a source-limitation and usability hardening phase.

Latest checkpoint before the digest/report workstream:

```text
PR #95 merge commit: 57a3478e43445ca6f8e56e2636b9067943d491a2
```

Final post-PR #95 baseline validation:

```text
pytest tests/test_digest_source_coverage_wording.py -q
2 passed

pytest tests/test_company_comparison_source_unavailable_display.py -q
3 passed

pytest tests/test_project_state_release_tag_consistency.py -q
5 passed

pytest -q
207 passed
```

Important interpretation:

- FDA source unavailability must not be interpreted as no FDA updates.
- Global source-health failures must be separated from requested-source query errors.
- ClinicalTrials.gov company comparison output must separate sponsor-name matches from non-sponsor returned records.
- Digest output remains working intelligence and requires human review before regulatory, clinical, legal, medical, competitive, commercial, or management-facing decisions.

---

## 4. Post-Release PM/RA Digest/Report Docs-Spec Workstream

### PR #97 — Regulatory-clinical digest report workflow

Added:

```text
docs/regulatory_clinical_digest_report_workflow.md
```

Purpose:

- Define how MVP tool outputs should be turned into a PM/RA-facing regulatory-clinical intelligence memo.
- Require source coverage status, regulatory findings, clinical trial findings, company/sponsor association review, risks/caveats, PM/RA follow-up actions, human review checklist, and raw MCP traceability.
- Preserve the rule that unavailable sources are not zero-result sources.

### PR #98 — Digest example memo and prompt pack

Added:

```text
docs/regulatory_clinical_digest_example_memo.md
docs/regulatory_clinical_digest_prompt_pack.md
```

Purpose:

- Provide a controlled example PM/RA digest memo.
- Provide copy-paste prompts for turning MVP tool outputs into controlled PM/RA memo drafts.
- Add prompts for clean requested-source scenarios, partial requested-source coverage, company/sponsor association review, executive summary only, human review checklist, red flag review, and minimal one-page memo.

### PR #99 — Digest memo validation exercise

Added:

```text
docs/regulatory_clinical_digest_memo_validation_exercise.md
```

Purpose:

- Define a dry-run validation exercise before designing any runtime generator.
- Validate whether generated memos are readable, source-aware, and safe for PM/RA review.
- Require explicit query scope, source coverage interpretation, regulatory finding validation, clinical trial finding validation, company/sponsor association validation, risk/caveat validation, PM/RA follow-up validation, and red-flag sentence review.

### PR #100 — Continuation update after digest dry-run validation

Updated:

```text
PROJECT_STATE_CONTINUATION.md
```

Purpose:

- Record PR #97–#99 and the digest dry-run validation result.
- Preserve the `PASS_WITH_LIMITATIONS` dry-run finding.
- Recommend a report template contract before any runtime generator.

### PR #101 — Regulatory-clinical digest report template contract

Added:

```text
docs/regulatory_clinical_digest_report_template_contract.md
```

Also updated:

```text
README.md
tests/test_readme_documentation_index.py
```

Purpose:

- Define a fixed docs/spec-only contract for controlled digest memo templates.
- Define required input object, required tool output inputs, required output object, source coverage labels, fixed memo sections, company/sponsor association fields, human review checklist, raw MCP traceability, and acceptance criteria before runtime implementation.
- Preserve explicit non-goals: no runtime report generator, template renderer, MCP-side report helper, new source, scheduler, dashboard, alerts, persistence, HTTP/SSE transport, `.mcp.json`, company alias database, corporate-family mapping, product ownership inference, or literature/patent/finance/news integration.

Validation:

```text
python -m pytest tests/test_readme_documentation_index.py -q
6 passed in 0.03s

python -m pytest -q
208 passed in 12.82s
```

### PR #102 — Project state update after digest template contract

Updated:

```text
.ai/PROJECT_STATE.md
PROJECT_STATE_CONTINUATION.md
```

Purpose:

- Record the PR #97–#101 digest/report docs-spec workstream.
- Record Codespaces quota limitation through July 2026.
- Preserve the recommendation to pause for direction calibration before runtime generator work.

### PR #103 — Clean-source digest dry-run memo

Added:

```text
docs/regulatory_clinical_digest_clean_source_dry_run.md
```

Also updated:

```text
README.md
tests/test_readme_documentation_index.py
```

Purpose:

- Validate the digest report template contract under a clean requested-source scenario using TFDA and ClinicalTrials.gov.
- Explicitly exclude FDA from the clean-source exercise so FDA unavailable-source behavior is not confused with zero-result behavior.
- Preserve company/sponsor association caveats and working-intelligence labeling.

Validation:

```text
python -m pytest tests/test_readme_documentation_index.py -q
6 passed in 0.03s

python -m pytest -q
208 passed in 10.90s
```

Important caveat: the reported validation ran in a `work` checkout rather than a branch-name-confirmed `add-clean-source-digest-dry-run` checkout, but the working tree had no uncommitted changes.

---

## 5. CMC Submission Readiness Docs-Spec Workstream

### PR #104 — CMC submission readiness mapping workflow

Added:

```text
docs/cmc_submission_readiness_mapping_workflow.md
```

Also updated:

```text
README.md
tests/test_readme_documentation_index.py
```

Purpose:

- Define a docs/spec-only workflow for mapping CMC project work into submission-readiness planning.
- Cover Module 3 gap mapping, vendor dependencies, method/stability dependencies, critical path rules, PM follow-up actions, and human review checklist.
- Preserve that the repository is not an official IND/eCTD submission system, eCTD publisher, GMP/QA record system, or EDMS.

Validation:

```text
python -m pytest tests/test_readme_documentation_index.py -q
7 passed

python -m pytest -q
209 passed
```

---

## 6. Latest Digest Dry-Run Validation Status

The latest documented digest dry-run sequence now includes both a partial-coverage FDA-unavailable scenario and a clean requested-source scenario.

Partial-coverage scenario after PR #99:

```text
Purpose: regulatory-clinical digest memo dry-run
Indication: gastric cancer
Companies: AstraZeneca, Merck
Regulatory sources: FDA, TFDA
Clinical registry: ClinicalTrials.gov
Date range: 1y
Limit: 5
```

Source health result:

```text
Overall source health: degraded
FDA: failed / SOURCE_UNAVAILABLE / high severity
TFDA: pass
ClinicalTrials.gov: pass
```

Correct interpretation:

```text
The digest returned 1 TFDA regulatory update and 5 ClinicalTrials.gov trial update records, while FDA coverage was unavailable and requires manual verification.
```

Dry-run memo validation result:

```text
PASS_WITH_LIMITATIONS
```

Clean-source scenario after PR #103:

```text
Purpose: clean requested-source digest memo dry-run
Regulatory source: TFDA
Clinical registry: ClinicalTrials.gov
FDA: not requested
```

Clean-source validation result:

```text
PASS_WITH_CONTROLLED_LIMITATIONS
```

Important interpretation:

- FDA not requested is not the same as FDA zero-result.
- TFDA and ClinicalTrials.gov clean-source behavior is documented as a controlled dry-run, not a live-source evidence claim.
- Company/sponsor association caveats remain required.

---

## 7. Current Product Status

Status:

```text
Regulatory-clinical digest/report workflow is usable for controlled PM/RA dry-run memo generation, with limitations, and now has a docs/spec-only template contract and clean-source dry-run. CMC submission readiness mapping has started as docs/spec-only and needs a non-confidential mock inventory dry-run next.
```

Estimated progress against the user's broader target system:

```text
Overall CMC PM + regulatory-clinical intelligence system: about 55% complete.
MVP regulatory-clinical intelligence prototype: about 70% complete.
```

What is now working:

- MVP source scope and guardrails are defined.
- FDA / TFDA / ClinicalTrials.gov MVP tools and safety interpretation rules exist.
- Source failure and source limitation wording is controlled.
- Regulatory-clinical digest memo workflow, prompt pack, validation exercise, template contract, and clean-source dry-run now exist.
- CMC submission readiness mapping workflow now exists as docs/spec-only.
- README documentation index tests continue to pass.

What remains intentionally not implemented:

- Runtime report generator.
- Template renderer.
- MCP-side report generation helper.
- Persistent source-failure event store.
- Dashboard, scheduler, alerting, external integration, or GitHub automation.
- Additional source expansion.
- Official eCTD publishing, EDMS, GMP/QA record, or submission record storage.

---

## 8. Current Guardrails

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
- News integration

For uncertain work, keep the implementation smaller and document limitations clearly.

The repository is not a GMP, QA, EDMS, eCTD publishing, official system of record, clinical decision support, legal decision system, medical decision system, commercial intelligence platform, or management decision system.

Do not store confidential, signed, GMP raw, QA-approved, official submission, or non-public company records in this repository.

---

## 9. Testing And Execution Environment Notes

Codespaces quota is near limit until July 2026. For upcoming code/test work, default to Claude Code Web and Codex Web workflows.

Do not assume Codespaces is available unless the user explicitly confirms availability. When suggesting validation, prefer:

```text
Claude Code Web or Codex Web validation on the PR branch
```

Only provide Codespaces commands as an optional fallback or when the user confirms Codespaces is available again.

If a Python environment is available and `pytest` is missing, install the project with dev dependencies first:

```bash
python -m pip install -e ".[dev]"
```

Do not commit generated or accidental dependency files such as `poetry.lock` unless dependency management is explicitly approved as part of the task.

---

## 10. Workflow Correction And Direction Calibration Rule

Use this workflow for future PRs while Codespaces quota is limited:

```text
Create branch → implement small docs/spec or code change → validate through Claude Code Web or Codex Web when available → open PR → confirm mergeable/review comments → merge → update state/handoff when needed → tag only when a release tag is explicitly needed
```

When local or Codespaces validation is unavailable, clearly label validation as not run and provide copy-paste commands for the user or Codex Web to run.

Do not tag before confirming that the PR has actually been merged into `main`.

After a sequence of similar PRs, the assistant/project workflow must pause for direction calibration before proposing or executing the next same-type PR. This rule is intended to prevent uncontrolled scope drift and over-narrowing around local documents.

PR #97–#103 should be treated as a completed digest/report docs-spec workstream. Do not proceed directly to runtime report generation without explicit approval.

PR #104 starts the CMC submission readiness docs/spec workstream. Before runtime automation, validate it with a non-confidential mock inventory and Module 3 gap matrix dry-run.

---

## 11. Recommended Next Step

Recommended next version:

```text
v0.2.16 — CMC submission readiness mock inventory dry-run
```

Recommended action:

```text
Create a non-confidential CMC mock inventory and Module 3 gap matrix dry-run.
```

Recommended document:

```text
docs/cmc_submission_readiness_mock_inventory.md
```

Purpose:

- Use fake/non-confidential sample CMC tasks to validate the PR #104 readiness workflow.
- Test whether the workflow can produce a PM-usable Module 3 gap matrix, vendor follow-up list, method/stability dependency map, and critical path summary.
- Keep it documentation-only and avoid storing confidential/GMP/QA/submission records.

Suggested mock items:

- DP potency assay qualification pending.
- DP stability report pending.
- DS specification needs CMC/RA review.
- Reference standard qualification status unknown.
- Vendor COA delayed.
- Excipient change rationale decision pending.

Preserve MVP source scope: FDA, TFDA, ClinicalTrials.gov only.

Keep the next step small and phase-controlled.

Do not add new agencies, sources, tools, scheduler, alerts, dashboard, persistence, HTTP/SSE transport, `.mcp.json`, GitHub automation, company alias database, corporate-family mapping, product ownership inference, literature, patent, finance, or news integrations without explicit approval.
