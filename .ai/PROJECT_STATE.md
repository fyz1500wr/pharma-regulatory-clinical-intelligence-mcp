# Project State — Pharma Regulatory Clinical Intelligence MCP

Last updated: 2026-06-06

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`
Current stable branch: `main`
Current completed release: `v0.2.15-fda-abuse-detection-source-failure-diagnostics`
Latest post-release main checkpoint: PR #101 digest report template contract

---

## 1. Current Status

The repository remains at completed tagged release `v0.2.15-fda-abuse-detection-source-failure-diagnostics`. After that release, the main branch completed a post-release source-limitation / usability hardening phase and a PM/RA regulatory-clinical digest/report docs-spec workstream.

Latest confirmed main commit:

```text
6e058cd4dc5c3c4f32189af8acce09f9b2b05645
```

Latest confirmed release tag:

```text
v0.2.15-fda-abuse-detection-source-failure-diagnostics
```

Important release and checkpoint status:

- v0.2.15 remains the latest confirmed completed and tagged release.
- The latest confirmed release tag is `v0.2.15-fda-abuse-detection-source-failure-diagnostics`.
- No new release tag was created for PR #97–#101 docs/product workflow work.
- PR #101 has been merged into `main`.
- PR #101 merge commit is `6e058cd4dc5c3c4f32189af8acce09f9b2b05645`.
- Final PR #101 validation passed: README documentation index test 6 passed and full test suite 208 passed.
- The current digest/report workstream remains docs/spec-only and does not add runtime report generation.

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

---

## 5. Latest Digest Dry-Run Validation Status

The latest documented dry-run validation was performed after PR #99.

Scenario:

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

Digest result:

```text
regulatory update count: 1
clinical trial update count: 5
source query errors: 1
open source failures: 1
```

Correct interpretation:

```text
The digest returned 1 TFDA regulatory update and 5 ClinicalTrials.gov trial update records, while FDA coverage was unavailable and requires manual verification.
```

Dry-run memo validation result:

```text
PASS_WITH_LIMITATIONS
```

Reason:

- The memo can be produced in a PM/RA-readable and source-aware format.
- The memo preserves FDA source-access limitation.
- The memo separates sponsor-name matches from non-sponsor returned records.
- The memo avoids company superiority, ownership, approval probability, and commercial-strength claims.
- Limitation remains: FDA was unavailable, so source coverage is partial.

---

## 6. Current Product Status

Status:

```text
Digest report workflow is usable for controlled PM/RA dry-run memo generation, with limitations, and now has a docs/spec-only template contract.
```

What is now working:

- The workflow can guide memo structure.
- The prompt pack can generate controlled memo sections.
- The validation exercise can detect overstatement risk.
- The report template contract defines required inputs, outputs, source coverage labels, sponsor association fields, human review checklist, raw MCP traceability, and acceptance criteria.
- FDA source unavailability is preserved as partial coverage.
- ClinicalTrials.gov company comparison is interpreted conservatively.

What remains intentionally not implemented:

- Runtime report generator.
- Template renderer.
- MCP-side report generation helper.
- Persistent source-failure event store.
- Dashboard, scheduler, alerting, or external integration.
- Additional source expansion.

---

## 7. Current Guardrails

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

## 8. Testing Environment Notes

The Codespaces environment may not always have dev dependencies installed. If `pytest` is missing, install the project with dev dependencies first:

```bash
python -m pip install -e ".[dev]"
```

Do not commit generated or accidental dependency files such as `poetry.lock` unless dependency management is explicitly approved as part of the task.

---

## 9. Workflow Correction And Direction Calibration Rule

Use this workflow for future PRs:

```text
Create branch → implement → run focused tests → run full tests → open PR → confirm mergeable/review comments → merge → pull main → rerun relevant tests → tag only when a release tag is explicitly needed
```

Do not tag before confirming that the PR has actually been merged into `main`.

After a sequence of similar PRs, the assistant/project workflow must pause for direction calibration before proposing or executing the next same-type PR. This rule is intended to prevent uncontrolled scope drift and over-narrowing around local documents.

PR #97–#101 should be treated as a completed digest/report docs-spec workstream. Do not proceed directly to runtime report generation without explicit approval.

---

## 10. Recommended Next Step

Recommended next version:

```text
v0.2.16 — direction calibration after digest report template contract
```

Recommended action:

```text
Pause for direction calibration after PR #97–#101 digest/report docs-spec workstream.
```

Recommended options:

1. Run one clean-source dry-run memo using TFDA + ClinicalTrials.gov only.
2. Start CMC/IND readiness mapping workflow as docs/spec-only.
3. Create source-health operator workflow as docs/spec-only.
4. Defer runtime report generator until explicitly approved and until the clean-source dry-run validates the template contract in a non-blocked scenario.

Preserve MVP source scope: FDA, TFDA, ClinicalTrials.gov only.

Keep the next step small and phase-controlled.

Do not add new agencies, sources, tools, scheduler, alerts, dashboard, persistence, HTTP/SSE transport, `.mcp.json`, GitHub automation, company alias database, corporate-family mapping, product ownership inference, literature, patent, finance, or news integrations without explicit approval.
