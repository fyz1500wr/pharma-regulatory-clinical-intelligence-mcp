# CMC Submission Readiness Mock Inventory

## Purpose

This document provides a non-confidential mock inventory and dry-run example for the CMC submission readiness mapping workflow.

It validates whether `docs/cmc_submission_readiness_mapping_workflow.md` can turn a small set of CMC work items into a practical PM/RA readiness view, including Module 3 gaps, vendor follow-up items, method/stability dependencies, critical path items, and next actions.

## Data Classification

| Field | Value |
|---|---|
| Data type | Mock / synthetic / non-confidential |
| Real product data | No |
| Real vendor data | No |
| Real GMP data | No |
| Real QA-approved record | No |
| Official submission content | No |
| Intended use | Workflow validation and PM/RA dry-run only |

Do not replace the mock items below with confidential, signed, GMP raw, QA-approved, official submission, or non-public company records in this repository.

## Non-Expansion Statement

This document does not add runtime implementation, MCP tools, scheduler, dashboard, alerts, persistence, HTTP/SSE transport, `.mcp.json`, GitHub automation, source expansion, literature/patent/finance/news integration, company alias database, corporate-family mapping, or product ownership inference.

It also does not create an official IND/eCTD submission, eCTD publisher, GMP/QA record system, EDMS, vendor dashboard, or management decision system.

## Mock Project Context

| Field | Mock Value |
|---|---|
| Project name | Mock IFN Oral Lozenge CMC Readiness Exercise |
| Submission phase | Phase 2 IND readiness planning |
| Review date | 2026-06-08 |
| Reviewer role | PM/RA working review |
| Product type | Recombinant protein drug product, mock example |
| Dosage form | Oral lozenge, mock example |
| Data source | Synthetic task inventory only |

This project context is intentionally generic and should not be treated as a real submission package.

## Mock Task Inventory

| Task ID | Area | Mock Work Item | Current Status | Owner | Due Date | Evidence Needed | Notes |
|---|---|---|---|---|---|---|---|
| CMC-001 | Drug Substance | DS specification table requires CMC/RA review | DRAFT_NEEDS_REVIEW | CMC / RA | 2026-06-21 | Draft DS specification and acceptance-criteria rationale | Acceptance criteria need phase-appropriate justification. |
| CMC-002 | Drug Product | DP potency assay qualification report pending | DATA_PENDING | Analytical / external lab | 2026-06-28 | Qualification summary, curve model, matrix effect review | Assay result affects DP release and stability interpretation. |
| CMC-003 | Stability | DP stability report pending | DATA_PENDING | Stability / external lab | 2026-07-05 | Stability tables, trend review, conclusions | Missing report may block Module 3 readiness summary. |
| CMC-004 | Reference Standard | Working reference standard qualification status unknown | UNKNOWN_REQUIRES_TRIAGE | Analytical | 2026-06-18 | Standard qualification memo, CoA, potency assignment basis | Potency linkage must be clear before final assay summary. |
| CMC-005 | Vendor | Vendor COA package delayed | VENDOR_BLOCKED | Vendor manager / CDMO | 2026-06-24 | Executed COA package and batch traceability summary | Delay may affect both DS and DP evidence package. |
| CMC-006 | Excipient / DP Development | Excipient change rationale decision pending | DECISION_PENDING | CMC / QA / RA | 2026-06-25 | Change rationale, comparability bridge, compendial status | Human decision needed on whether additional bridging is required. |
| CMC-007 | Manufacturing | DP manufacturing process description needs update | DRAFT_NEEDS_REVIEW | CMC / CDMO | 2026-07-01 | Updated process flow and in-process control summary | Depends on CDMO confirmation of process parameters. |
| CMC-008 | Container Closure | DP container closure justification incomplete | DATA_PENDING | CMC | 2026-07-08 | Packaging description, compatibility rationale | Not yet known whether this affects critical path. |

## Module 3 Gap Matrix Dry-Run

| CTD Section | Mock Item | Status | Owner | Dependency | Critical Path | Gap / Risk | Next Action |
|---|---|---|---|---|---|---|---|
| 3.2.S.4 Control of Drug Substance | DS specification table | DRAFT_NEEDS_REVIEW | CMC / RA | specification | yes | Acceptance criteria may be insufficiently justified for phase. | Review specification table and document phase-appropriate rationale. |
| 3.2.P.5 Control of Drug Product | DP potency assay qualification | DATA_PENDING | Analytical / external lab | method | yes | Assay qualification affects release and stability confidence. | Confirm report delivery date and matrix effect interpretation. |
| 3.2.P.8 Stability | DP stability report | DATA_PENDING | Stability / external lab | stability | yes | Stability summary cannot be finalized without trend review. | Confirm available timepoints, report timeline, and interim summary option. |
| 3.2.S.5 Reference Standards | Working reference standard qualification | UNKNOWN_REQUIRES_TRIAGE | Analytical | reference_standard | unknown | Potency assignment basis is unclear. | Confirm qualification status and link to assay unitage. |
| 3.2.P.4 Control of Excipients | Excipient change rationale | DECISION_PENDING | CMC / QA / RA | quality, regulatory | possible | Change rationale may require bridging or additional justification. | Hold CMC/QA/RA decision meeting and document outcome. |
| 3.2.P.3 Manufacture | DP manufacturing process description | DRAFT_NEEDS_REVIEW | CMC / CDMO | manufacturing, vendor | yes | Process description may not match current CDMO process. | Request CDMO confirmation and update process flow. |
| 3.2.P.7 Container Closure | DP container closure justification | DATA_PENDING | CMC | container_closure | unknown | Compatibility rationale incomplete. | Triage whether the gap is critical for target submission phase. |

## Vendor Follow-Up List

| Vendor Follow-Up ID | Vendor Role | Related Task | Owner | Due Date | Critical Path | Follow-Up Question | Escalation Needed |
|---|---|---|---|---|---|---|---|
| VF-001 | External assay lab | DP potency assay qualification | Analytical lead | 2026-06-28 | yes | Can the qualification summary and matrix effect assessment be delivered by the target date? | yes |
| VF-002 | External stability lab | DP stability report | Stability lead | 2026-07-05 | yes | Which timepoints are complete, and can an interim trend summary be issued? | yes |
| VF-003 | CDMO | Vendor COA package | Vendor manager | 2026-06-24 | yes | When will the complete COA and batch traceability package be available? | yes |
| VF-004 | CDMO | DP manufacturing process description | CMC lead | 2026-07-01 | yes | Please confirm current process flow, IPCs, and parameter ranges for the draft Module 3 description. | yes |

## Method And Stability Dependency Map

| Dependency ID | Dependency Type | Upstream Item | Downstream Impact | Risk If Delayed | Mitigation |
|---|---|---|---|---|---|
| DEP-001 | method | DP potency assay qualification | DP specification, DP release, DP stability interpretation | Cannot support DP control strategy narrative. | Request preliminary qualification summary and define interim caveat wording. |
| DEP-002 | stability | DP stability report | 3.2.P.8 stability summary and commitments | Module 3 stability readiness remains incomplete. | Confirm available timepoints and create interim stability status table. |
| DEP-003 | reference_standard | Working standard qualification | Potency assay linkage and report interpretation | Potency unitage and comparability may be unclear. | Confirm standard qualification and bridge to assay method. |
| DEP-004 | vendor | COA package | DS/DP batch evidence package | Batch traceability and release evidence incomplete. | Escalate vendor due date and track daily until received. |

## Critical Path Summary

Overall readiness status for this mock dry-run:

```text
YELLOW / AT RISK
```

Primary critical path items:

1. DP potency assay qualification report pending.
2. DP stability report pending.
3. Vendor COA package delayed.
4. DP manufacturing process description awaiting CDMO confirmation.
5. DS specification table requires CMC/RA review.

Items requiring triage before critical path classification:

1. Working reference standard qualification status.
2. DP container closure justification.
3. Excipient change bridging requirement.

## PM Next-Action List

| Action ID | Action | Owner | Due Date | Blocked By | Critical Path | Module 3 Section | Evidence Needed | Escalation Needed |
|---|---|---|---|---|---|---|---|---|
| ACT-001 | Confirm DP potency assay qualification report delivery and interim summary option. | Analytical lead | 2026-06-18 | External lab | yes | 3.2.P.5 | Qualification summary and matrix effect interpretation | yes |
| ACT-002 | Request DP stability interim trend table and final report timeline. | Stability lead | 2026-06-19 | External lab | yes | 3.2.P.8 | Stability tables and trend summary | yes |
| ACT-003 | Escalate delayed vendor COA package. | Vendor manager | 2026-06-17 | CDMO | yes | 3.2.S / 3.2.P support | COA package and batch traceability | yes |
| ACT-004 | Schedule CMC/RA review of DS specification table. | CMC lead | 2026-06-20 | Internal review | yes | 3.2.S.4 | Specification table and rationale | no |
| ACT-005 | Confirm reference standard qualification and potency assignment basis. | Analytical lead | 2026-06-18 | Internal analytical records | unknown | 3.2.S.5 / 3.2.P.6 | Qualification memo and CoA | possible |
| ACT-006 | Decide whether excipient change requires bridging justification. | CMC / QA / RA | 2026-06-25 | Decision meeting | possible | 3.2.P.4 / 3.2.P.2 | Change rationale and compendial status | possible |
| ACT-007 | Request CDMO confirmation of DP process flow and IPCs. | CMC lead | 2026-06-21 | CDMO | yes | 3.2.P.3 | Process flow and IPC summary | yes |

## Human Review Checklist Result

| Checklist Item | Mock Result | Comment |
|---|---|---|
| Module 3 section mapping reviewed by CMC/RA | Pending | Needs human review before use. |
| Vendor actions have owners and due dates | Pass | Vendor owner and due dates are listed. |
| Critical path items separated from non-critical items | Pass with limitation | Some items remain unknown and need triage. |
| Missing evidence separated from evidence pending review | Pass | DATA_PENDING vs DRAFT_NEEDS_REVIEW are separated. |
| Method/stability dependencies separated from routine testing | Pass | DEP-001 and DEP-002 are explicit. |
| Stability gaps explicitly listed | Pass | DP stability report and interim table are listed. |
| Specification gaps explicitly listed | Pass | DS specification gap is listed. |
| Reference standard gaps explicitly listed | Pass | Working standard qualification is listed. |
| Quality/change/risk decisions not hidden | Pass | Excipient change decision is explicit. |
| No confidential/GMP/QA/submission records stored | Pass | Mock-only document. |
| Output labeled as PM/RA working intelligence only | Pass | Stated throughout document. |

## Dry-Run Conclusion

This mock inventory supports the conclusion that the CMC submission readiness mapping workflow can convert a small CMC task set into a PM-usable readiness view.

The workflow is most useful for:

- identifying Module 3 gaps,
- separating vendor-blocked items from internal review items,
- highlighting method and stability dependencies,
- identifying critical path items,
- converting gaps into PM follow-up actions.

The mock dry-run also shows that readiness automation should not be built yet. Before automation, the next practical improvement would be a reusable template or prompt pack for collecting non-confidential CMC task inventory inputs.

## Explicit Non-Goals

This mock inventory does not:

- replace CMC, RA, QA, legal, medical, or management review,
- create official submission content,
- create signed CTD Module 3 text,
- store GMP raw data, signed reports, QA-approved records, or official submission content,
- determine regulatory acceptability,
- create a vendor dashboard or alert system,
- create runtime automation,
- create a new MCP tool,
- add sources or integrations.
