# Project State Continuation

Created: 2026-06-04  
Updated: 2026-06-06

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`

This file is a compact continuation handoff for starting a new chat.

Canonical detailed status is in `.ai/PROJECT_STATE.md`. This file is the preferred short handoff when chat context becomes slow or too long.

## Current checkpoint

- Stable branch: `main`
- Latest confirmed merged PR: PR #101
- PR #101 merge commit: `6e058cd4dc5c3c4f32189af8acce09f9b2b05645`
- Latest completed workstream: PM/RA regulatory-clinical digest report workflow, prompt pack, example memo, memo validation exercise, and report template contract
- Latest validation status: `PASS`
- Latest validation evidence:
  - `python -m pytest tests/test_readme_documentation_index.py -q` → `6 passed in 0.03s`
  - `python -m pytest -q` → `208 passed in 12.82s`
- Current tagged release: remains `v0.2.15-fda-abuse-detection-source-failure-diagnostics`; no new release tag was created for PR #97–#101 docs/product workflow work
- Open PRs at this checkpoint: none known after PR #101 merge

## Current project phase

The project is still MVP v1 and must remain source- and scope-controlled.

Approved MVP source scope remains:

```text
FDA
TFDA
ClinicalTrials.gov
```

Do not add EMA, PMDA, NMPA, CTIS, WHO ICTRP, literature, patent, finance, news, company-alias database, corporate-family mapping, product ownership inference, dashboard, scheduler, alerting, persistence, HTTP/SSE transport, `.mcp.json`, GitHub automation, or other integrations unless explicitly approved.

## Recent PR sequence after PR #94

### PR #95

Updated project continuation/state after PR #94 digest source-coverage wording work.

Purpose:

- Preserve the PR #94 source-limitation re-test result.
- Record that digest output now distinguishes requested-source query errors from global source-health warnings.

### PR #96

Updated `.ai/PROJECT_STATE.md` after the post-PR #95 usability hardening checkpoint.

Purpose:

- Keep project-state handoff aligned with the source-limitation and usability-hardening phase.
- Confirm that future work should pause for direction calibration before adding new product features.

### PR #97 — Regulatory-clinical digest report workflow

Added:

```text
docs/regulatory_clinical_digest_report_workflow.md
```

Also updated README documentation index and README index test.

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

Also updated README documentation index and README index test.

Purpose:

- Provide a controlled example PM/RA digest memo.
- Provide copy-paste prompts for turning MVP tool outputs into controlled PM/RA memo drafts.
- Add prompts for clean requested-source scenarios, partial requested-source coverage, company/sponsor association review, executive summary only, human review checklist, red flag review, and minimal one-page memo.

### PR #99 — Digest memo validation exercise

Added:

```text
docs/regulatory_clinical_digest_memo_validation_exercise.md
```

Also updated README documentation index and README index test.

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

Also updated README documentation index and README index test.

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

## Latest dry-run validation performed after PR #99

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

Generated output package included:

```text
check_source_health
list_source_failures
generate_regulatory_digest
compare_companies_by_indication
```

Source health result:

```text
Overall source health: degraded
FDA: failed / SOURCE_UNAVAILABLE / high severity
TFDA: pass
ClinicalTrials.gov: pass
```

Key interpretation:

- FDA failure is a source-access limitation.
- It must not be interpreted as FDA having zero matching regulatory updates.
- Manual FDA verification is required before PM/RA or management-facing conclusions.

Digest result:

```text
regulatory update count: 1
clinical trial update count: 5
source query errors: 1
open source failures: 1
```

Correct wording:

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

## Current overall product status

Status:

```text
Digest report workflow is usable for controlled PM/RA dry-run memo generation, with limitations, and now has a docs/spec-only template contract.
```

What is now working:

- The workflow can guide memo structure.
- The prompt pack can generate controlled memo sections.
- The validation exercise can detect overstatement risk.
- The report template contract defines required inputs, outputs, coverage labels, sponsor association fields, and acceptance criteria.
- FDA source unavailability is preserved as partial coverage.
- ClinicalTrials.gov company comparison is interpreted conservatively.

What remains intentionally not implemented:

- Runtime report generator.
- Template renderer.
- MCP-side report generation helper.
- Persistent source-failure event store.
- Dashboard, scheduler, alerting, or external integration.
- Additional source expansion.

## Current guardrails

- Keep MVP source scope limited to FDA, TFDA, and ClinicalTrials.gov.
- Do not add new agencies, sources, MCP tools, transport modes, dashboards, schedulers, alerts, persistence, external integrations, GitHub automation, or repository automation unless explicitly approved.
- Keep future work small and phase-controlled.
- Use Traditional Chinese for user-facing discussion.
- Avoid accidental Japanese output.
- After repeated related PRs, pause for direction calibration before continuing.
- Repo is not a GMP, QA, EDMS, eCTD publishing, or official system of record.
- Do not store confidential, signed, GMP raw, QA-approved, or official submission records in this repo.

## Recommended next step

Do not immediately build a runtime generator.

Recommended next action:

```text
Pause for direction calibration after PR #97–#101 digest/report docs-spec workstream.
```

Recommended options:

### Option A — recommended

```text
Run one clean-source dry-run memo using TFDA + ClinicalTrials.gov only.
```

Purpose:

- Validate clean requested-source behavior separately from FDA source-unavailable behavior.
- Confirm the template contract works for a non-blocked source scenario.
- Keep scope inside existing MVP sources.

### Option B

```text
Start CMC/IND readiness mapping workflow as docs/spec-only.
```

Purpose:

- Shift product workflow from digest memo formatting into CMC/IND readiness mapping.
- Keep it documentation-only at first.

### Option C

```text
Create source-health operator workflow as docs/spec-only.
```

Purpose:

- Help operators distinguish source block, egress/runtime problem, parser issue, query sensitivity, and true zero result.

### Option D — defer until later

```text
Design runtime report generator.
```

This should be deferred until after explicit approval and after the clean-source dry-run validates the template contract in a non-blocked scenario.

## New-chat opening prompt

請根據 GitHub repo `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`、`.ai/PROJECT_STATE.md`、以及 `PROJECT_STATE_CONTINUATION.md` 繼續。

請用繁體中文回覆，不要輸出日文。

請先確認：

1. `main` 是否已包含 PR #101；
2. `PROJECT_STATE_CONTINUATION.md` 和 `.ai/PROJECT_STATE.md` 是否已記錄 PR #97–#101、digest dry-run validation、template contract、以及 208 passed validation；
3. 是否有 open PR；
4. 最新測試狀態；
5. 是否需要先做 direction calibration。

目前建議下一步是：

```text
Direction calibration after PR #97–#101 digest/report docs-spec workstream.
```

請維持 docs/spec-only，不要新增 runtime generator、MCP tool、source、scheduler、dashboard、alerts、persistence、HTTP/SSE、`.mcp.json`、company alias database、corporate-family mapping、product ownership inference、literature/patent/finance/news integration，除非我明確批准。
