# MVP Live Acceptance Validation Record — 2026-06-03

## Validation metadata

| Field | Value |
|---|---|
| Validation date | 2026-06-03 |
| Initial validation commit | c1bbeb0 Add MVP live acceptance validation runbook (#68) |
| Final validated commit | ad63804 Expose agencies in stdio regulatory search wrapper (#70) |
| Release/tag under validation | post-v0.2.12 live acceptance documentation checkpoint |
| Validator | fyz1500wr |
| Environment | GitHub Codespaces |
| Network / egress notes | FDA live source unavailable; TFDA and ClinicalTrials.gov health checks passed. |

## Current validation status

| Check | Status | Evidence / notes |
|---|---|---|
| Tool registry load | PASS | All 8 MVP tools present. |
| check_source_health | PARTIAL | Overall degraded because FDA source unavailable. |
| list_source_failures | PASS | FDA open high failure recorded. |
| FDA source health | BLOCKED_SOURCE | FDA guidance/RSS fetch failed. Do not interpret as zero FDA results. |
| TFDA source health | PASS | TFDA_DataAction available. |
| ClinicalTrials.gov source health | PASS | ClinicalTrialsGov_API available. |

## Interim conclusion

Current decision: ACCEPTANCE_VALIDATION_IN_PROGRESS

Do not tag v0.2.12 yet.
Do not update project state yet.
Continue live validation for TFDA and ClinicalTrials.gov.

## Live validation round 2 — TFDA and ClinicalTrials.gov checks

| Tool / check | Status | Evidence / notes |
|---|---|---|
| TFDA search_regulatory_updates | FAIL_CODE | Requested agencies=["TFDA"], but the tool returned FDA SOURCE_UNAVAILABLE. TFDA-only search should not fail because FDA is unavailable. |
| ClinicalTrials.gov search_clinical_trials_by_indication | PASS | Returned structured ClinicalTrials.gov records with trial_id, registry, official_url, sponsor, phase, status, product_modality, and query_metadata. |
| compare_companies_by_indication | PARTIAL | Returned structured company_comparison, landscape_summary, query_metadata, and non-superiority limitations. Sponsor-name matching limitations remain visible. |

## Blocking defect

| Item | Classification | Description | Required action |
|---|---|---|---|
| TFDA-only regulatory search blocked by FDA failure | TOOL_PARAMETER_DEFECT | `search_regulatory_updates(agencies=["TFDA"])` returned FDA source unavailable instead of isolating the query to TFDA. | Fix agency isolation / source error handling before accepting MVP for controlled use. |

## Updated interim decision

Current decision: DO_NOT_ACCEPT_YET

Reason: TFDA-only regulatory search is not isolated from FDA source failure.

Do not tag v0.2.12 yet.
Do not update project state yet.
Open a focused bugfix branch for regulatory agency isolation.

## Live validation round 3 — agency isolation fix verification

| Tool / check | Status | Evidence / notes |
|---|---|---|
| Direct Python TFDA regulatory search with agencies=["TFDA"] | PASS | Returned structured TFDA-scoped response with agency_searched=["TFDA"], sources_searched=["TFDA_HTML"], and no FDA SOURCE_UNAVAILABLE error. Result was NO_MATCHING_RECORDS, which is acceptable and not a source failure. |
| stdio wrapper TFDA regulatory search with agencies=["TFDA"] | PASS | Returned structured TFDA-scoped response with agency_searched=["TFDA"], sources_searched=["TFDA_HTML"], and no FDA SOURCE_UNAVAILABLE error. Confirms MCP wrapper now forwards agencies. |

## Blocking defect resolution

| Defect | Previous status | Current status | Evidence / notes |
|---|---|---|---|
| TFDA-only regulatory search blocked by FDA failure | FAIL_CODE | RESOLVED | PR #69 fixed core tool agency parsing; PR #70 exposed agencies through stdio MCP wrapper. Both direct Python and stdio wrapper now return TFDA-scoped responses. |

## Updated interim decision after round 3

Current decision: ACCEPTANCE_VALIDATION_IN_PROGRESS

Reason: Previous blocking agency isolation defect is resolved. Continue final digest validation with known FDA source limitation.

Do not tag v0.2.12 yet.
Do not update project state yet.

## Live validation round 4 — final digest validation

| Tool / check | Status | Evidence / notes |
|---|---|---|
| generate_regulatory_digest with agencies=["TFDA"] and registries=["ClinicalTrials.gov"] | PASS_WITH_LIMITATIONS | Returned structured digest output. sources_searched included TFDA and ClinicalTrials.gov. source_errors was empty. Digest included 0 regulatory update(s), 5 clinical trial update(s), and source_health_summary warning due to 1 open source failure. |
| FDA source limitation handling | PASS_WITH_LIMITATIONS | FDA remained unavailable as an open source health failure, but the TFDA + ClinicalTrials.gov digest was not blocked by FDA SOURCE_UNAVAILABLE. |
| Final MVP v0.2.12 live acceptance decision | ACCEPT_WITH_KNOWN_LIMITATIONS | MVP live validation passed for controlled use with known limitations: FDA source unavailable during validation, TFDA returned no matching records for the tested query, ClinicalTrials.gov returned structured trial data, digest output is rule-based and not a final regulatory/clinical assessment. |

## Final validation conclusion

Current decision: ACCEPT_WITH_KNOWN_LIMITATIONS

Accepted for controlled MVP use under the following conditions:

1. FDA live source was unavailable during validation and must be treated as BLOCKED_SOURCE, not as zero FDA results.
2. TFDA-only regulatory search is now isolated from FDA source failure after PR #69 and PR #70.
3. ClinicalTrials.gov search and company comparison returned structured MVP outputs.
4. Digest generation returned structured output for TFDA + ClinicalTrials.gov without source_errors.
5. Digest output remains rule-based and requires human review before regulatory, clinical, legal, medical, or competitive decisions.

Release recommendation: v0.2.12 may proceed to project-state update and release tagging after this validation record is committed and merged.

Do not tag v0.2.12 until the validation record PR and project state PR are merged.
