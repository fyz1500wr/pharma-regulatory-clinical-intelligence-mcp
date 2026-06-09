# Project State Continuation

Created: 2026-06-04  
Updated: 2026-06-09

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`

This file is a compact continuation handoff for starting a new chat. Canonical detailed status remains in `.ai/PROJECT_STATE.md`.

## Current checkpoint

- Stable branch: `main`
- Latest confirmed merged PR: PR #112
- PR #112 merge commit: `b0c406e11b2bfc4db371fde7aadb363a23f76d13`
- Latest completed workstream: CMC submission readiness docs/spec workflow through mapping workflow, mock inventory, input template / prompt pack, management summary prompt revision, second mock management weekly reporting stress test, and state/handoff sync.
- Latest validation status: `PASS`
- Latest validation evidence from Claude Code on PR #112 branch `sync-project-state-after-management-summary-prompt` at HEAD `8126480` / `81264808b4a3fefb3506992a19930b5ccb0c6904`:
  - `python -m pytest tests/test_project_state_release_tag_consistency.py -q` → `5 passed in 0.02s`
  - `python -m pytest tests/test_readme_documentation_index.py -q` → `10 passed in 0.02s`
  - `python -m pytest -q` → `212 passed in 2.79s`
  - `git status --short` → clean / no output
- Current tagged release: remains `v0.2.15-fda-abuse-detection-source-failure-diagnostics`; no new release tag was created for PR #97–#112 docs/product workflow work.
- Open PRs at this checkpoint: none known after PR #112 merge.
- Execution environment note: Codespaces quota is near limit until July 2026. For upcoming code/test work, default to Claude Code Web and Codex Web workflows. Do not assume Codespaces is available unless the user explicitly says it is available again.

## Original user requirement baseline

The project is in build-stage and must be evaluated against the user's original full-system requirements, not only the latest CMC workstream.

Original target system:

1. Build a GitHub-based system architecture where project and code construction happen in Codex/GitHub, then the final usable knowledge/workflow is moved into Claude Project for execution.
2. Track updates from regulatory agencies and industry guidance sources:
   - FDA
   - EMA
   - TFDA
   - NMPA
   - PMDA
   - include dates and official document links
   - support date windows from 1 month to 5 years
3. Support regulatory/guidance retrieval by biologic product modality.
4. Track clinical trial progress and results by indication and company/vendor/sponsor, preferably using official clinical registry APIs.
5. Detect source/webpage/API/parser changes and support timely correction, ideally through source-health diagnostics and later notification/escalation design.
6. Prefer official APIs where available and use MCP-based retrieval.
7. Search or evaluate open-source skills/plugins/tools that can support Claude and/or Codex for at least one of the functions above.

## Current alignment to original requirements

Current rough alignment against the original target:

```text
Original Regulatory / Clinical Intelligence MCP system: about 45–50% complete
Project governance / GitHub + Claude/Codex workflow foundation: about 70% complete
CMC readiness extension module: about 75% complete
Overall build-stage system: about 55–60% complete
```

Interpretation:

- The repo has a strong governance, guardrail, state/handoff, and docs/spec foundation.
- The repo has a useful MVP regulatory-clinical intelligence subset using FDA, TFDA, and ClinicalTrials.gov.
- The repo has a useful CMC readiness docs/spec extension.
- The repo has not yet completed the original multi-agency regulatory tracking target because EMA, NMPA, and PMDA are not active MVP sources.
- The repo has not yet implemented scheduler, alerting, persistence, dashboard, source-change notification, or multi-source runtime automation.
- The repo has not yet captured the open-source skill/plugin survey as a formal project artifact.

## Current MVP source scope and deliberate limitation

Approved MVP v1 active source scope remains:

```text
FDA
TFDA
ClinicalTrials.gov
```

This is a deliberate MVP subset, not the full original source scope.

Do not add EMA, NMPA/CDE, PMDA, EU CTIS, WHO ICTRP, literature, patent, finance, news, company alias database, corporate-family mapping, product ownership inference, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, `.mcp.json`, GitHub automation, or other integrations unless explicitly approved.

If the next workstream requires source expansion, first create or update a source feasibility / traceability document. Do not immediately implement connectors.

## Recent relevant PR sequence

### PR #97–#103 — Regulatory-clinical digest/report docs-spec workstream

Completed a controlled PM/RA digest/report documentation workstream:

```text
docs/regulatory_clinical_digest_report_workflow.md
docs/regulatory_clinical_digest_example_memo.md
docs/regulatory_clinical_digest_prompt_pack.md
docs/regulatory_clinical_digest_memo_validation_exercise.md
docs/regulatory_clinical_digest_report_template_contract.md
docs/regulatory_clinical_digest_clean_source_dry_run.md
```

Purpose:

- Turn MVP tool outputs into PM/RA-facing regulatory-clinical intelligence memo drafts.
- Preserve source coverage caveats and sponsor/company association caveats.
- Keep reporting docs/spec-only and avoid runtime report generator work without explicit approval.

### PR #104–#112 — CMC submission readiness docs/spec workstream

Completed a controlled CMC readiness extension:

```text
docs/cmc_submission_readiness_mapping_workflow.md
docs/cmc_submission_readiness_mock_inventory.md
docs/cmc_submission_readiness_input_template.md
.ai/PROJECT_STATE.md
PROJECT_STATE_CONTINUATION.md
```

Purpose:

- Provide docs/spec-only CMC readiness mapping, mock inventory, input template, and prompt pack.
- Support Module 3 gap matrix, vendor follow-up, method/stability dependencies, critical path, PM actions, and management summary drafting.
- Revise Prompt 6 for recurring mock management weekly report generation.
- Confirm via second stress test that `docs/cmc_management_weekly_report_template.md` is not currently justified.

Important decision:

```text
Do not create docs/cmc_management_weekly_report_template.md at this time.
```

## Current guardrails

- Keep MVP source scope limited to FDA, TFDA, and ClinicalTrials.gov unless source expansion is explicitly approved.
- Keep future work small and phase-controlled.
- Use Traditional Chinese for user-facing discussion.
- Avoid accidental Japanese output.
- After repeated related PRs, pause for direction calibration before continuing.
- The repo is not a GMP, QA, EDMS, eCTD publishing, official submission, clinical decision support, legal decision, medical decision, commercial intelligence, or management decision system.
- Do not store confidential, signed, GMP raw, QA-approved, official submission, vendor confidential, or non-public company records in this repo.
- If validation is requested, use Claude Code Web or Codex Web first due to Codespaces quota limits.
- If asking Claude Code/Codex only to validate, explicitly instruct: do not modify files, do not commit, do not create branch, do not create PR.

## Risk of scope drift / narrowing

The recent PR #104–#112 sequence was useful but narrowed attention toward CMC readiness and weekly management reporting.

This is acceptable as a completed extension module, but it is not the full original system.

Do not continue adding CMC weekly-report documents, CMC dashboards, or CMC automation unless the user explicitly chooses that as the next workstream.

The next step should re-anchor the project to the original multi-agency regulatory / clinical intelligence MCP architecture.

## Recommended immediate next step

Recommended next action:

```text
Create a docs/spec-only original requirements traceability matrix before implementing anything else.
```

Suggested file:

```text
docs/original_requirements_traceability_matrix.md
```

Purpose:

- Map the user's original requirements to current repo capabilities.
- Identify what is complete, partial, missing, out-of-scope, or intentionally deferred.
- Distinguish original-system core requirements from CMC readiness extension work.
- Prevent the project from drifting further into narrow CMC weekly-report work.
- Define the next workstream deliberately.

The matrix should cover at least:

| Original Requirement Area | Current Status | Rough Completion | Current Repo Evidence | Gap | Next Workstream Candidate |
|---|---:|---:|---|---|---|
| Multi-agency regulatory tracking: FDA/EMA/TFDA/NMPA/PMDA | Partial | 35–45% | FDA/TFDA MVP docs/tools/specs | EMA/NMPA/PMDA inactive | Source expansion feasibility matrix |
| Date range 1 month to 5 years, dates and official links | Partial | 40–50% | Digest/report contract fields | Needs multi-source date-range validation | Date-range test plan |
| Biologic modality search | Early | 30–40% | Product modality input fields | Needs taxonomy and validation | Biologic modality taxonomy |
| Indication/company clinical trial tracking and results | Partial | 55–60% | ClinicalTrials.gov MVP / sponsor-name workflow | No persistence or change tracking | ClinicalTrials.gov indication/company tracking workflow |
| Source/webpage/API change detection | Early | 25–35% | Source health/failure diagnostics | No scheduler/alerts/persistence | Source-change detection design |
| MCP official/API-first source retrieval | Partial | 50–60% | MVP tool workflow | Multi-agency official API feasibility incomplete | Source API feasibility matrix |
| Open-source skill/plugin survey for Claude/Codex | Mostly missing | 10–20% | Not formalized | Need catalog/survey | Open-source plugin/skill survey |
| CMC readiness extension | Strong extension, not original core | 75% | PR #104–#112 | Needs real de-identified case later | Use current workflow without more CMC docs |

## New-chat opening prompt

Use the following prompt to continue in a new chat.

```text
請根據 GitHub repo `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`、`.ai/PROJECT_STATE.md`、以及 `PROJECT_STATE_CONTINUATION.md` 繼續。

請用繁體中文回覆，不要輸出日文。

目前對話已變長，請先不要新增程式、來源、MCP tool、scheduler、alerts、dashboard、persistence、HTTP/SSE、`.mcp.json`、GitHub automation、literature/patent/finance/news integration、company alias database、corporate-family mapping、product ownership inference，也不要新增 CMC weekly report template。

請先確認：

1. `main` 是否已包含 PR #112；
2. 是否有 open PR；
3. `.ai/PROJECT_STATE.md` 與 `PROJECT_STATE_CONTINUATION.md` 是否已記錄 PR #104–#112、PR #111 Prompt 6 revision、第二次 Claude Project stress test PASS、以及目前不需新增 `docs/cmc_management_weekly_report_template.md`；
4. 目前專案是否已被重新校準為 build-stage full-system planning，而不是只做 CMC weekly reporting；
5. 後續 code/test 工作是否應優先使用 Claude Code Web / Codex Web，而不是 Codespaces。

請把我最一開始的原始需求全部納入考量：

- GitHub/Codex 中建置專案與程式，最後移到 Claude Project 執行；
- 追蹤 FDA / EMA / TFDA / NMPA / PMDA 法規單位法條、公告或業界指引更新，標註日期與官方文件連結，日期區間 1 個月至 5 年；
- 可依不同生物藥品形式 / modality 分開檢索；
- 可依不同適應症追蹤不同廠商的臨床試驗最新進度與試驗結果，優先使用官方臨床 API；
- 若遇到網頁/API/parser 改版或 source failure，能偵測並支持後續修正，未來才評估通知機制；
- 優先官方 API，建立 MCP 抓取；
- 搜尋或整理可支援 Claude/Codex 的開源 skill/plugin/tool，至少對上述任一功能有幫助。

請先做 direction calibration，不要直接寫程式。

目前建議下一步是新增一個 docs/spec-only 文件：

`docs/original_requirements_traceability_matrix.md`

此文件要把原始需求逐項對照目前 repo 已完成內容、缺口、完成度、對應 PR/文件、是否屬 MVP v1、是否需要 source expansion approval、以及下一步建議。目的不是新增功能，而是防止專案繼續偏向 CMC weekly report 支線。

請先提出計畫與檔案內容大綱，等我確認後，再建立 branch / PR。
```
