# Regulatory-Clinical Digest Example Memo

## Purpose

This example shows how a PM/RA-facing regulatory-clinical intelligence memo should look after applying `docs/regulatory_clinical_digest_report_workflow.md`.

The memo is intentionally written as a controlled example, not as a live current-state assessment.

It demonstrates how to preserve source limitations, query-result caveats, and human-review requirements when summarizing MVP v1 MCP output.

## Example Scenario

| Field | Example value |
|---|---|
| Indication | Gastric cancer |
| Companies | AstraZeneca, Merck |
| Regulatory sources requested | FDA, TFDA |
| Clinical registry requested | ClinicalTrials.gov |
| Known source condition | FDA source unavailable or blocked in runtime |
| Clinical trial caveat | ClinicalTrials.gov query results require sponsor association review |

## Example Memo

# Regulatory-Clinical Intelligence Memo

## 1. Executive Summary

This memo summarizes a controlled MVP v1 intelligence run for gastric cancer, with company context for AstraZeneca and Merck.

Requested sources were FDA, TFDA, and ClinicalTrials.gov. FDA coverage is partial because the FDA source was unavailable in the runtime. Zero returned FDA regulatory updates must not be interpreted as no FDA updates.

The run returned clinical trial records from ClinicalTrials.gov. Returned clinical trial records are query results and must not be interpreted as confirmed sponsor-level activity until sponsor names and product association are reviewed.

This memo is working intelligence for PM/RA review. It is not a final regulatory, clinical, legal, medical, commercial, or management decision.

## 2. Source Coverage Status

| Source | Requested | Status | Interpretation |
|---|---:|---|---|
| FDA | Yes | Source unavailable | Partial requested-source coverage. FDA zero-count output is not a no-update finding. |
| TFDA | Yes | Query completed | Available MVP source output. Zero returned records may reflect filters and available source data. |
| ClinicalTrials.gov | Yes | Query completed | Returned records require sponsor/product association review. |

Coverage status:

```text
PARTIAL_REQUESTED_SOURCE_COVERAGE
```

Required interpretation:

```text
Coverage is partial for requested source(s): FDA. Zero returned updates must not be interpreted as no updates for unavailable sources.
```

## 3. Regulatory Update Findings

### FDA

No FDA regulatory update findings should be concluded from this run because FDA was unavailable.

Do not write:

```text
No FDA updates were found.
```

Use instead:

```text
FDA coverage was unavailable in this run; FDA regulatory update status requires manual verification.
```

### TFDA

TFDA returned zero regulatory updates in this example scenario.

Interpretation:

- TFDA query completed.
- Zero returned TFDA updates may be reported as zero returned records for the query scope.
- This is not evidence of complete TFDA absence unless the search strategy and official source coverage are manually reviewed.

## 4. Clinical Trial Findings

ClinicalTrials.gov returned trial records for the indication query.

The memo should summarize trial records as registry query results, not as confirmed company pipeline ownership.

Minimum fields to review:

| Field | Review expectation |
|---|---|
| NCT ID | Record-level traceability. |
| Trial title | Confirm indication relevance. |
| Phase | Support high-level development-stage review. |
| Recruitment status | Support activity review. |
| Sponsor/collaborator | Required for company association review. |
| Results availability | Flag whether results are posted. |
| URL | Required for manual verification. |

## 5. Company / Sponsor Association Review

Returned records are MVP query results. They are not confirmed sponsor-level company activity unless sponsor identity is reviewed.

| Company | Returned records | Sponsor-name matches | Non-sponsor records requiring manual review | Activity evaluable |
|---|---:|---:|---:|---|
| AstraZeneca | Example count from tool output | Example count from tool output | Example count from tool output | Yes, if source query succeeded and sponsor fields are reviewable |
| Merck | Example count from tool output | Example count from tool output | Example count from tool output | Yes, if source query succeeded and sponsor fields are reviewable |

Do not write:

```text
AstraZeneca has more activity than Merck.
```

Use instead:

```text
The query returned more records for AstraZeneca than Merck under the current search parameters. Sponsor-name matches and product association require manual review before interpreting relative activity.
```

## 6. Key Risks and Caveats

- FDA was unavailable in the example run; FDA zero returned updates must not be interpreted as no FDA updates.
- Source health status does not prove complete data recall.
- ClinicalTrials.gov query results may include records that are not sponsor-name matches for the requested company.
- Company comparison output does not infer corporate family relationships, product ownership, clinical success, approval probability, commercial strength, or company superiority.
- Official URLs and decision-critical findings require manual verification.
- This memo is not a final regulatory, clinical, legal, medical, commercial, or management decision.

## 7. PM/RA Recommended Follow-up Actions

1. Manually verify FDA for the indication and companies because FDA was unavailable in this run.
2. Review TFDA source URLs if any returned TFDA records are decision-critical.
3. Review ClinicalTrials.gov sponsor and collaborator fields for all company-associated records.
4. Separate sponsor-name matches from non-sponsor query returns before management reporting.
5. Preserve the source limitation statement in any downstream PM, RA, or management-facing summary.

## 8. Human Review Checklist

- [ ] Requested sources are listed.
- [ ] FDA unavailable status is visible.
- [ ] Zero FDA returned updates are not described as no FDA updates.
- [ ] ClinicalTrials.gov returned records are labeled as query results.
- [ ] Sponsor-name matches are separated from non-sponsor returned records.
- [ ] Official source URLs are reviewed for decision-critical findings.
- [ ] Caveats are preserved in any downstream summary.

## 9. Raw MCP Tool Traceability

| Tool | Output section to preserve |
|---|---|
| `check_source_health` | Source coverage status and source-health caveats. |
| `generate_regulatory_digest` | Executive summary, source errors, regulatory findings, clinical findings, known limitations. |
| `compare_companies_by_indication` | Returned records, sponsor-name match counts, non-sponsor records, evaluability status. |
| `list_source_failures` | Open source failures when requested-source or global source-health warnings need explanation. |

## Example Acceptance Review

This memo is acceptable only if a reviewer can answer:

1. Which sources were requested?
2. Which requested source was unavailable?
3. Whether zero FDA updates means no updates or unavailable source?
4. Which company/trial records are sponsor-name matches?
5. Which records require manual sponsor/product association review?
6. What PM/RA follow-up actions are required?

If any answer is unclear, the memo should not be used for management-facing communication.
