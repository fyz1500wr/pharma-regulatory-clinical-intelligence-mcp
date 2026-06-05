# Regulatory-Clinical Digest Memo Validation Exercise

## Purpose

This exercise validates whether a regulatory-clinical digest memo generated from MVP v1 MCP outputs is readable, source-aware, and safe for PM/RA review.

It should be completed before designing any runtime report generator, template renderer, or MCP-side report formatting helper.

This is a documentation and review exercise only. It does not add new data sources, MCP tools, scheduler, alerting, dashboard, persistence, or external integrations.

## When To Use This Exercise

Use this exercise after collecting MVP v1 tool outputs and before sharing a generated memo with PM, RA, management, or cross-functional stakeholders.

Use it especially when:

- any requested source is unavailable
- source health reports warnings
- `generate_regulatory_digest` returns zero regulatory updates
- `compare_companies_by_indication` is used
- ClinicalTrials.gov returned records may be mistaken for confirmed sponsor activity

## Required Inputs

Collect the following artifacts before the exercise:

| Artifact | Required? | Purpose |
|---|---:|---|
| User query scope | Yes | Defines indication, companies, sources, date range, and filters. |
| `check_source_health` output | Yes | Confirms requested-source and global source-health status. |
| `generate_regulatory_digest` output | Yes | Provides digest summary, findings, source errors, and limitations. |
| `compare_companies_by_indication` output | If company context is used | Supports company/sponsor association review. |
| `list_source_failures` output | If source-health warnings need explanation | Supports source-failure interpretation. |
| Draft memo | Yes | The memo to validate. |

## Exercise Scope

The exercise must stay within MVP v1 approved sources:

```text
FDA
TFDA
ClinicalTrials.gov
```

Do not add EMA, PMDA, NMPA, CTIS, WHO ICTRP, literature, patent, finance, news, or company-alias sources unless separately approved in a later scope decision.

## Step 1 — Confirm Query Scope

Record the run scope before reviewing the memo.

```text
Indication:
Companies:
Regulatory sources requested:
Clinical registry requested:
Date range:
Topic filters:
Product modality filters:
Tool run date:
Reviewer:
```

Validation questions:

- Are requested sources listed explicitly?
- Are companies listed exactly as queried?
- Is the date range visible?
- Are topic and modality filters preserved?

Fail the memo if the scope is missing or ambiguous.

## Step 2 — Confirm Source Coverage Interpretation

Review source status before reviewing findings.

| Check | Pass condition | Fail condition |
|---|---|---|
| Requested-source query errors | All requested-source errors are listed. | Source errors are hidden or summarized away. |
| Unavailable source interpretation | Unavailable source is described as partial coverage. | Unavailable source is described as no updates or no activity. |
| Global source-health warning | Global warnings are separated from requested-source query errors. | Global warnings are mixed into requested-source findings. |
| Source health pass | Source health pass is not treated as complete recall. | Memo says or implies complete data coverage. |

Required wording for unavailable requested sources:

```text
Coverage is partial for requested source(s): [source]. Zero returned updates must not be interpreted as no updates for unavailable sources.
```

## Step 3 — Validate Regulatory Findings

For each regulatory source, confirm whether the memo distinguishes:

- available source with returned records
- available source with zero returned records
- unavailable source with zero returned records
- narrow-filter zero result

FDA example failure:

```text
No FDA updates were found.
```

This fails if FDA was unavailable.

Safer replacement:

```text
FDA was unavailable in this run. FDA regulatory update status requires manual verification.
```

Validation questions:

- Does each regulatory finding include agency, title, date metadata, and URL when available?
- Does the memo avoid treating unavailable-source zero counts as no updates?
- Are decision-critical findings flagged for manual official-source verification?

## Step 4 — Validate Clinical Trial Findings

Clinical trial records should be described as ClinicalTrials.gov query results unless sponsor identity and product association have been reviewed.

Required checks:

- NCT ID or trial identifier is preserved when available.
- Trial title is preserved when available.
- Phase and recruitment status are not over-interpreted.
- Results availability is reported only when present in the tool output.
- Sponsor/collaborator fields are reviewed before company activity language is used.

Fail the memo if it turns returned records into confirmed company pipeline activity without sponsor review.

## Step 5 — Validate Company / Sponsor Association Section

When company comparison output is used, the memo must separate:

| Field | Required interpretation |
|---|---|
| Requested company | The user-entered company name. |
| Returned records | Records returned by the query, not automatically confirmed activity. |
| Sponsor-name matches | Records where sponsor name matches the requested company. |
| Non-sponsor returned records | Records requiring manual review. |
| Activity evaluable | Whether the row can support limited activity interpretation. |

Overstatement examples that fail:

```text
Company A is ahead of Company B.
Company A has stronger clinical activity.
Company B has no activity.
The returned trial proves sponsor ownership.
```

Safer replacements:

```text
The query returned more records for Company A under the current search parameters.
Sponsor-name matches and product association require manual review before interpreting relative activity.
```

## Step 6 — Validate Key Risks and Caveats

The memo must include caveats relevant to the run.

Minimum caveats:

- source unavailable is not zero activity
- source health pass does not prove complete recall
- ClinicalTrials.gov returned records may include non-sponsor records
- sponsor-name matching does not infer ownership or corporate family relationships
- official URLs require manual verification for decision-critical findings
- output is working intelligence only

Fail the memo if caveats are absent from the executive summary when they materially affect interpretation.

## Step 7 — Validate PM/RA Follow-up Actions

Recommended actions should be specific and evidence-linked.

Acceptable examples:

- Manually verify FDA because FDA was unavailable.
- Review ClinicalTrials.gov sponsor and collaborator fields for returned company-associated records.
- Preserve source limitations in management-facing summaries.
- Escalate source-health limitation when it affects a decision deadline.

Fail examples:

- Recommend a regulatory strategy based only on unavailable-source or query-result output.
- Recommend a competitive conclusion without sponsor/product association review.
- Recommend management action without preserving source limitations.

## Step 8 — Red Flag Sentence Review

Search the draft memo for sentences that contain or imply:

| Red flag | Why it fails |
|---|---|
| “No FDA updates” when FDA unavailable | Treats unavailable source as zero result. |
| “No company activity” | May overstate sponsor association limits. |
| “Company A is ahead” | Infers competitive strength. |
| “Confirmed sponsor activity” without sponsor review | Overstates ClinicalTrials.gov query output. |
| “Complete coverage” | Overstates source-health or search recall. |
| “Final recommendation” | Turns working intelligence into decision advice. |

For each red flag, write a safer replacement before approving the memo.

## Step 9 — Pass / Fail Decision

Use this decision table.

| Result | Criteria | Next action |
|---|---|---|
| Pass | Scope, source coverage, findings, caveats, and follow-up actions are clear and source-aware. | Memo can proceed to human PM/RA review. |
| Pass with limitations | Memo is usable but a source is unavailable or company association requires manual review. | Preserve limitations and assign follow-up actions. |
| Fail | Memo hides source limitations, overstates query results, or omits key caveats. | Revise memo before use. |

## Validation Checklist

- [ ] Scope is explicit.
- [ ] Requested sources are listed.
- [ ] Source errors are visible.
- [ ] Unavailable sources are not interpreted as zero updates.
- [ ] Regulatory findings distinguish available zero records from unavailable-source zero records.
- [ ] ClinicalTrials.gov returned records are identified as query results.
- [ ] Sponsor-name matches are separated from non-sponsor returned records.
- [ ] Company superiority, ownership, approval probability, and commercial strength are not inferred.
- [ ] Official URLs are flagged for manual review when decision-critical.
- [ ] PM/RA follow-up actions are specific and evidence-linked.
- [ ] Memo is labeled working intelligence only.

## Recommended Exercise Record

When completing the exercise, record:

```text
Exercise date:
Reviewer:
Memo title:
Tool outputs reviewed:
Source coverage decision:
Company association decision:
Red flag sentences found:
Revisions required:
Final validation result: Pass / Pass with limitations / Fail
```

## Exit Criteria Before Runtime Generator Design

Do not proceed to runtime report generator design until at least one dry-run memo:

1. preserves source limitation language correctly
2. separates requested-source errors from global source-health warnings
3. avoids over-interpreting ClinicalTrials.gov query results
4. produces actionable PM/RA follow-up steps
5. passes this validation checklist

If these criteria are not met, revise the prompt pack and example memo before considering runtime work.
