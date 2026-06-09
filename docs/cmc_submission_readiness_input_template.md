# CMC Submission Readiness Input Template and Prompt Pack

## Purpose

This document provides a reusable docs/spec-only input template and prompt pack for collecting non-confidential CMC readiness information and turning it into a consistent PM/RA working-intelligence output.

It builds on:

```text
docs/cmc_submission_readiness_mapping_workflow.md
docs/cmc_submission_readiness_mock_inventory.md
```

The goal is to reduce inconsistent input formatting and help reviewers consistently identify Module 3 gaps, vendor blockers, method/stability dependencies, critical path items, and PM next actions.

## Data Boundary

Use this template only with non-confidential or properly de-identified working information.

Do not paste or store the following in this repository:

- confidential product details,
- non-public vendor confidential records,
- signed reports,
- GMP raw data,
- QA-approved records,
- official submission content,
- batch records,
- executed COAs,
- controlled documents,
- personal data.

Outputs generated from this template are PM/RA working intelligence only. They do not replace CMC, QA, RA, legal, medical, or management review.

## Non-Expansion Statement

This template and prompt pack does not add runtime implementation, MCP tools, scheduler, dashboard, alerts, persistence, HTTP/SSE transport, `.mcp.json`, GitHub automation, source expansion, literature/patent/finance/news integration, company alias database, corporate-family mapping, or product ownership inference.

It also does not create an official IND/eCTD submission, eCTD publisher, GMP/QA record system, EDMS, vendor dashboard, alert system, or management decision system.

## Input Package Structure

Prepare the input package with these sections.

```text
1. Project context
2. CMC task inventory
3. Vendor dependency inventory
4. Method and stability dependency inventory
5. Known decisions and unresolved questions
6. Evidence inventory
7. Timeline assumptions
8. Requested output
```

## 1. Project Context Template

| Field | Input |
|---|---|
| Project name or code |  |
| Review date |  |
| Review purpose |  |
| Submission phase |  |
| Target readiness date |  |
| Product type / modality |  |
| Dosage form |  |
| Reviewer role |  |
| Data confidentiality status | Non-confidential / de-identified / mock |
| Explicit exclusions |  |

Recommended review purpose examples:

- Phase 1 IND readiness planning
- Phase 2 IND readiness planning
- CMC gap triage
- Vendor follow-up planning
- Management weekly readiness review
- Module 3 evidence completeness review

## 2. CMC Task Inventory Template

| Task ID | CTD Section | Area | Work Item | Status | Owner | Due Date | Evidence Needed | Dependency | Critical Path | Risk / Blocker | Next Action |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CMC-001 | 3.2.S.4 | DS control |  |  |  |  |  |  | yes / no / unknown |  |  |
| CMC-002 | 3.2.P.5 | DP control |  |  |  |  |  |  | yes / no / unknown |  |  |
| CMC-003 | 3.2.P.8 | Stability |  |  |  |  |  |  | yes / no / unknown |  |  |

Use controlled status labels from the readiness workflow whenever possible:

| Status | Use When |
|---|---|
| READY_FOR_REVIEW | Evidence exists and can be reviewed by CMC/RA. |
| DRAFT_NEEDS_REVIEW | Draft exists but needs technical, QA, or RA review. |
| DATA_PENDING | Data generation is ongoing or not yet received. |
| VENDOR_BLOCKED | Vendor response, report, COA, method, or batch information is blocking readiness. |
| DECISION_PENDING | Human decision is required before progress. |
| RISK_ACCEPTANCE_NEEDED | Gap may remain and needs explicit risk acceptance or mitigation. |
| NOT_APPLICABLE_WITH_RATIONALE | Item is not applicable and rationale is documented. |
| UNKNOWN_REQUIRES_TRIAGE | Status is not known and must be clarified. |

## 3. Vendor Dependency Inventory Template

| Vendor Item ID | Vendor Role | Related Task ID | Required Output | Current Status | Owner | Due Date | Blocking Impact | Escalation Needed | Follow-Up Question |
|---|---|---|---|---|---|---|---|---|---|
| VF-001 | CDMO / CRO / lab / supplier |  |  |  |  |  |  | yes / no / unknown |  |

Common vendor outputs:

- COA package summary,
- method report summary,
- stability report summary,
- process description confirmation,
- in-process control summary,
- raw-material or excipient statement,
- batch traceability summary,
- deviation or investigation status summary.

Do not paste executed GMP records or signed QA-approved vendor records into this repository.

## 4. Method And Stability Dependency Template

| Dependency ID | Type | Upstream Item | Downstream Impact | Related CTD Section | Risk If Delayed | Mitigation / Interim Option |
|---|---|---|---|---|---|---|
| DEP-001 | method |  |  |  |  |  |
| DEP-002 | stability |  |  |  |  |  |

Suggested dependency types:

```text
method
stability
manufacturing
specification
reference_standard
vendor
quality
regulatory
management_decision
```

## 5. Decision And Open Question Template

| Decision ID | Question | Owner | Due Date | Related Task | Impact If Unresolved | Proposed Decision Path |
|---|---|---|---|---|---|---|
| DEC-001 |  |  |  |  |  |  |

Use this section for items that need a human decision, not just more data.

Examples:

- Is additional bridging needed for an excipient or supplier change?
- Is a method qualification summary enough for the target phase?
- Is interim stability data acceptable for the internal readiness milestone?
- Is a gap a true blocker or a documented limitation?

## 6. Evidence Inventory Template

| Evidence ID | Evidence Type | Related Task | Current Location / Holder | Status | Review Needed | Notes |
|---|---|---|---|---|---|---|
| EVD-001 | protocol / report / CoA summary / specification / memo |  |  |  | CMC / RA / QA / other |  |

Allowed evidence descriptions should be summaries or placeholders only. Do not store controlled source records in this repository.

## 7. Timeline Assumption Template

| Milestone | Target Date | Confidence | Dependencies | Notes |
|---|---|---|---|---|
| Internal CMC readiness review |  | high / medium / low |  |  |
| Module 3 draft package review |  | high / medium / low |  |  |
| Vendor evidence receipt |  | high / medium / low |  |  |

## Requested Output Template

When asking an AI assistant to analyze the input package, request these outputs:

```text
1. Overall readiness summary
2. Module 3 gap matrix
3. Critical path summary
4. Vendor follow-up list
5. Method and stability dependency map
6. Decision log
7. PM next-action list
8. Human review checklist
9. Limitations and assumptions
```

## Prompt Pack

### Prompt 1 — Generate CMC Readiness Assessment

```text
You are supporting PM/RA CMC readiness planning.

Use the provided non-confidential CMC input package to generate a working-intelligence readiness assessment.

Required outputs:
1. Overall readiness summary with R/Y/G status.
2. Module 3 gap matrix.
3. Critical path summary.
4. Vendor follow-up list.
5. Method and stability dependency map.
6. Decision log.
7. PM next-action list.
8. Human review checklist.
9. Limitations and assumptions.

Rules:
- Do not invent missing evidence.
- Distinguish DATA_PENDING from DRAFT_NEEDS_REVIEW.
- Distinguish VENDOR_BLOCKED from internal review items.
- Mark critical path as yes/no/unknown with rationale.
- Preserve Module 3 section mapping uncertainty.
- Label the output as PM/RA working intelligence only.
- Do not treat the output as official submission content, GMP record, QA-approved record, or management decision.
```

### Prompt 2 — Convert Inventory To Module 3 Gap Matrix

```text
Convert the provided CMC task inventory into a Module 3 gap matrix.

For each item, include:
- CTD section,
- work item,
- status,
- owner,
- dependency type,
- critical path yes/no/unknown,
- evidence gap,
- risk if unresolved,
- next action.

Use conservative wording. If CTD placement is uncertain, mark it as uncertain rather than guessing.
```

### Prompt 3 — Identify Vendor Blockers

```text
Review the CMC input package and identify vendor-owned blockers.

Create a vendor follow-up list with:
- vendor role,
- related task,
- required output,
- due date,
- blocking impact,
- escalation status,
- precise follow-up question.

Do not request confidential raw records in the output. Ask for summaries, status confirmation, or controlled-document review pathways instead.
```

### Prompt 4 — Build Critical Path Summary

```text
From the CMC task inventory, identify critical path items.

Classify each item as:
- critical path = yes,
- critical path = no,
- critical path = unknown.

For each yes or unknown item, explain:
- why it may block readiness,
- which downstream output is affected,
- what decision or evidence is needed,
- what mitigation or interim option exists.
```

### Prompt 5 — Generate PM Next Actions

```text
Generate a PM next-action list from the provided CMC readiness input.

Each action must include:
- action ID,
- action,
- owner,
- due date if available,
- blocker/dependency,
- critical path status,
- related Module 3 section,
- evidence needed,
- escalation needed yes/no/unknown.

Keep actions concrete and follow-up oriented. Avoid generic statements such as "continue monitoring" unless paired with a specific owner and date.
```

### Prompt 6 — Management Summary And Weekly Reporting Stress Test

```text
Create a management-ready CMC readiness summary using the provided working-intelligence output.

Use this prompt for a single management summary or for a weekly management-readiness stress test. Keep the output concise and executive-ready, but preserve CMC/RA caveats and avoid overstating readiness.

Required format:
1. Report context
   - Review date.
   - Reporting period, if provided.
   - Submission phase.
   - Target readiness date.
   - Data boundary: non-confidential / de-identified / mock.

2. One-sentence executive summary
   - State the overall readiness status and the main reason in one sentence.

3. Overall status
   - Current R/Y/G status.
   - Prior R/Y/G status, if provided.
   - Status movement: improved / unchanged / worsened / unknown.
   - Movement reason.

4. Top management concerns
   - List the top 3 management-level concerns only.
   - For each concern, include why it matters for readiness.
   - Do not include technical housekeeping items unless they affect readiness date, vendor escalation, or management decision.

5. Critical path movement
   - True critical-path blockers.
   - Possible critical-path blockers.
   - Unknown critical-path items requiring triage.
   - Items that should not be treated as critical path, with rationale.

6. Decisions needed this week
   - Decision.
   - Owner.
   - Due date.
   - Impact if unresolved.
   - Whether management input is needed.

7. Vendor escalations
   - Vendor role.
   - Related task.
   - Required output.
   - Due date.
   - Escalation status.
   - Exact follow-up question.
   - State whether the request is for summary/status only and not for raw GMP, executed, signed, or vendor-confidential records.

8. Completed this week
   - List completed actions if provided.
   - If not provided, state that completed-this-week data was not included in the input.
   - Do not invent completed actions.

9. Next-week priorities
   - List concrete next-week priorities.
   - Include owner and due date where available.
   - Mark unknown owner or due date explicitly rather than inventing them.

10. Items not suitable for management escalation
   - List technical CMC/RA/QA review items that should remain at working-team level.
   - Provide a short rationale for not escalating.

11. Assumptions and caveats
   - State input limitations.
   - State that the output is PM/RA working intelligence only.
   - State that it is not final CMC, QA, regulatory, or management decision-making output.
   - State that missing evidence remains missing and requires human review.

12. Template adequacy check
   - Assess whether the current CMC readiness input package is sufficient for recurring weekly management reporting.
   - Use PASS / PARTIAL / FAIL.
   - If PARTIAL or FAIL, specify whether the first corrective action should be revising this existing prompt/template or creating a dedicated `docs/cmc_management_weekly_report_template.md`.
   - Do not recommend creating a new repository document unless repeated stress tests or recurring use show a structural gap that cannot reasonably fit in this existing template.

Rules:
- Keep the summary brief and avoid technical overstatement.
- Do not invent missing evidence, due dates, completed actions, vendor responses, or decisions.
- Separate management-level escalation items from technical review items.
- Separate true critical path from review-only housekeeping items.
- Preserve confidentiality boundaries.
- Do not request confidential raw records, signed reports, executed COAs, GMP raw data, batch records, QA-approved records, or vendor confidential records.
- State that the output is a PM/RA working summary, not a final CMC, QA, regulatory, or management decision.
```

### Prompt 7 — Red Flag Review

```text
Review the CMC readiness output for red flags.

Flag any wording that:
- treats missing evidence as completed,
- treats vendor delay as resolved without evidence,
- overstates regulatory acceptability,
- implies QA approval without QA review,
- implies official submission readiness without human review,
- hides critical path uncertainty,
- mixes mock or de-identified data with real confidential records.

Return a table with the risky sentence, why it is risky, and safer replacement wording.
```

## Quality Checklist Before Use

Before using any output generated from this template, confirm:

- [ ] Input data is non-confidential or properly de-identified.
- [ ] No signed, GMP raw, QA-approved, official submission, or controlled records are stored in the repo.
- [ ] Module 3 mapping has been reviewed or marked uncertain.
- [ ] Critical path items are separated from non-critical housekeeping items.
- [ ] Vendor blockers have owners and follow-up questions.
- [ ] Method and stability dependencies are explicit.
- [ ] Decision-needed items are separated from data-pending items.
- [ ] Limitations are visible in the output.
- [ ] Output is labeled PM/RA working intelligence only.

## Expected Use Sequence

Recommended sequence:

```text
1. Fill the input package with non-confidential or de-identified data.
2. Generate a CMC readiness assessment using Prompt 1.
3. Run Prompt 7 red flag review.
4. Revise the output for overstatement and missing limitations.
5. Use Prompt 6 only after the working assessment has been checked.
6. Escalate unresolved critical path and vendor blockers to the appropriate human owners.
```

## Explicit Non-Goals

This template does not:

- create official IND/eCTD content,
- replace CMC, RA, QA, legal, medical, or management review,
- make regulatory acceptability decisions,
- generate signed CTD Module 3 text,
- store controlled records,
- create a dashboard or alert system,
- create runtime automation,
- create a new MCP tool,
- add sources or integrations.
