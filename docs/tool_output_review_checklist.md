# Tool Output Review Checklist

## Purpose

This checklist helps reviewers inspect MVP v1 MCP tool outputs before using them in regulatory, clinical, PM, or management-facing summaries.

It is designed to prevent over-interpretation of source-grounded but limited outputs.

Use this checklist when reviewing outputs from:

- `search_regulatory_updates`
- `get_regulatory_document_detail`
- `compare_regulatory_updates`
- `search_clinical_trials_by_indication`
- `compare_companies_by_indication`
- `check_source_health`
- `list_source_failures`
- `generate_regulatory_digest`

This document is not a substitute for regulatory, clinical, legal, medical, QA, or CMC review.

---

## MVP v1 Scope Reminder

MVP v1 active sources are limited to:

- FDA
- TFDA
- ClinicalTrials.gov

Do not assume the output includes:

- EMA
- NMPA / CDE
- PMDA
- WHO ICTRP
- EU CTIS
- literature
- patents
- finance data
- commercial intelligence
- internal company data
- full regulatory document body review
- global clinical trial completeness

---

## General Output Review Checklist

Before using any tool output, confirm:

- [ ] The requested topic, indication, modality, agency, sponsor, or company name is clearly reflected in `query_metadata`.
- [ ] The output includes `official_url` where available.
- [ ] The output includes or preserves `known_limitations`.
- [ ] The output does not present missing results as proof of absence.
- [ ] The output does not claim final regulatory interpretation.
- [ ] The output does not infer clinical success, approval probability, company superiority, or commercial strength.
- [ ] The output clearly separates source-backed findings from suggested manual follow-up.
- [ ] Important records have been manually checked through the official URL before being used in decisions.

If any item above fails, treat the output as a draft only and add a visible caveat.

---

## Regulatory Output Checklist

Use this section for:

- `search_regulatory_updates`
- `get_regulatory_document_detail`
- `compare_regulatory_updates`
- regulatory sections of `generate_regulatory_digest`

Check:

- [ ] Agency is FDA, TFDA, or both.
- [ ] Each important record has an `official_url` where available.
- [ ] Publication date is shown or the absence of date is caveated.
- [ ] Document type and document status are not over-interpreted.
- [ ] Product modality and topic tags are treated as metadata, not final classification.
- [ ] `get_regulatory_document_detail` output is treated as metadata-backed only.
- [ ] `compare_regulatory_updates` output is treated as descriptive comparison only.
- [ ] FDA and TFDA differences are not described as final agency divergence.
- [ ] No TFDA result is not described as no Taiwan requirement.
- [ ] No FDA result is not described as no FDA requirement.

Safe regulatory interpretation pattern:

```text
The MVP v1 search returned records from [AGENCY] related to [TOPIC]. These records should be manually verified through the official URLs before being used as regulatory conclusions.
```

Avoid:

```text
This is the final FDA/TFDA requirement.
```

---

## Clinical Trial Output Checklist

Use this section for:

- `search_clinical_trials_by_indication`
- clinical trial sections of `generate_regulatory_digest`

Check:

- [ ] Registry is ClinicalTrials.gov only.
- [ ] Indication query is visible in `query_metadata`.
- [ ] Sponsor filter, if used, is visible and not over-expanded.
- [ ] Trial phase is reported without implying approval probability.
- [ ] Trial status is reported without implying success or failure.
- [ ] Intervention names are reported as registered record fields, not validated product identity.
- [ ] Official ClinicalTrials.gov URLs are preserved for important trials.
- [ ] Results availability is not treated as complete clinical evidence review.
- [ ] The output does not claim complete global trial activity.

Safe clinical interpretation pattern:

```text
The ClinicalTrials.gov MVP v1 result shows registered trial activity for [INDICATION]. This does not establish clinical success, approval probability, or complete global development activity.
```

Avoid:

```text
This product is likely to succeed because it has Phase 3 activity.
```

---

## Company Comparison Output Checklist

Use this section for:

- `compare_companies_by_indication`

Check:

- [ ] Comparison is clearly described as sponsor-name-based ClinicalTrials.gov activity only.
- [ ] Companies or sponsors are exactly listed in `query_metadata`.
- [ ] Trial counts are not treated as company quality rankings.
- [ ] Active trial count is not treated as development success.
- [ ] Completed trial count is not treated as positive outcome.
- [ ] Highest phase is not treated as approval probability.
- [ ] Sponsor-name matching is not treated as corporate family mapping.
- [ ] `date_range` is not described as an applied trial date filter in MVP v1.
- [ ] Data gaps are included in the summary.
- [ ] Manual verification is recommended for key trials and sponsor identity.

Required caveat when `date_range` is requested:

```text
In MVP v1, `date_range` is recorded in query metadata only. Date-based trial filtering is not applied.
```

Safe company comparison pattern:

```text
Company A shows more returned ClinicalTrials.gov trial activity than Company B in this query result. This is not evidence of clinical superiority, approval probability, or commercial strength.
```

Avoid:

```text
Company A is better than Company B.
```

---

## Digest Output Checklist

Use this section for:

- `generate_regulatory_digest`

Check:

- [ ] Digest type is clear: regulatory, clinical, or combined.
- [ ] Sources searched are listed.
- [ ] Search criteria are visible.
- [ ] Key regulatory updates include official URLs where available.
- [ ] Key clinical trial updates include ClinicalTrials.gov URLs where available.
- [ ] Impact matrix is treated as heuristic MVP output.
- [ ] Source health summary is included when requested.
- [ ] Known limitations are included.
- [ ] Manual follow-up actions are practical and source-linked.
- [ ] Executive summary does not overstate confidence.

Safe digest interpretation pattern:

```text
This digest is a rule-based MVP v1 summary for review. It should be used as a working intelligence draft, not as a final regulatory, clinical, or business decision.
```

Avoid:

```text
The digest confirms the final project action.
```

---

## Source Health / Failure Checklist

Use this section for:

- `check_source_health`
- `list_source_failures`
- source health sections of `generate_regulatory_digest`

Check:

- [ ] Source health status is reviewed before important analysis.
- [ ] Failed or degraded sources are named.
- [ ] Severity is reviewed.
- [ ] Suggested fix is preserved when available.
- [ ] Downstream outputs are caveated when a dependent source is degraded.
- [ ] Source health `pass` is not treated as proof of complete data coverage.
- [ ] Source failure records are treated as current snapshots only.
- [ ] Source failure records are not described as historical failure trends.

Safe source health pattern:

```text
Source health passed for the checked connector, but this does not prove complete data coverage. Important findings still require official source verification.
```

Safe source failure pattern:

```text
The source failure output reflects current source health status only. It should not be interpreted as a historical failure trend.
```

---

## Red Flag Phrases to Avoid

Avoid these phrases unless independently verified outside MVP v1:

- `confirmed final requirement`
- `agency equivalence is established`
- `no TFDA requirement exists`
- `no FDA requirement exists`
- `this product is likely to be approved`
- `Phase 3 means high approval probability`
- `completed trial means positive result`
- `recruiting trial means strong momentum`
- `Company A is better`
- `Company A is clinically superior`
- `Company A has stronger commercial potential`
- `source health passed, so the dataset is complete`
- `source failures show historical uptime trend`
- `digest determines the action`

---

## Safe Replacement Language

Use these instead:

| Risky wording | Safer wording |
|---|---|
| `confirmed final requirement` | `source-backed record requiring manual verification` |
| `no TFDA requirement exists` | `no MVP v1 TFDA result was returned; manual verification is needed` |
| `FDA and TFDA are aligned` | `returned FDA and TFDA records show similar themes, but this is not final agency equivalence` |
| `Phase 3 means likely approval` | `Phase 3 activity is present in the returned ClinicalTrials.gov records, but approval probability cannot be inferred` |
| `Company A is better` | `Company A has more returned trial activity in this query result` |
| `digest confirms action` | `digest suggests follow-up items for human review` |
| `source health pass means complete` | `source health passed for reachability or connector behavior, not complete data coverage` |

---

## Final Human Review Checklist

Before sending output to management, regulatory, CMC, clinical, QA, or external partners, confirm:

- [ ] Official URLs for key records were reviewed manually.
- [ ] Query scope and source scope are visible.
- [ ] MVP v1 limitations are included.
- [ ] Any source health issue is disclosed.
- [ ] Claims are limited to what the sources show.
- [ ] No unsupported approval, success, superiority, commercial, or final requirement conclusion is included.
- [ ] Follow-up actions are framed as review tasks, not final decisions.
- [ ] The summary can be traced back to source records and query metadata.

Recommended closing caveat:

```text
This summary is based on MVP v1 source-grounded outputs and requires manual verification through official source records before decision-making.
```
