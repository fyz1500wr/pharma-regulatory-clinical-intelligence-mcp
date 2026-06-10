# Static Dashboard Dry-Run Design

Last updated: 2026-06-10

Status: docs/spec-only design contract. This document defines a mock-data-only static dashboard dry-run design for the regulatory-clinical intelligence dashboard roadmap. It does not implement a dashboard renderer, generator, scheduler, persistence layer, runtime connector, GitHub Actions workflow, MCP tool, `.mcp.json`, alerting, or source expansion.

---

## 1. Purpose

This document defines how to validate the dashboard-first roadmap using controlled mock data before any runtime dashboard implementation is approved.

The dry-run should demonstrate that the schema families defined in `docs/dashboard_data_schema_contract.md` can support dashboard-style review across regulatory/guidance updates, clinical trial updates, source health status, and digest-level summaries.

The dry-run is intended to answer:

1. Can the planned dashboard tabs be populated from the canonical schema families?
2. Can users distinguish source unavailable, no matching records, partial metadata, and human-review-required cases?
3. Can regulatory/guidance and clinical trial content be displayed without implying approval probability, clinical success, commercial strength, or company superiority?
4. Can the static dashboard concept remain compatible with the MVP runtime source scope of FDA, TFDA, and ClinicalTrials.gov only?

---

## 2. Inputs

The dry-run uses mock records only. Mock records should be stored as examples in documentation or future test fixtures only if explicitly approved.

The dry-run input families are:

```text
RegulatoryGuidanceUpdate
ClinicalTrialUpdate
SourceHealthEvent
DashboardDigestSummary
```

The dry-run must not require live FDA, TFDA, ClinicalTrials.gov, EMA, NMPA/CDE, PMDA, ICH, WHO ICTRP, EU CTIS, literature, patent, finance, or news access.

---

## 3. Intended Static Dashboard Tabs

### 3.1 Overview Tab

Purpose:

- Provide a high-level summary of the date window, source coverage, and human-review caveats.
- Surface source-health limitations before detailed interpretation.

Mock input families:

```text
DashboardDigestSummary
SourceHealthEvent
```

Expected sections:

1. Date window and run metadata.
2. Source coverage summary.
3. Source health summary.
4. Human-review-required flags.
5. Key limitation statement.

Acceptance criteria:

- The overview must state when source failures or source limitations affect interpretation.
- The overview must not claim that a source has no updates when source access failed.
- The overview must not include approval probability, clinical success prediction, investment opinion, or company ranking.

### 3.2 Regulatory / Guidance Updates Tab

Purpose:

- Present mock regulatory and guidance update records by source, region, topic, modality, document type, date, and status.

Mock input family:

```text
RegulatoryGuidanceUpdate
```

Expected columns:

```text
record_id
source_name
source_category
region
title
document_type
record_date
topic_tags
modality_tags
guideline_family
guideline_stage_or_status
official_url
source_health_status
human_review_required
limitations
```

Display rules:

- ICH records, when present as mock records, must be shown as global harmonisation guidance, not as a drug-review agency and not as a clinical trial registry.
- Missing attachment URLs must be shown as missing metadata, not as evidence that no attachment exists.
- Draft, final, revision, and adoption statuses must be displayed as source-reported metadata only.

Acceptance criteria:

- Regulatory agency records and global harmonisation guidance records are visually or textually distinguishable.
- Topic and modality tags are displayed as classification aids, not as regulatory conclusions.
- No runtime source expansion is implied.

### 3.3 Clinical Trial Tracker Tab

Purpose:

- Present mock ClinicalTrials.gov-style trial records by indication, sponsor, intervention, phase, recruitment status, results availability, and key dates.

Mock input family:

```text
ClinicalTrialUpdate
```

Expected columns:

```text
record_id
registry_name
registry_id
registry_url
trial_title
indication_terms
sponsor_name
collaborator_names
intervention_names
phase
recruitment_status
study_start_date
primary_completion_date
results_first_posted_date
record_date
source_health_status
human_review_required
limitations
```

Display rules:

- Sponsor names must be shown as registry-reported sponsor names only.
- The dashboard must not infer company alias, corporate family, product ownership, clinical success, approval probability, commercial strength, or company superiority.
- Trials with partial metadata must remain visible with a limitation flag.

Acceptance criteria:

- Trial activity can be filtered or grouped by indication, sponsor, phase, and recruitment status.
- Results availability is shown as registry metadata only.
- Missing or partial fields do not suppress the record unless the mock test explicitly defines exclusion behavior.

### 3.4 Source Health Tab

Purpose:

- Present source availability, parser/API health, source-failure type, and recommended review actions.

Mock input family:

```text
SourceHealthEvent
```

Expected columns:

```text
record_id
source_name
source_category
source_check_status
failure_type
http_status
parser_error_code
schema_or_selector_change_detected
record_count_returned
expected_minimum_record_count
blocks_dashboard_use
recommended_action
retrieved_at
limitations
```

Display rules:

- `pass` means only that the source check passed under the tested condition; it does not prove complete source coverage.
- `failed`, `blocked`, `source_unavailable`, or `parser_changed` must not be interpreted as no matching records.
- FDA abuse-detection or apology responses must be shown as source-access limitations, not as evidence of zero FDA records.

Acceptance criteria:

- Source failures are visible before content interpretation.
- Source health records can explain why a dashboard tab may be incomplete.
- Source health failures can block or qualify dashboard use without deleting underlying mock records.

### 3.5 Digest Summary Tab

Purpose:

- Present a controlled dashboard-level summary that explains what the static dashboard would say and what it cannot conclude.

Mock input family:

```text
DashboardDigestSummary
```

Expected sections:

1. Scope and date window.
2. Regulatory/guidance update summary.
3. Clinical trial update summary.
4. Source health summary.
5. Required human review items.
6. Explicit limitations.

Acceptance criteria:

- Summary text must preserve source limitations and human-review caveats.
- Summary text must not convert mock data into regulatory, clinical, legal, medical, commercial, or management decisions.
- Summary text must be clearly distinguishable from a final report or official submission artifact.

---

## 4. Mock Data Design Rules

Mock data should include enough variation to test dashboard behavior:

1. At least one regulatory agency update record.
2. At least one global harmonisation guidance mock record.
3. At least one clinical trial record with complete metadata.
4. At least one clinical trial record with partial metadata.
5. At least one source health pass event.
6. At least one source unavailable or parser failure event.
7. At least one digest summary that references source limitations.

Mock data must not include confidential, non-public, vendor-confidential, signed, GMP raw, QA-approved, official submission, or personal data.

Mock data may use fictional titles, fictional sponsor names, and fictional URLs, or clearly labeled public/example URLs if appropriate. It must not imply that a fictional product or sponsor has real regulatory status.

---

## 5. Dry-Run Output Artifact Concept

This PR does not implement artifacts. The future dry-run may define one or more static artifacts only after approval.

Possible future artifact shapes:

```text
mock_dashboard_records.json
mock_dashboard_summary.md
mock_dashboard_table.csv
```

These are conceptual only in this document.

This document does not authorize generating, committing, publishing, rendering, scheduling, or hosting dashboard artifacts.

---

## 6. Source Interpretation Rules

The dry-run must preserve the following interpretation rules:

1. Source unavailable is not no result.
2. Parser or schema change is not no result.
3. Source health pass is not proof of full coverage.
4. Missing metadata is not negative evidence.
5. Clinical trial registry sponsor fields are not company ownership inference.
6. ICH is a global harmonisation guidance source, not a clinical trial registry and not a drug-review agency.
7. Dashboard summaries are working intelligence drafts and require human review.

---

## 7. Acceptance Criteria Summary

The static dashboard dry-run design is acceptable when it demonstrates the following without runtime implementation:

- The four canonical dashboard schema families can populate the planned dashboard tabs.
- Source health limitations are shown before or alongside content interpretation.
- Regulatory agency, global harmonisation guidance, and registry records remain distinguishable.
- Partial metadata records can be displayed with limitations.
- Mock summaries preserve human-review caveats.
- The design does not add or imply dashboard rendering, GitHub Actions, scheduling, alerting, persistence, runtime connectors, new MCP tools, `.mcp.json`, source expansion, or external integrations.

---

## 8. Non-Goals

This document does not add or approve:

- Runtime dashboard renderer.
- Static dashboard artifact generator.
- GitHub Actions workflow.
- Scheduler.
- Alerts.
- GitHub Pages publication.
- Persistence layer.
- Runtime source connector.
- New MCP tool.
- `.mcp.json`.
- EMA, NMPA/CDE, PMDA, ICH, WHO ICTRP, or EU CTIS runtime integration.
- Literature, patent, finance, or news integration.
- Company alias database.
- Corporate-family mapping.
- Product ownership inference.
- Clinical success scoring.
- Approval probability scoring.
- Commercial strength scoring.
- CMC weekly management report template.

---

## 9. Recommended Follow-Up

Recommended next docs/spec-only step after this design is validated:

```text
Define mock dashboard record examples and static artifact acceptance tests.
```

That follow-up should still avoid runtime dashboard rendering, GitHub Actions, scheduler, alerts, persistence, source expansion, and new MCP tools unless explicitly approved.
