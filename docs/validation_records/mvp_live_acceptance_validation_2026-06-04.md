# MVP Live Acceptance Validation Record — 2026-06-04

Status: ACCEPT_WITH_SOURCE_LIMITATIONS  
Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`  
Branch used for record: `docs/v0.2.16-mvp-live-acceptance-results`  
Validated from: GitHub Codespaces on `main`  
Validation date: 2026-06-04

This record documents the first controlled live acceptance validation evidence for the MVP v1 regulatory and clinical intelligence tools.

This record does not add new sources, MCP tools, scheduler, alerts, dashboard, persistence, HTTP/SSE transport, `.mcp.json`, GitHub automation, literature, patent, finance, or commercial intelligence integration.

---

## 1. Validation scope

The live validation remained limited to the approved MVP v1 source scope:

```text
FDA + TFDA + ClinicalTrials.gov
```

The validation followed the existing MVP live acceptance validation runbook and results-template intent.

---

## 2. Pre-validation checks

| Check | Status | Evidence |
|---|---|---|
| `git checkout main` | PASS | Already on `main` |
| `git pull --ff-only origin main` | PASS | Already up to date |
| Editable install | PASS | `python -m pip install -e ".[dev]"` completed successfully |
| Project-state release consistency test | PASS | `pytest tests/test_project_state_release_tag_consistency.py -q`: 5 passed |
| Full regression suite | PASS | `pytest -q`: 202 passed |

Interpretation: the repository baseline was stable before live-source validation.

---

## 3. Tool registry validation

| Check | Status | Evidence |
|---|---|---|
| Tool registry load | PASS | All 8 MVP tools loaded from `TOOL_REGISTRY` |

Confirmed tools:

```text
check_source_health
compare_companies_by_indication
compare_regulatory_updates
generate_regulatory_digest
get_regulatory_document_detail
list_source_failures
search_clinical_trials_by_indication
search_regulatory_updates
```

---

## 4. Source health summary

| Source | Status | Evidence / interpretation |
|---|---|---|
| FDA | BLOCKED_SOURCE | FDA requests were redirected to an FDA abuse-detection/apology path and surfaced as `SOURCE_UNAVAILABLE`. This must not be interpreted as `NO_MATCHING_RECORDS`. |
| TFDA | PASS | TFDA connector execution path returned available/pass. |
| ClinicalTrials.gov | PASS | ClinicalTrials.gov connector execution path returned available/pass. |

Overall source health status: `degraded`.

Source failure summary:

| Failure | Status | Severity | Interpretation |
|---|---|---|---|
| `FDA_openFDA-api_status-open` | open | high | FDA live source access was blocked by abuse-detection/apology path; rerun FDA validation in another approved runtime or manually verify FDA official sources before interpreting FDA coverage. |

---

## 5. Regulatory tool validation

### 5.1 FDA regulatory search

| Check | Status | Evidence / interpretation |
|---|---|---|
| FDA `search_regulatory_updates` | PASS for failure handling / BLOCKED_SOURCE for live source | Returned structured `SOURCE_UNAVAILABLE`; did not silently return zero records. |

Key interpretation:

```text
FDA source-access limitation remained visible and was not converted into NO_MATCHING_RECORDS.
```

### 5.2 TFDA regulatory search

| Check | Status | Evidence / interpretation |
|---|---|---|
| TFDA `search_regulatory_updates` | PASS / structured no-result | Returned `NO_MATCHING_RECORDS` with `query_metadata`, `date_range`, `date_from`, `date_to`, and `sources_searched`. |

Key interpretation:

```text
Because TFDA source health passed, a TFDA no-result response for the selected query and date range is structurally acceptable within the stated query scope.
```

### 5.3 FDA + TFDA comparison

| Check | Status | Evidence / interpretation |
|---|---|---|
| `compare_regulatory_updates` | PARTIAL / PASS for limitation visibility | FDA failure was preserved under `partial_lookup_failures`; TFDA completed with 0 matching updates. |

Key interpretation:

```text
The comparison did not treat blocked FDA access as zero FDA regulatory updates.
```

---

## 6. ClinicalTrials.gov tool validation

### 6.1 Indication search

| Check | Status | Evidence / interpretation |
|---|---|---|
| `search_clinical_trials_by_indication("gastric cancer")` | PASS | Returned 5 ClinicalTrials.gov trial records with trial ID, sponsor, phase, status, official URL, retrieved timestamp, indication, intervention, and product modality fields. |

### 6.2 Company-by-indication comparison

| Check | Status | Evidence / interpretation |
|---|---|---|
| `compare_companies_by_indication` for AstraZeneca vs Merck in gastric cancer | PASS / MVP-limited | Returned company comparison, trial counts, active/completed counts, phase/status distributions, key trials, landscape summary, and limitations. |

Important limitations remained visible:

- ClinicalTrials.gov only.
- `date_range` is recorded in query metadata only; date-based trial filtering is not applied in MVP v1.
- Company matching is sponsor-name based.
- Trial counts do not imply clinical success, approval probability, commercial strength, or company superiority.

---

## 7. Digest validation

### 7.1 Primary digest: FDA + TFDA + ClinicalTrials.gov

| Check | Status | Evidence / interpretation |
|---|---|---|
| `generate_regulatory_digest` with FDA + TFDA + ClinicalTrials.gov | PARTIAL / PASS for source limitation visibility | Digest generated successfully. It included 0 regulatory updates, 5 clinical trial updates, 1 source query error, and 1 open source failure. FDA `SOURCE_UNAVAILABLE` remained visible in `query_metadata.source_errors`. |

### 7.2 Fallback digest: TFDA + ClinicalTrials.gov

| Check | Status | Evidence / interpretation |
|---|---|---|
| `generate_regulatory_digest` with TFDA + ClinicalTrials.gov | PASS / source-limited | Digest generated successfully with 0 regulatory updates and 5 clinical trial updates. `source_errors` was empty for the requested source set. |

Important digest limitations remained visible:

- Digest content is not a final regulatory, clinical, legal, or medical assessment.
- Impact matrix is heuristic and requires manual review.
- MVP v1 digest is a rule-based aggregation over current MCP tool outputs.

---

## 8. Final acceptance decision

| Decision | Selected? | Rationale |
|---|---|---|
| ACCEPT_FOR_CONTROLLED_MVP_USE | No | FDA live source access was blocked in the validation environment. |
| ACCEPT_WITH_SOURCE_LIMITATIONS | Yes | TFDA and ClinicalTrials.gov live paths were usable, FDA source blocking was visible and structured, and digest/comparison outputs preserved limitations. |
| DO_NOT_ACCEPT_YET | No | No code-level failure, unstructured exception, hidden FDA failure, or unsafe clinical/company superiority inference was observed in this validation. |

Final decision:

```text
ACCEPT_WITH_SOURCE_LIMITATIONS
```

---

## 9. Required follow-up before broader use

1. Do not interpret FDA `SOURCE_UNAVAILABLE` as no FDA regulatory updates.
2. For FDA-dependent work, rerun FDA validation in another approved runtime or manually verify FDA official sources.
3. Keep executive or regulatory-facing digest language conservative.
4. Treat digest output as a working intelligence draft requiring human review.
5. Do not expand source scope or tooling based on this validation alone.

---

## 10. PR recommendation

A narrow evidence-recording PR is justified because live validation was completed and produced a clear acceptance decision.

Recommended PR title:

```text
Record v0.2.16 MVP live acceptance validation results
```

Recommended scope:

- Add this validation record only.
- Do not change runtime behavior.
- Do not add sources, tools, scheduler, alerts, dashboard, persistence, HTTP/SSE, `.mcp.json`, GitHub automation, literature, patent, or finance integration.

---

## 11. Important interpretation

This validation record does not certify regulatory completeness, clinical completeness, legal compliance, medical correctness, CMC adequacy, or business decision readiness.

It only records that the current MVP tools can be used as a controlled working-intelligence aid within the approved MVP source scope, with FDA source-access limitations visible and requiring manual verification or rerun in another approved runtime.
