# Project State Continuation

Created: 2026-06-04  
Updated: 2026-06-05

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`

This file is a compact continuation handoff for starting a new chat.

Canonical detailed status remains in `.ai/PROJECT_STATE.md` when it is updated. This file is the preferred short handoff when chat context becomes slow or too long.

## Current checkpoint

- Stable branch: `main`
- Latest confirmed merged PR: PR #99
- PR #99 merge commit: `4b2f60d0e7dfbbc8e3c6d09b2061d72f5d8de3df`
- Latest completed workstream: PM/RA regulatory-clinical digest report workflow, prompt pack, example memo, and memo validation dry-run
- Latest dry-run validation status: `PASS_WITH_LIMITATIONS`
- Current tagged release: remains the prior MVP release tag; no new release tag was created for PR #97–#99 docs/product workflow work
- Open PRs at this checkpoint: none known after PR #99 merge

## Current project phase

The project is still MVP v1 and must remain source- and scope-controlled.

Approved MVP source scope remains:

```text
FDA
TFDA
ClinicalTrials.gov
```

Do not add EMA, PMDA, NMPA, CTIS, WHO ICTRP, literature, patent, finance, news, company-alias database, corporate-family mapping, product ownership inference, dashboard, scheduler, alerting, persistence, HTTP/SSE transport, `.mcp.json`, or other integrations unless explicitly approved.

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

### Source health result

Overall source health: `degraded`

Source-specific result:

```text
FDA: failed / SOURCE_UNAVAILABLE / high severity
TFDA: pass
ClinicalTrials.gov: pass
```

FDA details:

- FDA guidance and RSS fetches redirected to FDA abuse-detection/apology path.
- Final URL included `https://www.fda.gov/apology_objects/abuse-detection-apology.html`.
- Status code was 404.
- `detected_source_block` was true.

Interpretation:

- FDA failure is a source-access limitation.
- It must not be interpreted as FDA having zero matching regulatory updates.
- Manual FDA verification is required before PM/RA or management-facing conclusions.

### Source failure result

`list_source_failures` returned:

```text
open_failure_count: 1
high_failure_count: 1
critical_failure_count: 0
open failure: FDA_openFDA-api_status-open
```

Interpretation:

- FDA has an open high-severity source-access failure in the current runtime.
- This is a current source-health snapshot, not a historical failure database.

### Digest result

`generate_regulatory_digest` returned:

```text
regulatory update count: 1
clinical trial update count: 5
source query errors: 1
open source failures: 1
```

Key digest behavior:

- Executive summary stated: `Coverage is partial for requested source(s): FDA`.
- Executive summary stated that zero returned updates must not be interpreted as no updates for unavailable sources.
- Digest returned 1 TFDA regulatory update.
- Digest returned 5 ClinicalTrials.gov trial records.

Important interpretation:

- Correct wording is not `No FDA updates`.
- Correct wording is: `The digest returned 1 TFDA regulatory update and 5 ClinicalTrials.gov trial update records, while FDA coverage was unavailable and requires manual verification.`

### Company comparison result

`compare_companies_by_indication` returned activity-evaluable rows for both AstraZeneca and Merck because ClinicalTrials.gov was available.

Observed company rows:

```text
AstraZeneca:
- returned records: 5
- sponsor-name matches: 4
- non-sponsor records requiring manual review: 1
- active trial count: 2
- completed/terminated/suspended/withdrawn group: 3
- highest phase: PHASE3

Merck:
- returned records: 5
- sponsor-name matches: 1
- non-sponsor records requiring manual review: 4
- active trial count: 2
- completed/terminated/suspended/withdrawn group: 3
- highest phase: PHASE3
```

Interpretation rule:

- These are ClinicalTrials.gov query results.
- Sponsor-name matches must be separated from non-sponsor returned records.
- The counts do not establish company superiority, product ownership, clinical success, approval probability, or commercial strength.
- Non-sponsor returned records require manual sponsor/product association review.

### Dry-run memo validation result

Final dry-run decision:

```text
PASS_WITH_LIMITATIONS
```

Reason:

- The memo can be produced in a PM/RA-readable and source-aware format.
- The memo preserves FDA source-access limitation.
- The memo separates sponsor-name matches from non-sponsor returned records.
- The memo avoids company superiority, ownership, approval probability, and commercial-strength claims.
- Limitation remains: FDA was unavailable, so source coverage is partial.

Generated local artifact in the prior chat:

```text
/mnt/data/regulatory_clinical_digest_dry_run_memo_validation.md
```

This file was a chat artifact, not necessarily committed to the repository.

## Current overall product status

Status:

```text
Digest report workflow is usable for controlled PM/RA dry-run memo generation, with limitations.
```

What is now working:

- The workflow can guide memo structure.
- The prompt pack can generate controlled memo sections.
- The validation exercise can detect overstatement risk.
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
- Do not add new agencies, sources, MCP tools, transport modes, dashboards, schedulers, alerts, persistence, external integrations, or repository automation unless explicitly approved.
- Keep future work small and phase-controlled.
- Use Traditional Chinese for user-facing discussion.
- Avoid accidental Japanese output.
- After repeated related PRs, pause for direction calibration before continuing.
- Repo is not a GMP, QA, EDMS, eCTD publishing, or official system of record.
- Do not store confidential, signed, GMP raw, QA-approved, or official submission records in this repo.

## Recommended next step

Do not immediately build a runtime generator.

Recommended next PR:

```text
PR #100 — Add report template contract
```

Recommended scope of PR #100:

- Docs/spec only.
- Define fixed memo sections.
- Define required input fields.
- Define required output fields.
- Define source coverage status labels.
- Define company/sponsor association fields.
- Define acceptance criteria before runtime implementation.

Do not implement runtime generator in PR #100.

Recommended file candidate:

```text
docs/regulatory_clinical_digest_report_template_contract.md
```

Likely README/test updates:

```text
README.md
tests/test_readme_documentation_index.py
```

## Direction options for the next chat

Option A — recommended:

```text
Create PR #100: Add regulatory-clinical digest report template contract.
```

Option B:

```text
Run another dry-run memo with a clean requested-source scenario, e.g. TFDA + ClinicalTrials.gov only, to validate clean-source behavior.
```

Option C:

```text
Pause product workflow and update `.ai/PROJECT_STATE.md` to align with PR #97–#99 and dry-run validation.
```

Option D — defer until later:

```text
Design runtime report generator.
```

This should be deferred until the report template contract is accepted.

## New-chat opening prompt

請根據 GitHub repo `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`、`.ai/PROJECT_STATE.md`、以及 `PROJECT_STATE_CONTINUATION.md` 繼續。

請用繁體中文回覆，不要輸出日文。

請先確認：

1. `main` 是否已包含 PR #99；
2. `PROJECT_STATE_CONTINUATION.md` 是否已記錄 PR #97–#99 和 dry-run validation；
3. 是否有 open PR；
4. 最新測試狀態；
5. 是否需要先做 direction calibration。

目前建議下一步是：

`PR #100 — Add regulatory-clinical digest report template contract`

請維持 docs/spec-only，不要新增 runtime generator、MCP tool、source、scheduler、dashboard、alerts、persistence、HTTP/SSE、`.mcp.json`、company alias database、corporate-family mapping、product ownership inference、literature/patent/finance/news integration，除非我明確批准。
