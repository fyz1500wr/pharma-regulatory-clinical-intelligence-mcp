# Live Source Behavior Notes

## Purpose

This document explains practical behavior that may appear when MVP v1 tools query live or external public sources.

It is intended to help users, Claude Project, Codex, MCP clients, and future maintainers interpret live-source outputs conservatively.

Use this document when a tool output contains:

- empty results
- missing fields
- inconsistent dates
- source health warnings
- sponsor-name matching limitations
- metadata-backed regulatory details
- ClinicalTrials.gov-only trial activity

This document does not define new tools, new sources, persistence, scheduler behavior, alerting, or source expansion.

---

## MVP v1 Active Sources

MVP v1 active sources are intentionally limited to:

- FDA
- TFDA
- ClinicalTrials.gov

Do not assume MVP v1 includes:

- EMA
- NMPA / CDE
- PMDA
- WHO ICTRP
- EU CTIS
- literature
- patents
- finance data
- commercial intelligence
- internal company records
- full global clinical trial coverage
- full-text regulatory document review

If a user needs those sources, treat that as a separate post-MVP source expansion decision.

---

## General Live Source Behavior

Live-source outputs can vary between runs because external sources may change, throttle, fail, or expose incomplete metadata.

Common behavior includes:

- no matching records for a query
- records with missing dates
- records with incomplete document status
- records with limited summaries
- official URLs that require manual review
- search results affected by keyword wording
- temporary API or website instability
- source health pass without complete data coverage
- source degradation that affects only part of the output

General interpretation rule:

```text
A live-source result should be treated as source-grounded working intelligence, not as a final regulatory, clinical, legal, medical, commercial, or CMC conclusion.
```

---

## FDA Behavior Notes

FDA-related outputs in MVP v1 should be interpreted as FDA source-backed metadata or search results within the implemented connector scope.

Practical notes:

- Search terms can strongly affect returned records.
- A narrow query may return no records even when FDA has related materials under different wording.
- A broad query may return records that require manual filtering.
- Document type and document status are metadata fields and should not be treated as final applicability decisions.
- Product modality tags, when present, should be treated as classification aids, not final regulatory classification.
- `get_regulatory_document_detail` is metadata-backed in MVP v1 and does not replace full document review.
- Official FDA URLs should be manually reviewed before using a record in a regulatory conclusion.

Do not conclude:

```text
No FDA result was returned, therefore no FDA requirement exists.
```

Safer wording:

```text
MVP v1 did not return matching FDA records for this query. This should not be interpreted as evidence that no FDA requirement exists. Manual verification through FDA official sources is required.
```

---

## TFDA Behavior Notes

TFDA-related outputs in MVP v1 should be interpreted as TFDA source-backed metadata or search results within the implemented connector scope.

Practical notes:

- Chinese and English search terms may produce different results.
- Traditional Chinese regulatory wording may differ from the user's English topic wording.
- A missing TFDA result does not prove absence of Taiwan requirements.
- Announcement category does not automatically establish product-specific applicability.
- Publication date, document status, and topic fields may require manual confirmation from the official announcement.
- Official TFDA URLs and original公告內容 should be reviewed manually before using the result as a Taiwan regulatory conclusion.

Do not conclude:

```text
No TFDA result was returned, therefore Taiwan has no relevant requirement.
```

Safer wording:

```text
MVP v1 did not return matching TFDA records for this query. This should not be interpreted as evidence that no Taiwan requirement exists. Manual verification through TFDA official sources is required.
```

---

## ClinicalTrials.gov Behavior Notes

ClinicalTrials.gov-related outputs in MVP v1 should be interpreted as registered trial activity from ClinicalTrials.gov only.

Practical notes:

- ClinicalTrials.gov is not complete global clinical trial coverage.
- Indication wording can strongly affect returned trials.
- Sponsor names may appear in different forms across records.
- Sponsor-name matching is not corporate family mapping.
- Intervention names are registry fields and may not fully validate product identity.
- Trial phase does not indicate approval probability.
- Trial status does not establish clinical success or failure.
- Recruiting or active status does not prove development strength.
- Completed status does not prove positive results.
- Results availability does not replace clinical evidence review.

Do not conclude:

```text
This company is stronger because it has more returned ClinicalTrials.gov trials.
```

Safer wording:

```text
This company has more returned ClinicalTrials.gov trial activity in this query result. This does not establish clinical superiority, approval probability, commercial strength, or company superiority.
```

---

## Sponsor Name Matching Behavior

MVP v1 company comparison is sponsor-name-based.

This means:

- It compares returned trial records using the sponsor names supplied in the query.
- It may miss subsidiaries, affiliates, acquired companies, or alternate sponsor spellings.
- It may include records where the sponsor name matches text but requires manual identity confirmation.
- It should not infer corporate family relationships unless the source record explicitly supports them.

Required caveat for company comparisons:

```text
Company comparison is based on sponsor-name matching in ClinicalTrials.gov MVP v1 outputs. It is not a corporate family mapping or company superiority assessment.
```

---

## Date Range Behavior

Some MVP v1 outputs may record a requested `date_range` in `query_metadata`.

Important limitation:

```text
For `compare_companies_by_indication`, `date_range` is recorded in query metadata only. Date-based trial filtering is not applied in MVP v1.
```

Do not say:

```text
The company comparison covers only trials within the requested date range.
```

Safer wording:

```text
The requested date range was recorded in query metadata, but MVP v1 does not apply date-based trial filtering for this company comparison output.
```

---

## Source Health Behavior

`check_source_health` checks current source or connector behavior.

A source health pass means:

- the current health check passed
- the source or connector appeared reachable under the check performed

A source health pass does not mean:

- all data from the source was retrieved
- the source database is complete
- the query result is exhaustive
- every downstream output is fully reliable

A degraded or failed source means:

- confidence in dependent outputs should be lowered
- affected findings should be caveated
- source-specific failures should be reviewed
- manual official-source verification becomes more important

Safe source health wording:

```text
Source health passed for the checked source, but this does not prove complete data coverage. Important findings still require manual verification through official source records.
```

---

## Source Failure Behavior

`list_source_failures` converts current source health information into structured failure records.

In MVP v1, source failure records are:

- current snapshots
- operational review aids
- useful for caveating downstream outputs

They are not:

- a historical uptime database
- a persistent failure event store
- evidence of long-term source reliability trends

Safe source failure wording:

```text
The source failure output reflects current source health status only. It should not be interpreted as a historical failure trend.
```

---

## Empty Result Handling

Empty results should be handled conservatively.

Possible causes include:

- query wording too narrow
- source metadata not using the expected term
- language mismatch
- source connector limitation
- temporary source behavior
- true absence of matching records within MVP v1 scope

Do not treat an empty result as proof of absence.

Recommended empty-result wording:

```text
MVP v1 did not return matching records for this query. This means no matching records were found within the current MVP v1 source/query scope. It should not be interpreted as proof that no relevant requirement, document, or trial activity exists.
```

Recommended follow-up:

- try alternate keywords
- try local-language terms where relevant
- review official source search pages manually
- check source health
- include an explicit caveat in the final summary

---

## Metadata and Field Gaps

Live-source outputs may contain missing or incomplete fields.

Common gaps include:

- missing publication date
- missing document status
- missing product modality
- missing trial phase
- missing intervention details
- missing results availability
- limited summary text

Interpretation rule:

```text
Missing metadata should be reported as missing or unavailable. It should not be filled in by assumption.
```

Safer field-gap wording:

```text
The returned record does not include [FIELD] in the MVP v1 output. Manual review of the official record is needed before using this field in analysis.
```

---

## Recommended User-Facing Caveats

Use these caveats in reports, summaries, or Claude responses when appropriate.

### General caveat

```text
This summary is based on MVP v1 source-grounded outputs and requires manual verification through official source records before decision-making.
```

### Regulatory caveat

```text
Regulatory findings are based on returned FDA and/or TFDA records within MVP v1 scope. They should not be treated as final regulatory interpretation or complete agency requirement mapping.
```

### TFDA empty-result caveat

```text
No matching TFDA record was returned by MVP v1 for this query. This does not establish that no Taiwan requirement exists.
```

### Clinical trial caveat

```text
Clinical trial findings are based on ClinicalTrials.gov MVP v1 outputs only. They do not establish clinical success, approval probability, commercial strength, or complete global clinical activity.
```

### Company comparison caveat

```text
Company comparison is sponsor-name-based ClinicalTrials.gov activity only. It should not be interpreted as a company superiority, clinical success, approval probability, or commercial strength assessment.
```

### Source health caveat

```text
Source health status reflects the current check only. A pass does not prove complete data coverage, and a failure should lower confidence in affected downstream outputs.
```

---

## Do Not Conclude

Do not use MVP v1 live-source outputs to conclude:

- no FDA requirement exists
- no TFDA requirement exists
- FDA and TFDA are finally aligned
- FDA and TFDA are finally divergent
- a final regulatory requirement has been established
- a product is likely to be approved
- a trial phase proves approval probability
- a trial status proves success or failure
- a company is superior
- a company has stronger commercial potential
- returned trial activity is complete global clinical activity
- source health pass proves complete data coverage
- source failure output proves historical reliability trends

---

## Practical Review Workflow

Recommended workflow for important outputs:

1. Run `check_source_health` for relevant sources.
2. Run the relevant search, comparison, or digest tool.
3. Inspect `query_metadata`.
4. Inspect `known_limitations`.
5. Preserve `official_url` for important records.
6. Check for empty results or missing fields.
7. Add caveats for source scope, field gaps, and source health issues.
8. Manually verify key records through official source URLs.
9. Use tool output as a working intelligence draft, not a final decision.

---

## Relationship to Tool Output Review Checklist

Use this document together with `docs/tool_output_review_checklist.md`.

Recommended division of use:

| Document | Main use |
|---|---|
| `docs/live_source_behavior_notes.md` | Explains why live-source outputs may vary, be incomplete, or require caveats. |
| `docs/tool_output_review_checklist.md` | Provides practical checklist items for reviewing outputs before use. |

Together, these documents help keep MVP v1 outputs practical, source-grounded, and conservative.
