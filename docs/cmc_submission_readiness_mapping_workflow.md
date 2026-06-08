# CMC Submission Readiness Mapping Workflow

## Purpose

This document defines a docs/spec-only workflow for mapping CMC project work into early-phase submission readiness, eCTD Module 3 readiness, vendor dependencies, critical path items, and PM follow-up actions.

The workflow is intended for PM/RA planning support. It does not create an official regulatory submission package, GMP record, QA-approved record, EDMS record, or eCTD publishing system.

## Scope Status

| Area | Status |
|---|---|
| Workflow type | Documentation/specification only |
| Runtime implementation | Not implemented |
| MCP tool | Not added |
| Scheduler / dashboard / alerts | Not added |
| Persistence layer | Not added |
| eCTD publisher | Not added |
| GMP / QA record system | Not added |
| Source expansion | Not added |

## Non-Expansion Statement

This workflow does not add new sources, tools, scheduler, alerts, dashboard, persistence, HTTP/SSE transport, `.mcp.json`, GitHub automation, literature/patent/finance/news integration, company alias database, corporate-family mapping, or product ownership inference.

It also does not store confidential, signed, GMP raw, QA-approved, official submission, or non-public company records in this repository.

## Intended Users

| User | Intended Use |
|---|---|
| CMC PM | Track CMC readiness gaps, vendor blockers, and critical path. |
| RA / Regulatory CMC reviewer | Map evidence readiness to Module 3 sections and submission questions. |
| CMC lead | Prioritize method, stability, manufacturing, and vendor follow-up. |
| Vendor manager | Track CDMO/CRO/lab dependencies and due dates. |
| Executive reviewer | Review red/yellow/green readiness status and key blockers. |

## Input Object

A future implementation, if explicitly approved, should use an input object like the following. This document only defines the contract.

| Field | Required? | Description |
|---|---:|---|
| `project_name` | Yes | Internal project or product name. Do not include confidential identifiers unless approved. |
| `submission_phase` | Yes | Example: pre-IND, IND-enabling, Phase 1, Phase 2, post-approval. |
| `target_submission_date` | Optional | Planned submission or internal readiness target date. |
| `dosage_form` | Optional | Drug product dosage form or modality summary. |
| `drug_substance_type` | Optional | Small molecule, peptide, protein, biologic, cell therapy, gene therapy, etc. |
| `module3_sections_in_scope` | Yes | Target CTD/eCTD Module 3 sections. |
| `task_inventory` | Yes | Current CMC task list or GitHub Project task export. |
| `vendor_inventory` | Optional | CDMO/CRO/lab/vendor list and responsibilities. |
| `document_inventory` | Optional | Draft protocols, reports, COAs, specifications, methods, validation summaries, stability tables. |
| `known_blockers` | Optional | Known blockers, unresolved deviations, data gaps, vendor delays, or missing decisions. |
| `review_date` | Yes | Date of readiness review. |
| `reviewer` | Optional | Human reviewer role or name. |

## Readiness Mapping Dimensions

Each CMC item should be mapped across five dimensions.

| Dimension | Purpose |
|---|---|
| Evidence readiness | Whether the required data/report/document exists and is reviewable. |
| Module 3 placement | Where the item belongs in CTD/eCTD Module 3. |
| Dependency status | Whether the item depends on vendor, method, stability, manufacturing, QA, or RA input. |
| Critical path status | Whether a delay affects the target submission/readiness date. |
| Decision status | Whether a human decision or escalation is required. |

## Module 3 Readiness Map

Use this controlled mapping as a starting structure.

| CTD Section | Readiness Question | Typical Evidence | Common Blockers |
|---|---|---|---|
| 3.2.S.1 General Information | Is the drug substance identity and nomenclature defined? | Structure/sequence, general properties, manufacturer role. | Ambiguous naming, incomplete sequence/identity evidence. |
| 3.2.S.2 Manufacture | Is the DS manufacturing process sufficiently described? | Process description, process flow, controls, batch history. | Missing vendor process detail, unclear in-process controls. |
| 3.2.S.3 Characterisation | Are structure, impurities, and product-related variants sufficiently characterized? | Characterization reports, impurity/variant data, orthogonal methods. | Missing orthogonal characterization, unclear impurity attribution. |
| 3.2.S.4 Control of Drug Substance | Are DS specifications, analytical methods, and validation/qualification status ready? | Specification table, method summaries, validation/qualification reports, COAs. | Method not qualified/validated, acceptance criteria not justified. |
| 3.2.S.5 Reference Standards | Are reference standards and qualification status defined? | Reference standard qualification, CoA, bridging rationale. | Working standard not qualified, missing potency linkage. |
| 3.2.S.6 Container Closure | Is DS container closure and storage justified? | Container description, compatibility, storage conditions. | Missing compatibility or hold-time data. |
| 3.2.S.7 Stability | Is DS stability package adequate for phase and storage condition? | Stability protocol, tables, trends, conclusions, commitments. | Missing long-term data, unexplained OOS/OOT trends. |
| 3.2.P.1 Description and Composition | Is DP composition and dosage form defined? | Composition table, excipient function, manufacturing formula. | Excipient change not justified, unclear overage or potency basis. |
| 3.2.P.2 Pharmaceutical Development | Is formulation/process rationale adequate? | Development report, compatibility, process selection rationale. | Weak link between formulation choice and product performance. |
| 3.2.P.3 Manufacture | Is DP manufacturing process sufficiently described? | Batch formula, process flow, controls, batch records summary. | Missing manufacturing controls or vendor process details. |
| 3.2.P.4 Control of Excipients | Are excipient standards and compendial/non-compendial controls defined? | Excipient specs, CoAs, compendial references. | Supplier change, non-compendial grade, missing justification. |
| 3.2.P.5 Control of Drug Product | Are DP specs, analytical methods, and validation/qualification status ready? | Specification table, method summaries, validation/qualification reports, COAs. | Method not qualified/validated, matrix effect unresolved. |
| 3.2.P.6 Reference Standards | Are DP assay standards and bridging defined? | Standard qualification, potency assignment, bridging. | Potency standard not linked to method or unitage. |
| 3.2.P.7 Container Closure | Is DP container closure defined and justified? | Packaging description, compatibility, protection rationale. | Missing compatibility, leachables/extractables question unresolved. |
| 3.2.P.8 Stability | Is DP stability package adequate for phase and storage condition? | Protocol, stability tables, trends, conclusions, commitments. | Missing timepoints, unresolved assay variability, storage change. |
| 3.2.A / Appendices | Are facilities, adventitious agent safety, or other appendices needed? | Facility information, viral safety, special appendices. | Incorrect assumption that appendix is not needed. |
| 3.2.R Regional Information | Are regional administrative or country-specific items needed? | Regional forms or local quality attachments. | Local requirement missed. |

## Readiness Status Labels

Use a conservative status label for each item.

| Status | Definition |
|---|---|
| `READY_FOR_REVIEW` | Evidence exists and can be reviewed by CMC/RA. |
| `DRAFT_NEEDS_REVIEW` | Draft exists but needs technical, QA, or RA review. |
| `DATA_PENDING` | Data generation is ongoing or not yet received. |
| `VENDOR_BLOCKED` | Vendor response, report, COA, method, or batch record is blocking readiness. |
| `DECISION_PENDING` | Human decision is required before work can progress. |
| `RISK_ACCEPTANCE_NEEDED` | Gap may remain and needs explicit risk acceptance or mitigation. |
| `NOT_APPLICABLE_WITH_RATIONALE` | Item is not applicable and the rationale is documented. |
| `UNKNOWN_REQUIRES_TRIAGE` | Status is not known and must be clarified. |

## Critical Path Rules

Mark `critical_path = yes` when any of the following are true:

- The item blocks submission-readiness or Module 3 completion.
- The item blocks method validation/qualification.
- The item blocks stability protocol finalization, stability pull, or stability report.
- The item blocks DS/DP specification finalization.
- The item blocks batch release or batch usability.
- The item requires vendor data that cannot be recreated internally within the required timeline.
- The item requires RA/CMC decision before other downstream work can proceed.

Mark `critical_path = no` when the item is useful but does not affect the target readiness date.

Mark `critical_path = unknown` when dependency information is incomplete.

## Dependency Categories

Use one or more dependency categories.

| Dependency | Examples |
|---|---|
| `vendor` | CDMO, CRO, assay vendor, supplier, logistics vendor. |
| `method` | Method development, transfer, qualification, validation, bridging. |
| `stability` | Protocol, pull, testing, trend, report, commitment. |
| `manufacturing` | DS/DP batch, process description, batch record, IPC, deviation. |
| `specification` | DS/DP specification, acceptance criteria, justification. |
| `reference_standard` | Standard qualification, potency assignment, bridging. |
| `quality` | QA review, deviation, change control, OOS/OOT, audit. |
| `regulatory` | RA strategy, agency expectation, Module 3 placement, regional item. |
| `management_decision` | Resourcing, timeline, vendor selection, risk acceptance. |

## Output Object

A future approved implementation should produce an output object with these sections.

| Output Field | Description |
|---|---|
| `readiness_summary` | Overall R/Y/G readiness summary with caveats. |
| `module3_gap_matrix` | Module 3 section-by-section readiness and evidence gap matrix. |
| `critical_path_items` | Items blocking target readiness date. |
| `vendor_follow_up_items` | Vendor-owned actions and due dates. |
| `method_and_stability_dependencies` | Method/stability items that affect readiness. |
| `decision_log_needed` | Human decisions required before progress. |
| `risk_acceptance_candidates` | Items that may require formal risk acceptance. |
| `pm_next_actions` | Practical PM follow-up actions. |
| `review_limitations` | Known limitations and missing source material. |
| `human_review_checklist` | Checklist for PM/CMC/RA review before management use. |

## Example Module 3 Gap Matrix

| CTD Section | Item | Status | Owner | Dependency | Critical Path | Next Action |
|---|---|---|---|---|---|---|
| 3.2.S.4 | DS specification table | DRAFT_NEEDS_REVIEW | CMC/RA | specification | yes | Confirm acceptance criteria and justification. |
| 3.2.P.5 | DP potency assay qualification | DATA_PENDING | Analytical / vendor | method | yes | Confirm qualification report due date and matrix effect status. |
| 3.2.P.8 | DP stability report | DATA_PENDING | Stability / vendor | stability | yes | Confirm available timepoints and reporting date. |
| 3.2.S.5 | Working standard qualification | UNKNOWN_REQUIRES_TRIAGE | Analytical | reference_standard | unknown | Confirm standard status and potency assignment basis. |
| 3.2.P.4 | Excipient supplier change rationale | DECISION_PENDING | CMC / QA / RA | quality, regulatory | possible | Decide whether bridging justification is needed. |

## Example PM Readiness Summary

```text
Overall CMC readiness is YELLOW.

The main readiness blockers are DP potency assay qualification, DP stability reporting, and DS/DP specification finalization. Vendor-owned dependencies should be escalated because delay may affect the target submission-readiness date.

This summary is a PM/RA working-intelligence draft. It does not replace CMC technical review, QA review, signed reports, GMP records, or official regulatory submission content.
```

## PM Follow-Up Action Format

Each follow-up action should include:

| Field | Required? | Description |
|---|---:|---|
| `action_id` | Yes | Short tracking identifier. |
| `action` | Yes | Concrete follow-up action. |
| `owner` | Yes | Person, function, or vendor owner. |
| `due_date` | Optional | Target completion date. |
| `blocked_by` | Optional | Dependency or blocker. |
| `critical_path` | Yes | yes / no / unknown. |
| `module3_section` | Optional | Relevant CTD/eCTD Module 3 section. |
| `evidence_needed` | Optional | Specific report, protocol, data table, COA, or decision record. |
| `escalation_needed` | Optional | yes / no / unknown. |

## Human Review Checklist

Before using a readiness summary for PM, RA, or management discussion, confirm:

- [ ] Module 3 section mapping has been reviewed by a qualified CMC/RA reviewer.
- [ ] All vendor-owned actions have owners and due dates.
- [ ] Critical path items are separated from non-critical housekeeping items.
- [ ] Missing evidence is clearly distinguished from evidence that is complete but pending review.
- [ ] Method qualification/validation dependencies are separated from routine testing.
- [ ] Stability data gaps, OOS/OOT issues, and reporting dates are explicitly listed.
- [ ] Specification and acceptance-criteria gaps are explicitly listed.
- [ ] Reference standard and potency assignment gaps are explicitly listed.
- [ ] Quality issues, deviations, changes, or risk acceptances are not hidden in summary wording.
- [ ] No confidential, signed, GMP raw, QA-approved, or official submission records are stored in this repository.
- [ ] The output is labeled as PM/RA working intelligence only.

## Acceptance Criteria Before Runtime Implementation

Do not build runtime automation for this workflow unless all of the following are explicitly approved and validated:

1. The user approves moving beyond docs/spec-only.
2. A sample non-confidential CMC task inventory is defined.
3. A sample Module 3 mapping exercise is reviewed by the user.
4. Status labels and critical path rules are stable enough for repeated use.
5. Confidentiality boundaries are documented.
6. The output is clearly labeled as working intelligence, not official submission content.
7. The implementation does not add unauthorized sources, storage, dashboards, alerts, scheduler, or repository automation.

## Explicit Non-Goals

This workflow does not:

- create an official IND or eCTD submission
- generate signed CTD Module 3 text
- replace CMC, QA, RA, legal, medical, or management review
- store GMP raw data, signed reports, QA-approved records, or official submission content
- create vendor dashboards or alerts
- create persistence or database tables
- create GitHub automation
- add literature, patent, finance, or news integrations
- infer product ownership or corporate-family relationships
- expand source scope beyond approved MVP boundaries
