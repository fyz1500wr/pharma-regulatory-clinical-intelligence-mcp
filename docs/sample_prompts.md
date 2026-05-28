# Sample Prompts

## Purpose

This document provides copy-paste prompt examples for using the MVP v1 regulatory-clinical intelligence MCP tools safely.

It is written for users, Claude Project, Codex, and future maintainers who need practical prompts that keep the system inside MVP v1 scope.

These prompts are designed to:

- Use only MVP v1 active sources.
- Preserve source URLs and query metadata.
- Include known limitations.
- Avoid unsupported regulatory, clinical, commercial, or company-ranking conclusions.

---

## General Prompting Rules

When using this project, prompts should usually include these guardrails:

```text
Use MVP v1 active sources only: FDA, TFDA, and ClinicalTrials.gov.
Show official URLs where available.
Show query metadata and known limitations.
Do not infer clinical success, approval probability, commercial strength, or company superiority.
Do not treat missing results as proof that no requirement or activity exists.
Recommend manual verification before decision-making.
```

Avoid broad requests such as:

```text
Tell me which company is better.
Tell me the final regulatory requirement.
Tell me whether this product will be approved.
```

Use bounded requests such as:

```text
Summarize the available MVP v1 records and clearly state limitations.
Compare available trial activity without inferring superiority.
Identify official URLs and manual follow-up items.
```

---

## Regulatory Update Prompts

### Prompt 1: Search FDA and TFDA updates by topic

```text
Search FDA and TFDA regulatory updates related to [TOPIC] within MVP v1 scope.

Use only MVP v1 active regulatory sources:
- FDA
- TFDA

Return:
1. Key updates
2. Agency
3. Publication date
4. Document type or status if available
5. Product modality if available
6. Official URL
7. Known limitations
8. Recommended manual follow-up

Do not infer final regulatory requirements.
Do not conclude regulatory absence only because one agency has no result.
```

Use for:

- CMC guideline updates
- Quality updates
- Biologics updates
- Cell therapy updates
- Clinical trial regulation updates
- GMP or inspection-related updates

---

### Prompt 2: Search one agency only

```text
Search [FDA or TFDA] regulatory updates related to [TOPIC].

Return:
1. Matching records
2. Official URLs
3. Publication dates
4. Topics and product modality if available
5. Known limitations
6. Items that need manual verification

Use MVP v1 tools only.
Do not expand to EMA, PMDA, NMPA/CDE, WHO ICTRP, EU CTIS, literature, patents, finance, or commercial intelligence.
```

Use when the user wants a targeted single-agency search.

---

### Prompt 3: Find source-backed regulatory follow-up items

```text
Search MVP v1 regulatory updates for [TOPIC] and produce a practical follow-up list.

Return:
1. Source-backed updates with official URLs
2. Why each update may matter
3. What the project team should manually verify
4. Suggested owner function, such as CMC, clinical, QA, regulatory, or PM
5. Known limitations

Do not present the follow-up list as final regulatory advice.
```

Use when preparing meeting discussion items or PM follow-up tasks.

---

## Regulatory Comparison Prompts

### Prompt 4: Compare FDA vs TFDA updates by topic

```text
Compare FDA and TFDA regulatory updates related to [TOPIC].

Use MVP v1 tools only.
Focus on:
1. Similar themes
2. Differences in available records
3. Official URLs
4. Known limitations
5. What needs manual verification

Do not treat this comparison as final agency equivalence.
Do not infer that missing TFDA results mean no Taiwan requirement exists.
Do not infer final regulatory requirement mapping.
```

Use for quick FDA/TFDA landscape comparison.

---

### Prompt 5: Compare regulatory updates for a product modality

```text
Compare available FDA and TFDA updates related to [PRODUCT MODALITY], focusing on [TOPIC].

Examples of product modality:
- Small molecule
- Biologic
- Cell therapy
- Gene therapy
- Vaccine
- Combination product

Return:
1. Available records by agency
2. Shared themes
3. Agency-specific differences
4. Official URLs
5. Known limitations
6. Manual follow-up actions

Do not infer final agency alignment or divergence beyond the records found.
```

Use when the discussion is modality-specific.

---

### Prompt 6: Prepare a conservative regulatory comparison summary

```text
Prepare a conservative regulatory comparison summary for [TOPIC] using FDA and TFDA MVP v1 records.

Structure the answer as:
1. Executive summary
2. Source-backed findings
3. Similarities
4. Differences
5. Data gaps
6. Manual verification checklist

Do not make unsupported conclusions.
Do not treat the result as a final regulatory position.
```

Use for management updates or project discussion decks.

---

## Clinical Trial Landscape Prompts

### Prompt 7: Search ClinicalTrials.gov by indication

```text
Search ClinicalTrials.gov for clinical trial activity related to [INDICATION].

Return:
1. Key trials
2. Sponsors
3. Phase
4. Status
5. Intervention names
6. Official ClinicalTrials.gov URLs
7. Known limitations

Use MVP v1 ClinicalTrials.gov source only.
Do not infer clinical success, approval probability, or commercial strength.
```

Use for first-pass indication landscape review.

---

### Prompt 8: Search trials for an indication and sponsor

```text
Search ClinicalTrials.gov for [INDICATION] trials sponsored by [SPONSOR].

Return:
1. Trial identifiers
2. Trial titles
3. Phase
4. Status
5. Intervention names
6. Official URLs
7. Known limitations

Use sponsor-name matching conservatively.
Do not infer corporate family relationships unless explicitly supported by the source record.
```

Use when the user asks about one company or sponsor.

---

### Prompt 9: Summarize clinical trial activity without over-inference

```text
Summarize available ClinicalTrials.gov activity for [INDICATION].

Focus on:
1. Trial count in the returned result
2. Common phases
3. Common statuses
4. Sponsors appearing in the result
5. Key interventions
6. Known limitations
7. Manual verification needs

Do not infer clinical success.
Do not infer approval probability.
Do not infer market strength.
Do not treat ClinicalTrials.gov activity as complete global trial activity.
```

Use for safe landscape summaries.

---

## Company Trial Activity Comparison Prompts

### Prompt 10: Compare companies by indication

```text
Compare ClinicalTrials.gov trial activity for the following companies in [INDICATION]:

Companies:
- [COMPANY A]
- [COMPANY B]
- [COMPANY C]

Use sponsor-name-based comparison only.

Return:
1. Trial count by company
2. Active trial count
3. Completed trial count
4. Highest phase
5. Key trials
6. Data gaps
7. Known limitations

Do not infer company superiority.
Do not infer clinical success.
Do not infer approval probability.
Do not infer commercial strength.
```

Use for competitor activity comparison, not competitor quality ranking.

---

### Prompt 11: Compare companies with date range caveat

```text
Compare sponsor-name-based ClinicalTrials.gov trial activity for [COMPANY A] and [COMPANY B] in [INDICATION].

Record the requested date range as [DATE RANGE], but clearly state that MVP v1 records date_range in metadata only and does not apply date-based trial filtering.

Return:
1. Company-level trial activity
2. Key trials
3. Highest phase observed in returned results
4. Status distribution
5. Data gaps
6. Known limitations

Do not claim date-filtered completeness.
Do not infer clinical, regulatory, or commercial superiority.
```

Use when the user requests a time window.

---

### Prompt 12: Prepare a conservative company activity summary

```text
Prepare a conservative company trial activity summary for [INDICATION] using ClinicalTrials.gov MVP v1 data.

Companies:
- [COMPANY A]
- [COMPANY B]

Structure the answer as:
1. Summary of returned trial activity
2. Company-by-company table
3. Key trials requiring manual review
4. Data gaps
5. Known limitations
6. What cannot be concluded from this comparison

Explicitly state that this is not a company superiority assessment.
```

Use for practical internal discussion while preventing over-interpretation.

---

## Regulatory-Clinical Digest Prompts

### Prompt 13: Generate combined digest

```text
Generate a combined regulatory-clinical digest for [TOPIC / INDICATION / PRODUCT MODALITY].

Use MVP v1 active sources only:
- FDA
- TFDA
- ClinicalTrials.gov

Include:
1. Executive summary
2. Key regulatory updates
3. Key clinical trial updates
4. Impact matrix if available
5. Source health summary
6. Known limitations
7. Manual follow-up actions

Do not present this as a final regulatory or clinical assessment.
```

Use for weekly or project-level intelligence summaries.

---

### Prompt 14: Generate regulatory-only digest

```text
Generate a regulatory-only digest for [TOPIC] using FDA and TFDA MVP v1 sources.

Return:
1. Executive summary
2. Key source-backed updates
3. Official URLs
4. Impact considerations
5. Known limitations
6. Recommended manual follow-up

Do not include EMA, PMDA, NMPA/CDE, WHO ICTRP, EU CTIS, literature, patents, finance, or commercial intelligence.
Do not infer final regulatory requirements.
```

Use when the request is regulatory only.

---

### Prompt 15: Generate clinical-trial-only digest

```text
Generate a clinical-trial-only digest for [INDICATION] using ClinicalTrials.gov MVP v1 data.

Return:
1. Executive summary
2. Key clinical trial updates or trial activity
3. Sponsors
4. Phase and status overview
5. Official ClinicalTrials.gov URLs
6. Known limitations
7. Manual verification items

Do not infer clinical success, approval probability, or commercial strength.
```

Use when the request is clinical-trial focused.

---

### Prompt 16: Executive summary with limitations

```text
Create an executive summary from MVP v1 regulatory-clinical outputs for [TOPIC].

The summary must include:
1. What the sources show
2. What changed or may matter
3. What requires manual verification
4. Known limitations
5. What cannot be concluded

Keep the tone practical and conservative.
Do not overstate confidence.
Do not present heuristic impact as final assessment.
```

Use for management-facing summaries.

---

## Source Health and Failure Prompts

### Prompt 17: Check source health before analysis

```text
Check MVP v1 source health before generating analysis.

Sources:
- FDA
- TFDA
- ClinicalTrials.gov

Return:
1. Overall status
2. Failed or degraded sources
3. Severity
4. Suggested fix
5. Whether downstream analysis confidence should be downgraded

Do not treat source health pass as proof of complete data coverage.
Do not treat source failure records as historical failure trend data.
```

Use before important analysis runs.

---

### Prompt 18: Review source failures

```text
List current MVP v1 source failures and summarize operational impact.

Return:
1. Open failures
2. Source ID
3. Agency or registry
4. Failure type
5. Severity
6. Suggested fix
7. Which downstream analysis should be caveated

Make clear that MVP v1 source failures are current snapshots, not historical failure records.
```

Use when source health is degraded.

---

### Prompt 19: Add source caveats to a result

```text
Review the source health and source failure status, then add appropriate caveats to the analysis for [TOPIC].

Return:
1. Source health summary
2. Open failures if any
3. Affected source-dependent conclusions
4. Confidence downgrade notes
5. Manual follow-up items

Do not discard all analysis automatically because one source is degraded.
Do not overstate results from a degraded source.
```

Use when combining source health with a digest or comparison output.

---

## Bad Prompts and Better Prompts

### Company comparison

Bad:

```text
Compare Company A and Company B and tell me which one is better.
```

Better:

```text
Compare sponsor-name-based ClinicalTrials.gov trial activity for Company A and Company B in [INDICATION]. Do not infer clinical success, approval probability, commercial strength, or company superiority. Return trial counts, active/completed counts, highest phase, key trials, data gaps, and known limitations.
```

---

### Regulatory absence

Bad:

```text
TFDA did not show a result, so Taiwan has no relevant requirement, right?
```

Better:

```text
Search TFDA records related to [TOPIC]. If no MVP v1 result is found, state that no MVP v1 result was found and recommend manual verification before concluding regulatory absence.
```

---

### Approval probability

Bad:

```text
This company has Phase 3 trials. What is the chance of approval?
```

Better:

```text
Summarize the returned ClinicalTrials.gov trial activity for [COMPANY] in [INDICATION], including phase, status, sponsor, key trials, and known limitations. Do not infer approval probability.
```

---

### Regulatory final conclusion

Bad:

```text
Tell me the final FDA and TFDA requirement for this topic.
```

Better:

```text
Compare available FDA and TFDA MVP v1 records related to [TOPIC]. Return source-backed findings, official URLs, similarities, differences, data gaps, and manual verification checklist. Do not present the result as final regulatory requirement mapping.
```

---

### Digest overconfidence

Bad:

```text
Generate a digest and tell me what action to take.
```

Better:

```text
Generate a combined regulatory-clinical digest for [TOPIC] using MVP v1 sources only. Include executive summary, key regulatory updates, key clinical trial updates, source health, known limitations, and manual follow-up actions. Do not present heuristic impact as final decision-making advice.
```

---

## Copy-Paste Prompt Pack

### Copy-paste 1: Regulatory update search

```text
Search FDA and TFDA regulatory updates related to [TOPIC] within MVP v1 scope. Use only FDA and TFDA. Return key updates, official URLs, publication dates, product modality if available, known limitations, and recommended manual follow-up. Do not infer final regulatory requirements or regulatory absence.
```

### Copy-paste 2: FDA vs TFDA comparison

```text
Compare FDA and TFDA regulatory updates related to [TOPIC]. Use MVP v1 tools only. Return similar themes, differences in available records, official URLs, known limitations, and manual verification needs. Do not treat this as final agency equivalence or final regulatory requirement mapping.
```

### Copy-paste 3: Clinical trial landscape

```text
Search ClinicalTrials.gov for clinical trial activity related to [INDICATION]. Return key trials, sponsors, phase, status, intervention names, official ClinicalTrials.gov URLs, and known limitations. Do not infer clinical success, approval probability, or commercial strength.
```

### Copy-paste 4: Company trial activity comparison

```text
Compare sponsor-name-based ClinicalTrials.gov trial activity for [COMPANY A], [COMPANY B], and [COMPANY C] in [INDICATION]. Return trial count, active trial count, completed trial count, highest phase, key trials, data gaps, and known limitations. Do not infer company superiority, clinical success, approval probability, or commercial strength.
```

### Copy-paste 5: Combined regulatory-clinical digest

```text
Generate a combined regulatory-clinical digest for [TOPIC / INDICATION / PRODUCT MODALITY]. Use MVP v1 active sources only: FDA, TFDA, and ClinicalTrials.gov. Include executive summary, key regulatory updates, key clinical trial updates, impact matrix if available, source health summary, known limitations, and manual follow-up actions. Do not present this as a final regulatory or clinical assessment.
```

### Copy-paste 6: Source health check

```text
Check MVP v1 source health for FDA, TFDA, and ClinicalTrials.gov before generating analysis. Return overall status, failed or degraded sources, severity, suggested fix, and whether downstream analysis confidence should be downgraded. Do not treat source health pass as proof of complete data coverage.
```

### Copy-paste 7: Source failure review

```text
List current MVP v1 source failures and summarize operational impact. Return open failures, source ID, agency or registry, failure type, severity, suggested fix, and downstream analysis that should be caveated. Make clear that MVP v1 source failures are current snapshots, not historical failure records.
```

### Copy-paste 8: Executive summary with limitations

```text
Create an executive summary from MVP v1 regulatory-clinical outputs for [TOPIC]. Include what the sources show, what may matter, what requires manual verification, known limitations, and what cannot be concluded. Keep the tone practical and conservative. Do not overstate confidence.
```
