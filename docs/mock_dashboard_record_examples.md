# Mock Dashboard Record Examples and Static Artifact Acceptance Criteria

Last updated: 2026-06-11

Status: docs/spec-only. This document defines mock dashboard record examples and static artifact acceptance criteria for validating the dashboard design without implementing a dashboard renderer, artifact generator, GitHub Actions workflow, scheduler, alerts, persistence, runtime connector, new MCP tool, `.mcp.json`, source expansion, or external integration.

---

## 1. Purpose

This document gives controlled mock records that can be used to reason about the static dashboard dry-run design in `docs/static_dashboard_dry_run_design.md` and the canonical dashboard schema contract in `docs/dashboard_data_schema_contract.md`.

The examples are fictional and non-confidential. They are not evidence of real regulatory status, clinical status, product ownership, company hierarchy, commercial value, or approval probability.

---

## 2. Mock Record Set

The minimum mock set should contain one or more examples for each canonical dashboard schema family:

```text
RegulatoryGuidanceUpdate
ClinicalTrialUpdate
SourceHealthEvent
DashboardDigestSummary
```

The mock set should exercise both normal and limitation cases:

```text
source pass
source unavailable
complete metadata
partial metadata
human review required
registry-reported sponsor only
global harmonisation guidance distinct from regulatory agency records
```

---

## 3. RegulatoryGuidanceUpdate Examples

### Example RGU-001 — Regulatory agency update

```yaml
record_id: RGU-001
schema_name: RegulatoryGuidanceUpdate
schema_version: 1
source_name: TFDA
source_category: regulatory_agency
source_url: https://example.invalid/tfda/mock-guidance
retrieved_at: 2026-06-11T00:00:00Z
record_date: 2026-05-20
date_window_bucket: 1_month
region: Taiwan
title: Mock TFDA quality guidance update for biologic products
document_type: guidance_update
topic_tags:
  - quality
  - CMC
modality_tags:
  - recombinant_protein
guideline_family: mock_quality_guidance
guideline_code: MOCK-TFDA-Q-001
guideline_stage_or_status: final
official_url: https://example.invalid/tfda/mock-guidance
attachment_urls: []
source_health_status: pass
human_review_required: true
limitations:
  - Mock record only; not an official TFDA record.
```

Expected dashboard behavior:

- Show as a regulatory agency update.
- Show topic and modality tags as classification aids only.
- Show empty `attachment_urls` as missing or absent mock metadata, not as regulatory evidence.
- Preserve human review flag.

### Example RGU-002 — Global harmonisation guidance

```yaml
record_id: RGU-002
schema_name: RegulatoryGuidanceUpdate
schema_version: 1
source_name: ICH
source_category: global_harmonisation_guidance
source_url: https://example.invalid/ich/mock-guideline
retrieved_at: 2026-06-11T00:00:00Z
record_date: 2026-04-15
date_window_bucket: 3_months
region: global
title: Mock ICH guideline revision concept note
document_type: harmonised_guidance
topic_tags:
  - quality
modality_tags:
  - unknown
guideline_family: mock_ich_quality
guideline_code: MOCK-ICH-QX
guideline_stage_or_status: concept
source_health_status: pass
human_review_required: true
limitations:
  - Mock record only; ICH is not a drug-review agency and not a clinical trial registry.
```

Expected dashboard behavior:

- Show as global harmonisation guidance.
- Do not display as FDA, TFDA, EMA, NMPA/CDE, or PMDA review activity.
- Do not display as clinical trial activity.

---

## 4. ClinicalTrialUpdate Examples

### Example CTU-001 — Complete registry metadata

```yaml
record_id: CTU-001
schema_name: ClinicalTrialUpdate
schema_version: 1
source_name: ClinicalTrials.gov
source_category: clinical_trial_registry
registry_name: ClinicalTrials.gov
registry_id: NCT00000001
registry_url: https://clinicaltrials.gov/study/NCT00000001
retrieved_at: 2026-06-11T00:00:00Z
record_date: 2026-05-01
date_window_bucket: 3_months
trial_title: Mock phase 2 biologic study in condition A
indication_terms:
  - condition A
sponsor_name: Mock Sponsor A
collaborator_names:
  - Mock Collaborator B
intervention_names:
  - Mock recombinant protein product
phase: Phase 2
recruitment_status: Recruiting
study_start_date: 2026-01-15
primary_completion_date: 2027-08-31
results_first_posted_date: null
source_health_status: pass
human_review_required: true
limitations:
  - Mock record only; sponsor name is registry-reported metadata only.
```

Expected dashboard behavior:

- Show as clinical trial registry activity.
- Allow grouping by indication, sponsor, phase, and recruitment status.
- Do not infer clinical success, approval probability, company superiority, commercial strength, product ownership, or corporate family.

### Example CTU-002 — Partial metadata

```yaml
record_id: CTU-002
schema_name: ClinicalTrialUpdate
schema_version: 1
source_name: ClinicalTrials.gov
source_category: clinical_trial_registry
registry_name: ClinicalTrials.gov
registry_id: NCT00000002
registry_url: https://clinicaltrials.gov/study/NCT00000002
retrieved_at: 2026-06-11T00:00:00Z
record_date: 2026-03-10
date_window_bucket: 6_months
trial_title: Mock early-stage trial with partial dates
indication_terms:
  - condition B
sponsor_name: Mock Sponsor C
collaborator_names: []
intervention_names:
  - Mock modality not specified
phase: Not Applicable
recruitment_status: Active, not recruiting
study_start_date: null
primary_completion_date: null
results_first_posted_date: null
source_health_status: pass
human_review_required: true
limitations:
  - Partial date metadata in mock record.
  - Missing dates are not negative evidence.
```

Expected dashboard behavior:

- Display with limitation flag.
- Do not suppress solely because dates are partial.
- Do not interpret missing results date as failed or negative outcome.

---

## 5. SourceHealthEvent Examples

### Example SHE-001 — Source check pass

```yaml
record_id: SHE-001
schema_name: SourceHealthEvent
schema_version: 1
source_name: ClinicalTrials.gov
source_category: clinical_trial_registry
source_check_status: pass
failure_type: null
http_status: 200
parser_error_code: null
schema_or_selector_change_detected: false
record_count_returned: 2
expected_minimum_record_count: 1
blocks_dashboard_use: false
recommended_action: Continue normal review with human verification.
retrieved_at: 2026-06-11T00:00:00Z
limitations:
  - Source health pass does not prove complete coverage.
```

Expected dashboard behavior:

- Show source as available for the mock run.
- Preserve caveat that pass does not prove complete coverage.

### Example SHE-002 — Source unavailable

```yaml
record_id: SHE-002
schema_name: SourceHealthEvent
schema_version: 1
source_name: FDA
source_category: regulatory_agency
source_check_status: source_unavailable
failure_type: access_limitation
http_status: 403
parser_error_code: FDA_ACCESS_LIMITATION
schema_or_selector_change_detected: unknown
record_count_returned: null
expected_minimum_record_count: 1
blocks_dashboard_use: true
recommended_action: Treat FDA results as incomplete; do not interpret as zero FDA updates.
retrieved_at: 2026-06-11T00:00:00Z
limitations:
  - Source unavailable is not no result.
  - Access limitation is not evidence of zero matching records.
```

Expected dashboard behavior:

- Display a source-health warning before FDA content interpretation.
- Block or qualify FDA dashboard use.
- Do not show `0 FDA updates` as a conclusion.

---

## 6. DashboardDigestSummary Example

### Example DDS-001 — Source-aware dashboard summary

```yaml
record_id: DDS-001
schema_name: DashboardDigestSummary
schema_version: 1
source_name: static_mock_run
source_category: dashboard_digest_summary
retrieved_at: 2026-06-11T00:00:00Z
record_date: 2026-06-11
date_window_bucket: 6_months
summary_title: Mock dashboard dry-run summary
covered_sources:
  - TFDA
  - ICH
  - ClinicalTrials.gov
  - FDA
source_health_summary:
  - ClinicalTrials.gov source check passed in mock run.
  - FDA source unavailable in mock run; FDA content cannot be interpreted as complete.
key_findings:
  - Mock TFDA and ICH records demonstrate regulatory/guidance tab behavior.
  - Mock ClinicalTrials.gov records demonstrate complete and partial metadata behavior.
human_review_required: true
limitations:
  - Mock summary only.
  - Not a regulatory, clinical, legal, medical, commercial, or management decision.
```

Expected dashboard behavior:

- Show source-health caveats near the top of the summary.
- Require human review.
- Avoid final recommendations or decision language.

---

## 7. Static Artifact Acceptance Criteria

A future static artifact dry-run remains docs/spec-only unless separately approved. If static artifact examples are later approved, they should meet these criteria:

1. Every mock record must include `record_id`, `schema_name`, `schema_version`, `source_name`, `source_category`, `retrieved_at`, `record_date`, `source_health_status` or equivalent source-health context, `human_review_required`, and `limitations`.
2. Every dashboard tab must preserve source limitation language.
3. Source unavailable must never be rendered as no matching records.
4. Missing metadata must never be rendered as negative evidence.
5. Clinical trial sponsor fields must remain registry-reported metadata only.
6. ICH mock records must remain global harmonisation guidance records.
7. Artifact summaries must clearly state that they are working intelligence drafts requiring human review.
8. No artifact may imply clinical success, approval probability, product ownership, commercial strength, company superiority, regulatory acceptance, or management decision.

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

After validation, pause for direction calibration before adding more dashboard documents.

Possible next directions:

```text
1. Continue docs/spec-only dashboard artifact planning.
2. Return to MVP runtime hardening.
3. Revisit source/guidance expansion sequencing without implementing connectors.
4. Stop new PRs until an explicit direction is selected.
```
