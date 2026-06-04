# Project State — Pharma Regulatory Clinical Intelligence MCP

Last updated: 2026-06-04

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`
Current stable branch: `main`
Current completed release: `v0.2.14-fda-blocked-source-interpretation-regression`

---

## 1. Current Status

The repository is now at a completed v0.2.15 main checkpoint after PR #82 merged FDA source-health diagnostics hardening into `main`. PR #83 was first merged into the PR #82 branch to address the HTTP 200 FDA abuse/apology-page feedback before the final PR #82 merge.

Latest confirmed main commit:

```text
b125447fbb54f42d2814bf891b5ec376995b6166
```

Latest confirmed release tag:

```text
v0.2.14-fda-blocked-source-interpretation-regression
```

Important release status:

- v0.2.15 is the latest completed main checkpoint after PR #82 merged, but it is not yet tagged.
- v0.2.14 remains the latest confirmed release tag until the v0.2.15 tag is created.
- PR #82 has been merged into `main` for FDA abuse-detection source failure diagnostics.
- Related PR #83 has been merged into the PR #82 branch to detect FDA abuse pages on successful HTTP 200 responses.
- The main checkpoint commit is `b125447fbb54f42d2814bf891b5ec376995b6166`.
- The release checkpoint commit is `b125447fbb54f42d2814bf891b5ec376995b6166`.
- The suggested release tag is `v0.2.15-fda-abuse-detection-source-failure-diagnostics`, but the tag has not yet been created.
- Final Codespaces validation on `main` passed with 202 tests.
- FDA abuse-detection/apology redirects remain source-access limitations surfaced as `SOURCE_UNAVAILABLE`, not zero FDA regulatory results.
- Digest output remains working intelligence and requires human review before regulatory, clinical, legal, medical, competitive, or commercial decisions.

---

## 2. Completed Work Since Previous Project State

### v0.2.3 — Offline regulatory date range smoke example

PR:

```text
#49 Add offline date range regulatory search smoke example
```

Main commit:

```text
68b1f59 Add offline date range regulatory search smoke example (#49)
```

Initial release tag:

```text
v0.2.3-offline-regulatory-date-range-smoke
```

Scope:

- Added offline mocked smoke example for `search_regulatory_updates(date_range=...)`.
- Added documentation for the date range smoke example.
- Added pytest wrapper for the smoke example.
- Added README documentation index entry.

Validation result on main after merge:

```text
python examples/offline_regulatory_date_range_smoke.py
offline regulatory date range smoke passed

python -m pytest -q
172 passed
```

Important interpretation:

Passing this offline smoke confirms the mocked date range normalization and filtering path. It does not validate live FDA or TFDA availability.

---

### v0.2.3.1 — Hotfix for smoke import path and README reminder

PR:

```text
#50 Fix offline date range smoke import path and README reminder
```

Main commit:

```text
66677e6 Fix offline date range smoke import path and README reminder (#50)
```

Patch release tag:

```text
v0.2.3.1-offline-regulatory-date-range-smoke-hotfix
```

Scope:

- Made `examples/offline_regulatory_date_range_smoke.py` robust when run from the repository root by explicitly adding the repository root to `sys.path`.
- Restored the README `Non-Expansion Reminder` text that was unintentionally removed during the v0.2.3 README index update.

Validation result on main after merge:

```text
python examples/offline_regulatory_date_range_smoke.py
offline regulatory date range smoke passed

python -m pytest -q
172 passed
```

---

### v0.2.4 — Bilingual product modality keyword taxonomy

PR:

```text
#51 Expand bilingual product modality keyword taxonomy
```

Main commit:

```text
79ba7f5 Expand bilingual product modality keyword taxonomy (#51)
```

Release tag:

```text
v0.2.4-bilingual-product-modality-taxonomy
```

Scope:

- Expanded MVP product modality keyword taxonomy with English and Traditional Chinese terms.
- Added regression tests for bilingual keyword classification.
- Preserved scope control: taxonomy/config/tests only.

Files changed:

```text
config/taxonomy/product_modality_keywords.yaml
tests/test_product_modality_classifier.py
```

Additional regression coverage:

- Bilingual English/Traditional Chinese keyword matching across MVP modality labels.
- ADC phrases should classify as `adc`, not plain `antibody`.
- `mRNA疫苗` should prioritize `mrna_rna` over general `vaccine`.
- Unresolved Chinese content should remain `requires_manual_review`.

Validation result on main after merge and corrected tag:

```text
python -m pytest tests/test_product_modality_classifier.py -q
10 passed

python -m pytest -q
176 passed
```

---

### v0.2.5 — Offline TFDA bilingual regulatory search smoke example

PR:

```text
#54 Add offline TFDA bilingual regulatory search smoke example
```

Main commit:

```text
1515075 Add offline TFDA bilingual regulatory search smoke example (#54)
```

Release tag:

```text
v0.2.5-offline-tfda-bilingual-regulatory-search-smoke
```

Scope:

- Added an offline mocked TFDA-style bilingual regulatory search smoke example.
- Added documentation for the TFDA bilingual regulatory search smoke example.
- Added pytest wrapper for the smoke example.
- Added README documentation index entry.
- Preserved scope control: offline example/docs/tests only.

Files added or updated:

```text
examples/offline_tfda_bilingual_regulatory_search_smoke.py
docs/tfda_bilingual_regulatory_search_smoke_example.md
tests/test_offline_tfda_bilingual_regulatory_search_smoke_example.py
README.md
```

Validated behavior:

- TFDA bilingual query retrieval for `mRNA疫苗`
- TFDA bilingual query retrieval for `抗體藥物複合體 ADC`
- TFDA bilingual query retrieval for `生物相似性藥品`
- product modality classification from Chinese title and summary text
- `product_modality="mrna_rna"`
- `product_modality="adc"`
- `product_modality="biosimilar"`
- `product_modality` as a list of strings
- no-result behavior after product modality filtering
- invalid `product_modality` structured error handling
- `query_metadata.filters_applied.query`
- `query_metadata.filters_applied.product_modality`

Validation result on main after merge:

```text
python examples/offline_tfda_bilingual_regulatory_search_smoke.py
offline TFDA bilingual regulatory search smoke passed

python -m pytest tests/test_offline_tfda_bilingual_regulatory_search_smoke_example.py -q
1 passed

python -m pytest -q
177 passed
```

Important interpretation:

Passing this offline smoke confirms the TFDA-style bilingual query retrieval and product modality filter path in mocked records. It does not validate live TFDA source availability.

---

### v0.2.6 — Offline smoke example conventions

PR: #56 Add offline smoke example conventions

Main commit: 4cd8108 Add offline smoke example conventions (#56)

Release tag: v0.2.6-offline-smoke-example-conventions

Scope:
- Added documentation-only conventions for future offline smoke examples.
- Added README documentation index entry.
- Refreshed the v0.2.5 tag correction note.
- Preserved scope control: documentation and project-state text only.

Files added or updated:
- docs/offline_smoke_example_conventions.md
- README.md
- .ai/PROJECT_STATE.md

Documented conventions:
- Offline smoke example naming pattern.
- Example script structure.
- Documentation structure.
- Pytest wrapper structure.
- README index rule.
- Scope-control boundaries.
- Validation expectations.

Validation result:
- docs/offline_smoke_example_conventions.md exists.
- README index contains docs/offline_smoke_example_conventions.md.
- v0.2.6 tag points to 4cd8108.

Important interpretation:
This is a documentation-only maintenance release. It does not validate runtime behavior and does not add source scope, MCP tools, tests, .mcp.json changes, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, GitHub issue automation, or external integrations.

---

### v0.2.7 — Release handoff checklist

PR: #58 Add release handoff checklist

Main commit: 633cf4b Add release handoff checklist (#58)

Release tag: v0.2.7-release-handoff-checklist

Scope:
- Added documentation-only release/tag/project-state handoff checklist.
- Added README documentation index entry.
- Preserved scope control: documentation only.

Files added or updated:
- docs/release_handoff_checklist.md
- README.md
- .ai/PROJECT_STATE.md

Documented checklist coverage:
- Pre-branch status check.
- Branch naming.
- Scope check before implementation.
- Safe implementation rules.
- Pre-PR validation.
- PR review checklist.
- Merge-before-tag rule.
- Post-merge main sync.
- Tag creation and tag correction rule.
- Project-state update rule.
- Final verification.
- Branch cleanup.
- Handoff note for next work.
- Stop conditions.

Important interpretation:
This is a documentation-only maintenance release. It does not add runtime behavior, tests, source scope, MCP tools, .mcp.json changes, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, GitHub issue automation, or external integrations.

---

### v0.2.8 — README documentation index consistency test

PR: #60 Add README documentation index consistency test

Main commit: 4ef8953 Add README documentation index consistency test (#60)

Release tag: v0.2.8-readme-documentation-index-consistency

Scope:
- Added test-only regression coverage for README Post-MVP Documentation Index consistency.
- Preserved scope control: test only.

Files added or updated:
- tests/test_readme_documentation_index.py
- .ai/PROJECT_STATE.md

Validation result:
- Focused test passed: 5 passed.
- Full test suite passed: 182 passed.

Test coverage added:
- Confirms Post-MVP Documentation Index exists.
- Confirms expected index entries are present.
- Confirms indexed docs and .ai/PROJECT_STATE.md paths exist.
- Confirms no duplicate index entries.
- Confirms release_handoff_checklist.md is indexed with expected scope text.

Important interpretation:
This is a test-only maintenance release. It does not add runtime behavior, source scope, MCP tools, .mcp.json changes, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, GitHub issue automation, or external integrations.

---

### v0.2.9 — Project-state release/tag consistency test

PR: #62 Add project state release tag consistency test

Main commit: 0c27888 Add project state release tag consistency test (#62)

Release tag: v0.2.9-project-state-release-tag-consistency

Scope:
- Added test-only regression coverage for `.ai/PROJECT_STATE.md` release/tag consistency.
- Added checks that visible source-scope and expansion guardrails remain present.
- Preserved scope control: test only.

Files added or updated:
- tests/test_project_state_release_tag_consistency.py
- .ai/PROJECT_STATE.md

Validation result:
- Focused test passed: 5 passed.
- Full test suite passed: 187 passed.

Test coverage added:
- Confirms `Current completed release` matches `Latest confirmed release tag`.
- Confirms release tag naming follows `vX.Y.Z-*` format.
- Confirms latest confirmed main commit is an ancestor of current HEAD.
- Confirms the current release section mentions release tag, PR, and main commit.
- Confirms recommended next version is present.
- Confirms current source-scope and expansion guardrails remain visible.

Important interpretation:
This is a test-only maintenance release. It does not add runtime behavior, source scope, MCP tools, .mcp.json changes, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, GitHub issue automation, or external integrations.

---

### v0.2.10 — Query metadata consistency offline smoke

PR: #64 Add query metadata consistency offline smoke

Main commit: 92ffc82 Add query metadata consistency offline smoke (#64)

Release tag: v0.2.10-query-metadata-consistency-offline-smoke

Scope:
- Added an offline mocked query metadata consistency smoke example for FDA-style and TFDA-style regulatory search outputs.
- Added pytest wrapper for the smoke example.
- Added documentation for the query metadata consistency smoke example.
- Added README Post-MVP Documentation Index entry.
- Updated README documentation index consistency test expected entries.
- Preserved scope control: offline example/docs/tests only.

Files added or updated:
- examples/offline_query_metadata_consistency_smoke.py
- tests/test_offline_query_metadata_consistency_smoke_example.py
- docs/query_metadata_consistency_smoke_example.md
- README.md
- tests/test_readme_documentation_index.py
- .ai/PROJECT_STATE.md

Validation result after PR #64 merge and main sync:
- Focused smoke test passed: 1 passed.
- README documentation index test passed: 5 passed.
- Project-state release/tag consistency test passed: 5 passed.
- Full test suite passed: 188 passed.

Validated behavior:
- FDA regulatory record metadata contract.
- TFDA regulatory record metadata contract.
- `query_metadata` agency and source contract.
- `query_metadata.filters_applied.query` contract.
- `query_metadata.filters_applied.product_modality` contract.
- `query_metadata.filters_applied.date_range` contract.
- Derived `date_from` / `date_to` metadata from `date_range="1m"`.
- FDA/TFDA `query_metadata` key consistency.
- FDA/TFDA `filters_applied` key consistency.
- FDA/TFDA normalized record key consistency.

Important interpretation:
This offline smoke validates normalized regulatory search metadata consistency across mocked FDA and TFDA records. It does not validate live FDA/TFDA source availability and does not add source scope, MCP tools, `.mcp.json` changes, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, GitHub issue automation, EMA/NMPA/PMDA/WHO ICTRP/EU CTIS, literature, patent, or finance integrations.

---

### v0.2.11 — Clinical trial query metadata consistency offline smoke

PR: #66 Add clinical trial query metadata consistency offline smoke

Main commit: 99532d2 Add clinical trial query metadata consistency offline smoke (#66)

Release tag: v0.2.11-clinical-trial-query-metadata-consistency-offline-smoke

Scope:
- Added an offline ClinicalTrials.gov-style clinical trial query metadata consistency smoke example.
- Added pytest wrapper for the smoke example.
- Added documentation for the clinical trial query metadata consistency smoke example.
- Added README Post-MVP Documentation Index entry.
- Updated README documentation index consistency test expected entries.
- Preserved scope control: offline example/docs/tests only.

Files added or updated:
- examples/offline_clinical_trial_query_metadata_consistency_smoke.py
- tests/test_offline_clinical_trial_query_metadata_consistency_smoke_example.py
- docs/clinical_trial_query_metadata_consistency_smoke_example.md
- README.md
- tests/test_readme_documentation_index.py
- .ai/PROJECT_STATE.md

Validation result after PR #66 merge and main sync:
- Offline smoke script passed.
- Focused smoke test passed: 1 passed.
- README documentation index test passed: 5 passed.
- Project-state release/tag consistency test passed: 5 passed.
- Full test suite passed: 189 passed.

Validated behavior:
- ClinicalTrials.gov normalized trial metadata contract.
- Clinical trial indication query metadata contract.
- Clinical trial sponsor/company query metadata contract.
- Clinical trial `date_range` metadata recorded but not applied.
- Clinical trial `product_modality` filter metadata contract.
- Clinical trial `phase` filter metadata contract.
- Clinical trial `include_completed_trials` metadata contract.
- Clinical trial `include_results` metadata contract.
- Clinical trial `official_url` and `results_available` fields.

Important interpretation:
This offline smoke validates ClinicalTrials.gov-style clinical trial query metadata consistency across mocked records. It does not validate live ClinicalTrials.gov source availability and does not add source scope, MCP tools, `.mcp.json` changes, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, GitHub issue automation, EMA/NMPA/PMDA/WHO ICTRP/EU CTIS, literature, patent, or finance integrations.

---


### v0.2.12 — MVP live acceptance validation

PR: #71 Add v0.2.12 live acceptance validation record

Main commit: b7c6102 Add v0.2.12 live acceptance validation record (#71)

Release tag: v0.2.12-mvp-live-acceptance-validation

Scope:
- Added MVP live acceptance validation runbook and results template.
- Ran live source health validation for FDA, TFDA, and ClinicalTrials.gov.
- Confirmed FDA live source was unavailable during validation and recorded it as a source health limitation.
- Confirmed TFDA and ClinicalTrials.gov source health paths were available.
- Fixed `search_regulatory_updates(agencies=["TFDA"])` agency isolation so TFDA-only search is not blocked by FDA source failure.
- Exposed `agencies` through the stdio MCP wrapper for `search_regulatory_updates`.
- Added focused regression tests for agency isolation and stdio wrapper forwarding.
- Added live acceptance validation record documenting final `ACCEPT_WITH_KNOWN_LIMITATIONS` decision.
- Preserved MVP source scope: FDA, TFDA, ClinicalTrials.gov only.

Files added or updated:
- docs/mvp_live_acceptance_validation_runbook.md
- docs/mvp_live_acceptance_validation_results_template.md
- docs/validation_records/mvp_live_acceptance_validation_2026-06-03.md
- src/mcp_server/tools_regulatory.py
- src/mcp_server/stdio_server.py
- tests/test_regulatory_search_agency_isolation.py
- tests/test_stdio_regulatory_agencies_wrapper.py
- tests/test_readme_documentation_index.py
- README.md
- .ai/PROJECT_STATE.md

Validation result after PR #70 merge and main sync:
- `pytest tests/test_stdio_regulatory_agencies_wrapper.py -q`: 1 passed.
- `pytest tests/test_regulatory_search_agency_isolation.py -q`: 2 passed.
- `pytest -q`: 192 passed.

Live validation result:
- Tool registry loaded all 8 MVP tools.
- `check_source_health` returned degraded status because FDA was unavailable.
- `list_source_failures` reported one open high FDA source failure.
- Direct Python TFDA-only regulatory search with `agencies=["TFDA"]` returned a structured TFDA-scoped response with no FDA `SOURCE_UNAVAILABLE` error.
- stdio wrapper TFDA-only regulatory search with `agencies=["TFDA"]` returned a structured TFDA-scoped response with no FDA `SOURCE_UNAVAILABLE` error.
- ClinicalTrials.gov indication search returned structured trial records.
- Company comparison by indication returned structured comparison output with known non-superiority limitations.
- Final digest validation for TFDA + ClinicalTrials.gov returned structured output with `sources_searched` including TFDA and ClinicalTrials.gov, empty `source_errors`, 0 regulatory update(s), 5 clinical trial update(s), and source health warning due to one open FDA source failure.

Important interpretation:
v0.2.12 validates the controlled MVP live acceptance path under known source-health limitations. It does not claim complete FDA availability, complete TFDA recall, complete ClinicalTrials.gov recall, final regulatory assessment, final clinical assessment, legal advice, medical advice, or competitive superiority.

---

### v0.2.13 — Post-live validation cleanup and release hardening

PR: #74 Update project state after v0.2.13

Related PR: #73 Harden v0.2.13 live validation and release handoff docs

Main commit: 152e091 Update project state after v0.2.13 (#74)

Release checkpoint commit: 152e091 Update project state after v0.2.13 (#74)

Release tag: v0.2.13-post-live-validation-release-hardening

Status: confirmed tagged release after PR #73 and PR #74 were merged into `main`.

Scope:
- Documentation-only hardening.
- Updated MVP live acceptance validation runbook Step 8.
- Added primary digest validation path for FDA + TFDA when FDA is reachable.
- Added fallback digest validation path for TFDA-only when FDA is BLOCKED_SOURCE.
- Clarified BLOCKED_SOURCE is a source-health limitation, not a zero-result regulatory finding.
- Clarified digest output remains working intelligence, not final regulatory, clinical, legal, medical, competitive, or commercial assessment.
- Updated release handoff checklist to clarify project-state-before-tag flow.
- Added explicit warning not to ask for merge again after a PR has already been merged.
- Preserved MVP source scope: FDA, TFDA, ClinicalTrials.gov only.

Files updated:
- docs/mvp_live_acceptance_validation_runbook.md
- docs/release_handoff_checklist.md
- .ai/PROJECT_STATE.md

Validation before tag creation on main:
- pytest tests/test_readme_documentation_index.py -q: 5 passed
- pytest -q: 192 passed

Important interpretation:
v0.2.13 does not add sources, tools, runtime behavior, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, .mcp.json, or GitHub automation. It only hardens documentation and release handoff guidance after v0.2.12 live acceptance validation, then records the post-tag project-state checkpoint.

---

### v0.2.14 — FDA blocked-source interpretation regression

PR: #77 Update project state after v0.2.14 regression

Related PR: #76 Add v0.2.14 FDA blocked-source interpretation regression

Main commit: 2ce8ac8 Update project state after v0.2.14 regression (#77)

Release checkpoint commit: 2ce8ac8 Update project state after v0.2.14 regression (#77)

Release tag: v0.2.14-fda-blocked-source-interpretation-regression

Status: confirmed tagged release after PR #76 and PR #77 were merged into `main`.

Scope:
- Test-only source-resilience regression.
- Added deterministic offline comparison regression for FDA `BLOCKED_SOURCE` / `SOURCE_UNAVAILABLE`.
- Added deterministic offline digest regression for FDA source failure plus usable TFDA/ClinicalTrials.gov output.
- Confirmed FDA source failure remains visible in `partial_lookup_failures` or `query_metadata.source_errors`.
- Confirmed FDA failure is not silently converted into `FDA: 0 matching update(s)`.
- Confirmed TFDA zero-result behavior remains distinguishable from FDA source failure.
- Preserved MVP source scope: FDA, TFDA, ClinicalTrials.gov only.

Files added or updated:
- tests/test_regulatory_search_agency_isolation.py
- tests/test_digest_fda_blocked_source_interpretation.py

Validation:
- pytest tests/test_regulatory_search_agency_isolation.py -q: 3 passed
- pytest tests/test_digest_fda_blocked_source_interpretation.py -q: 1 passed
- pytest tests/test_project_state_release_tag_consistency.py -q: 5 passed
- pytest -q: 194 passed

Important interpretation:
This is a test-only regression checkpoint. It does not add new source agencies, MCP tools, runtime behavior, `.mcp.json` changes, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, GitHub automation, EMA/NMPA/PMDA/WHO ICTRP/EU CTIS, literature, patent, or finance integrations.

---


### v0.2.15 — FDA abuse-detection source failure diagnostics

PR: #82 Improve FDA abuse-detection source failure diagnostics

Related PR: #83 Detect FDA abuse pages on successful responses

Main commit: b125447fbb54f42d2814bf891b5ec376995b6166 Improve FDA abuse-detection source failure diagnostics (#82)

Release checkpoint commit: b125447fbb54f42d2814bf891b5ec376995b6166 Improve FDA abuse-detection source failure diagnostics (#82)

Pending release tag: v0.2.15-fda-abuse-detection-source-failure-diagnostics

Suggested release tag: `v0.2.15-fda-abuse-detection-source-failure-diagnostics`

Status: completed main checkpoint; tag not yet created

Scope:
- Source-health diagnostics hardening.
- Preserves FDA abuse-detection/apology redirect as `SOURCE_UNAVAILABLE`.
- Prevents FDA abuse/apology responses from being interpreted as `NO_MATCHING_RECORDS`.
- Handles both HTTP error responses and HTTP 200 abuse/apology page responses.
- Improves structured failure details with `requested_url`, `final_url`, `status_code`, `detected_source_block`, and `redirected_to_abuse_detection`.
- Improves source-health `suspected_cause` / `known_limitations` for FDA abuse-detection redirects.
- Fixes example import path for offline product modality regulatory search smoke.
- Preserves MVP source scope: FDA, TFDA, ClinicalTrials.gov only.

Files changed by completed PR:
- examples/offline_product_modality_regulatory_search_smoke.py
- src/connectors/fda/fda_updates_client.py
- src/mcp_server/tools_healthcheck.py
- tests/test_digest_fda_blocked_source_interpretation.py
- tests/test_fda_updates_client.py

Validation:
- pytest tests/test_fda_updates_client.py -q: 23 passed
- pytest tests/test_regulatory_search_agency_isolation.py -q: 3 passed
- pytest tests/test_digest_fda_blocked_source_interpretation.py -q: 2 passed
- pytest tests/test_project_state_release_tag_consistency.py -q: 5 passed
- pytest -q: 202 passed

Important interpretation:
- v0.2.15 does not restore FDA live access when FDA blocks the runtime.
- v0.2.15 does not bypass FDA source controls.
- v0.2.15 does not add scraping workaround, new source agencies, new MCP tools, `.mcp.json` changes, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, GitHub automation, EMA/NMPA/PMDA/WHO ICTRP/EU CTIS, literature, patent, or finance integrations.
- v0.2.15 only hardens source-failure diagnostics and interpretation so FDA abuse-detection/apology responses remain source-access limitations, not zero-result findings.

---

## 3. Important Workflow Correction

Use this workflow for future PRs:

```text
Create branch → implement → run focused tests → run full tests → open PR → confirm mergeable/review comments → merge → pull main → rerun relevant tests → tag
```

Do not tag before confirming that the PR has actually been merged into `main`.

Do not suggest merge before running tests when the PR branch can be tested in Codespaces.

---

## 4. Current Guardrails

MVP source scope remains limited to:

```text
FDA
TFDA
ClinicalTrials.gov
```

Do not add the following unless explicitly approved:

- Additional agencies such as EMA, NMPA, PMDA, WHO ICTRP, EU CTIS
- Literature integration
- Patent integration
- Finance integration
- Scheduler
- Alerts
- Persistence layer
- Dashboard
- HTTP/SSE transport
- GitHub issue automation
- New MCP tools
- `.mcp.json` changes

For uncertain work, keep the implementation smaller and document limitations clearly.

---

## 5. Current Known Notes

### Testing environment

The Codespaces environment may not always have dev dependencies installed. If `pytest` is missing, install the project with dev dependencies first:

```bash
python -m pip install -e ".[dev]"
```

Do not commit generated or accidental dependency files such as `poetry.lock` unless dependency management is explicitly approved as part of the task.

### Direction calibration rule

After a sequence of similar PRs, the assistant/project workflow must pause for direction calibration before proposing or executing the next same-type PR. This rule is intended to prevent uncontrolled scope drift and over-narrowing around local documents.

### Product modality classifier behavior

The current classifier is keyword mapping driven. v0.2.4 expanded the mapping and tests without changing core classifier logic.

Current classifier priority is determined by the order of labels in `config/taxonomy/product_modality_keywords.yaml`. This is intentional for the current MVP implementation and is covered by tests for ADC and mRNA vaccine priority behavior.

---

## 6. Recommended Next Step

Recommended next version:

```text
v0.2.15 — release tag creation — v0.2.15-fda-abuse-detection-source-failure-diagnostics
```

Recommended options:

- Create the v0.2.15 tag after the project-state PR merges.
- Then run final tag verification.
- Then pause for direction calibration before another same-type PR.
- Keep any follow-up small and controlled.
- Do not add new agencies or sources without explicit approval.
- Preserve the interpretation that blocked FDA source access is a source-health limitation, not a zero-result finding.

Keep the next step small and phase-controlled.

Do not add new source scope, MCP tools, `.mcp.json` changes, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, GitHub issue automation, EMA/NMPA/PMDA/WHO ICTRP/EU CTIS, literature, patent, or finance integrations.
