# MVP Live Acceptance Validation Results Template

Use this template to record the first controlled live acceptance validation of the MVP.

This template should be copied into a dated validation record when the validation is executed.

Example copy path:

```text
docs/validation_records/mvp_live_acceptance_validation_YYYY-MM-DD.md
```

Do not treat this template itself as an executed validation record.

## Validation metadata

| Field | Value |
|---|---|
| Validation date | TBD |
| Repository commit | TBD |
| Release/tag under validation | TBD |
| Validator | TBD |
| Environment | Codespaces / local / other |
| Python version | TBD |
| Network / egress notes | TBD |

## Pre-validation checks

| Check | Status | Evidence / notes |
|---|---|---|
| Clean `main` checkout | NOT_RUN |  |
| `git pull --ff-only origin main` completed | NOT_RUN |  |
| `git status --short` clean before validation | NOT_RUN |  |
| Full regression suite passed before live validation | NOT_RUN |  |

## Source health summary

| Source | Status | Evidence / notes |
|---|---|---|
| FDA | NOT_RUN |  |
| TFDA | NOT_RUN |  |
| ClinicalTrials.gov | NOT_RUN |  |

Allowed status values:

- PASS
- PARTIAL
- BLOCKED_SOURCE
- FAIL_CODE
- NOT_RUN

## Tool-level validation results

| Tool / check | Status | Evidence / notes | Follow-up needed? |
|---|---|---|---|
| Tool registry load | NOT_RUN |  |  |
| `check_source_health` | NOT_RUN |  |  |
| `list_source_failures` | NOT_RUN |  |  |
| FDA `search_regulatory_updates` | NOT_RUN |  |  |
| TFDA `search_regulatory_updates` | NOT_RUN |  |  |
| `compare_regulatory_updates` | NOT_RUN |  |  |
| `search_clinical_trials_by_indication` | NOT_RUN |  |  |
| `compare_companies_by_indication` | NOT_RUN |  |  |
| `generate_regulatory_digest` | NOT_RUN |  |  |

## Key evidence snippets

Paste short evidence snippets below. Avoid pasting excessively long raw outputs.

### Tool registry evidence

```text
TBD
```

### Source health evidence

```text
TBD
```

### FDA regulatory search evidence

```text
TBD
```

### TFDA regulatory search evidence

```text
TBD
```

### Regulatory comparison evidence

```text
TBD
```

### ClinicalTrials.gov indication search evidence

```text
TBD
```

### Company-by-indication comparison evidence

```text
TBD
```

### Regulatory digest evidence

```text
TBD
```

## Blockers and defects

| Item | Classification | Description | Proposed follow-up |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

Suggested classifications:

- SOURCE_OR_EGRESS_BLOCKER
- LIVE_SOURCE_SCHEMA_CHANGE
- TOOL_PARAMETER_DEFECT
- NORMALIZATION_DEFECT
- OUTPUT_CONTRACT_DEFECT
- DOCUMENTATION_GAP
- NO_ACTION_NEEDED

## Final decision

Select one:

| Decision | Selected? | Rationale |
|---|---|---|
| ACCEPT_FOR_CONTROLLED_MVP_USE | No |  |
| ACCEPT_WITH_SOURCE_LIMITATIONS | No |  |
| DO_NOT_ACCEPT_YET | No |  |

## Required follow-up before broader use

- TBD

## Important interpretation

This validation record does not certify regulatory completeness, clinical completeness, legal compliance, medical correctness, CMC adequacy, or business decision readiness.

It only records whether the current MVP tools can be used as a controlled working-intelligence aid within the approved MVP source scope.
