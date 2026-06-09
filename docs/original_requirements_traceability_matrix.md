# Original Requirements Traceability Matrix

## Purpose

This document maps the user's original full-system requirements to the current repository state. It is intended to prevent scope drift, clarify which capabilities are already implemented as MVP v1, and separate the regulatory-clinical intelligence core from later CMC readiness extension work.

This is a docs/spec-only governance document. It does not approve source expansion, add connectors, add MCP tools, create a runtime generator, or introduce scheduling, alerting, persistence, dashboards, HTTP/SSE transport, `.mcp.json`, GitHub automation, company alias mapping, corporate-family mapping, product ownership inference, or literature/patent/finance/news integrations.

## Source Documents Reviewed

Primary governing and status documents:

- `PROJECT_INSTRUCTION.md`
- `README.md`
- `CLAUDE.md`
- `.ai/PROJECT_STATE.md`
- `PROJECT_STATE_CONTINUATION.md`

Core design and workflow documents:

- `docs/source_priority_matrix.md`
- `docs/product_modality_taxonomy.md`
- `docs/mcp_tool_contract.md`
- `docs/data_dictionary.md`
- `workflows/regulatory_clinical_intelligence_workflow.md`
- `docs/post_mvp_source_expansion_decision_matrix.md`
- `docs/source_failure_diagnostic_runbook.md`
- `docs/live_source_behavior_notes.md`

Recent reporting and extension documents:

- `docs/regulatory_clinical_digest_report_workflow.md`
- `docs/regulatory_clinical_digest_report_template_contract.md`
- `docs/regulatory_clinical_digest_prompt_pack.md`
- `docs/regulatory_clinical_digest_clean_source_dry_run.md`
- `docs/cmc_submission_readiness_mapping_workflow.md`
- `docs/cmc_submission_readiness_mock_inventory.md`
- `docs/cmc_submission_readiness_input_template.md`

Relevant PR groups:

- PR #82: FDA abuse-detection source failure diagnostics
- PR #97-#103: regulatory-clinical digest/report docs-spec workflow
- PR #104-#112: CMC submission readiness docs/spec extension workflow
- PR #113: continuation handoff update with original requirements calibration

## Status Legend

| Status | Meaning |
|---|---|
| Complete | Implemented or documented sufficiently for the current approved scope. |
| MVP v1 subset | Implemented only for the approved MVP v1 source or tool boundary. |
| Partial | Some design or docs exist, but important scope, implementation, or validation gaps remain. |
| Extension | Useful related work, but not part of the original regulatory-clinical intelligence core. |
| Missing | Not yet formally designed, implemented, or validated. |
| Approval required | Should not proceed without explicit user approval or a source-expansion decision. |

## Traceability Matrix

| Original Requirement Area | Original Requirement Detail | Current Repo Evidence | Current Status | Approx. Completion | MVP v1? | Requires Source Expansion Approval? | Current Gap | Recommended Next Action |
|---|---|---|---|---:|---|---|---|---|
| GitHub/Codex build to Claude Project execution | Build the project and code in GitHub/Codex, then use Claude Project for execution through controlled instructions/tools. | `PROJECT_INSTRUCTION.md`, `README.md`, `CLAUDE.md`, `AGENTS.md`, `docs/claude_project_validation_workflow.md`, `docs/claude_code_web_mcp_smoke_test_note.md` | Partial | 70% | Yes | No | Governance and usage workflow exist, but execution still depends on manual Claude/Codex setup and environment-specific validation. | Keep workflow docs current; avoid adding GitHub automation or `.mcp.json` unless explicitly approved. |
| Regulatory agency tracking | Track FDA, EMA, TFDA, NMPA, and PMDA updates with official links and dates. | `PROJECT_INSTRUCTION.md`, `docs/source_priority_matrix.md`, `README.md` | MVP v1 subset | 45% | Partial | Yes for EMA/NMPA/PMDA | FDA and TFDA are MVP active. EMA, NMPA/CDE, and PMDA remain documented as later phases, not active sources. | Use `docs/post_mvp_source_expansion_decision_matrix.md` before any new agency connector or runtime source work. |
| Official-source-first retrieval | Prefer official APIs, official RSS, official open data portals, downloadable datasets, official HTML, then controlled fallback parser. | `docs/source_priority_matrix.md`, `workflows/regulatory_clinical_intelligence_workflow.md`, `docs/source_failure_diagnostic_runbook.md` | Complete for governance; MVP subset for implementation | 65% | Yes | Yes for new sources | Source priority rules exist, but only MVP active sources are implemented/validated. | Preserve official-source-first ordering in all future source-expansion decisions. |
| Date-window support | Support time windows from 1 month to 5 years. | `PROJECT_INSTRUCTION.md`, `docs/mcp_tool_contract.md`, `docs/regulatory_date_range_smoke_example.md` | MVP v1 subset | 55% | Yes | Yes for non-MVP agencies | Shared date ranges are documented and smoke-tested, but not validated across all original target agencies. | Keep date-window handling within existing MVP tools; validate per agency before source expansion. |
| Product modality filtering | Support regulatory/guidance retrieval by biologic product modality and broader therapeutic modality. | `docs/product_modality_taxonomy.md`, `docs/product_modality_regulatory_search_smoke_example.md`, `README.md` | Partial | 60% | Yes | Possibly for source-specific modality mapping | Broad `product_modality` taxonomy exists, but source-specific tagging quality and biologics-specific confidence remain limited. | Add future validation examples only after confirming they do not imply new runtime/source expansion. |
| Clinical trial tracking by indication/company | Track clinical trial progress and results by indication and company/vendor/sponsor using official registries where possible. | `README.md`, `docs/mcp_tool_contract.md`, `workflows/regulatory_clinical_intelligence_workflow.md`, `docs/clinical_trial_query_metadata_consistency_smoke_example.md` | MVP v1 subset | 55% | Yes | Yes for non-ClinicalTrials.gov registries | ClinicalTrials.gov API v2 is active. Sponsor/company matching remains name-based and does not infer corporate family, ownership, success, or superiority. | Keep sponsor association caveats explicit; do not add company alias DB or ownership inference without approval. |
| Clinical trial results awareness | Identify trial records and results availability without overclaiming clinical outcomes. | `docs/data_dictionary.md`, `docs/mcp_tool_contract.md`, `docs/regulatory_clinical_digest_report_workflow.md` | Partial | 45% | Yes | Yes for non-MVP registries | Results availability can be represented, but the system should not interpret success or regulatory impact without human review. | Maintain digest caveats and manual verification checklist. |
| Source failure and parser-change detection | Detect source/webpage/API/parser changes and support correction; notifications may be future design. | `docs/source_failure_diagnostic_runbook.md`, `docs/live_source_behavior_notes.md`, PR #82, `README.md` | Partial | 60% | Yes | No for MVP diagnostics; yes for advanced monitoring | Current source health is snapshot/diagnostic oriented. Historical source-health store, scheduler, and alerts are not implemented. | Keep diagnostics in MVP scope; require approval before scheduler, alert, persistence, or GitHub Issue automation. |
| MCP-based retrieval and analysis | Expose standardized MCP tools so Claude can query, summarize, compare, and generate reports without direct scraping. | `docs/mcp_tool_contract.md`, `README.md`, `CLAUDE.md` | MVP v1 subset | 70% | Yes | Yes for new tools/sources | 8 MVP tools exist. No new tools should be added unless a separate decision approves scope expansion. | Preserve current tool boundary and source caveats in reports. |
| Regulatory-clinical digest/reporting | Generate controlled PM/RA-facing summaries and digest memos from MVP tool outputs. | PR #97-#103, `docs/regulatory_clinical_digest_report_workflow.md`, `docs/regulatory_clinical_digest_report_template_contract.md`, `docs/regulatory_clinical_digest_prompt_pack.md` | Partial | 65% | Yes | No | Docs/spec workflow exists. Runtime generator and advanced report automation are not approved. | Continue using prompt/report contracts; do not add a runtime generator without approval. |
| Open-source skill/plugin/tool survey | Search or evaluate open-source skills/plugins/tools that may support Claude/Codex for at least one required function. | Mentioned in `PROJECT_STATE_CONTINUATION.md` original requirement baseline | Missing | 10% | No | Maybe | No formal artifact currently captures evaluated open-source skills/plugins/tools. | If prioritized, create a docs-only survey matrix before installing or integrating anything. |
| CMC readiness work | Map CMC workstreams, Module 3 gaps, vendor follow-up, method/stability dependency, critical path, and management-ready readiness drafts. | PR #104-#112, `docs/cmc_submission_readiness_mapping_workflow.md`, `docs/cmc_submission_readiness_mock_inventory.md`, `docs/cmc_submission_readiness_input_template.md` | Extension | 75% | No | No | Useful extension, but it is not the original regulatory-clinical intelligence core. Recent work risks narrowing the project toward CMC weekly reporting. | Pause CMC weekly template work; keep CMC readiness as an extension module until original-system gaps are recalibrated. |
| CMC weekly report template | Create a dedicated CMC weekly management report template. | PR #112 continuation/state context; `docs/cmc_submission_readiness_input_template.md` Prompt 6 | Approval required | 0% as standalone file | No | No | Explicit decision: do not create `docs/cmc_management_weekly_report_template.md` at this time. | Do not add this document unless the user explicitly approves a new CMC-reporting workstream. |

## MVP v1 vs Original Full-System Boundary

The current repository is best understood as a controlled MVP v1 plus documentation and extension workstreams. MVP v1 active sources are:

```text
FDA
TFDA
ClinicalTrials.gov
```

The original full-system target also includes EMA, NMPA/CDE, and PMDA. Those agencies are documented in planning and source-priority materials, but they are not currently active MVP runtime sources. Any work to activate them should start with a source-expansion decision document and should not jump directly to connector, MCP tool, scheduler, or report-generator implementation.

## CMC Readiness Extension Boundary

The CMC readiness documents are useful for PM/RA workflow design, especially for non-confidential Module 3 readiness mapping, vendor follow-up, method/stability dependency planning, and management summary stress testing.

However, CMC readiness is an extension module. It should not replace the original regulatory-clinical intelligence roadmap, and it should not automatically lead to a dedicated CMC weekly management report template.

## Explicit Out-of-Scope Items

The following remain out of scope unless explicitly approved:

- New runtime source connectors for EMA, NMPA/CDE, PMDA, EU CTIS, WHO ICTRP, literature, patents, finance, news, or commercial intelligence
- New MCP tools
- Runtime report generator
- Scheduler
- Alerts or notification system
- Dashboard
- Persistence or historical event store
- HTTP/SSE transport
- `.mcp.json`
- GitHub automation or GitHub Issue automation
- Company alias database
- Corporate-family mapping
- Product ownership inference
- Clinical success, approval probability, commercial strength, or company superiority inference
- CMC weekly management report template
- Storage of confidential, signed, GMP raw, QA-approved, official submission, vendor confidential, or non-public company records

## Recommended Next Workstream

Recommended next workstream after this matrix:

1. Keep the repo on the original regulatory-clinical intelligence MCP mainline.
2. Use this matrix to decide whether the next docs/spec work should be:
   - source expansion feasibility for EMA/NMPA/PMDA,
   - open-source skill/plugin/tool survey,
   - MVP v1 validation/handoff cleanup,
   - or a narrow source-health diagnostics refinement.
3. Do not continue into CMC weekly report template creation unless the user explicitly approves that separate extension workstream.

## Validation Plan

Recommended validation commands for this docs/spec-only change:

```bash
python -m pytest tests/test_project_state_release_tag_consistency.py -q
python -m pytest tests/test_readme_documentation_index.py -q
python -m pytest -q
git status --short
```

If using Claude Code Web or Codex Web only to validate, use an instruction such as:

```text
Do not modify files.
Do not commit.
Do not create a branch.
Do not create a pull request.
Only run the requested commands and report results.
```
