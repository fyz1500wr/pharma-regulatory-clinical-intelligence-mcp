# Source Failure Diagnostic Runbook

## 1. Purpose-first rule

This runbook exists to keep the project aligned with its original purpose: to track official regulatory updates and clinical trial developments, preserve dates and official source links, classify records by product modality or indication, and expose controlled MCP tools for Claude-based intelligence reporting.

Source failure handling is not a side feature. It protects the reliability of the core intelligence workflow. A failed connector, blocked runtime, changed webpage, or empty result must not be confused with evidence that no regulatory update, no clinical trial, or no company activity exists.

All future code changes should follow this principle:

```text
Build code to answer the original intelligence questions safely.
Do not optimize only for passing tests or producing output.
Always preserve official-source traceability, date meaning, source health context, and conservative interpretation.
```

This means every connector, parser, health check, MCP tool, and report generator should support the following project goals:

1. Track official regulatory laws, guidance, notices, and industry updates by date range.
2. Support product-modality-based retrieval and classification.
3. Track indication-, company-, and trial-status-based clinical trial activity from official registry data.
4. Detect and triage source failures, webpage changes, API changes, and parser breakage.
5. Prefer official APIs, RSS feeds, open data, and official source pages over uncontrolled scraping.

---

## 2. When to use this runbook

Use this runbook whenever any MCP tool returns:

- `overall_status = degraded`
- `overall_status = unavailable`
- one or more source health items with `status = failed`
- an empty regulatory or clinical trial result set where source availability is uncertain
- a source failure record from `list_source_failures`
- a runtime message such as `Host not in allowlist`
- an API status error, schema mismatch, parser failure, or suspiciously low result count

Use it before making any of the following statements:

- no regulatory updates were found
- no clinical trials were found
- no company activity was found
- a source is offline
- a connector is broken
- a webpage was redesigned
- the code needs to be fixed

---

## 3. Required diagnostic sequence

### Step 1: Check source health first

Run:

```text
check_source_health
```

Interpretation rule:

```text
Source health pass means the connector execution path responded.
It does not prove complete source coverage, perfect search recall, or complete official data capture.
```

If a source fails, do not treat downstream search results as complete.

### Step 2: List source failures

Run:

```text
list_source_failures
```

Use this tool to classify current failures by source, severity, failure type, suspected cause, suggested fix, and known limitation.

Important rule:

```text
list_source_failures is a current snapshot.
It is not a historical incident log unless a later phase adds persistence.
```

### Step 3: Separate runtime failure from source failure

If the failure type is `egress_policy`, the runtime could not reach the source because of network or allowlist restrictions.

Typical examples:

```text
403 Host not in allowlist
not in allowlist
egress allowlist
runtime network policy
network allowlist
```

This means:

```text
The current runtime cannot access the source.
It does not prove that the official source is offline.
It does not prove that there are no regulatory updates.
It does not prove that there are no clinical trials.
It does not prove that the connector code is wrong.
```

### Step 4: Confirm whether the issue is a no-result case

Only interpret a search result as `no matching records` when:

1. the relevant source health check is not failed,
2. the query parameters are valid,
3. the date range is valid,
4. the source or connector is within the active project phase,
5. known limitations do not invalidate the search, and
6. the MCP tool explicitly returns a no-result state rather than a source failure.

---

## 4. Failure type interpretation

| Failure type | Meaning | What to do | What not to conclude |
|---|---|---|---|
| `egress_policy` | Runtime/network allowlist blocked access to the source. | Add the source host to the runtime allowlist, switch to Codespaces/local, or rerun in an approved runtime. | Do not conclude no updates, no trials, or source offline. |
| `api_status` | The API or official endpoint did not respond successfully, or the connector could not complete an availability check. | Check official endpoint status, connector request logic, response code, and retry behavior. | Do not conclude no matching records. |
| `schema_drift` / future | The official API or data structure changed. | Update parsing/normalization after confirming official response structure. | Do not treat old parser output as complete. |
| `selector_break` / future | HTML structure changed and parser selectors no longer match. | Review webpage structure and update selector tests. | Do not assume the webpage has no records. |
| `empty_result_anomaly` / future | Result volume is unexpectedly zero or unusually low. | Compare against recent known records and broaden query/date range. | Do not conclude no activity without confirmation. |
| `unknown` | Failure type is not yet classified. | Preserve error details and investigate. | Do not hide or normalize away the uncertainty. |

---

## 5. Diagnostic decision tree

```text
A tool returns empty or incomplete results
  ↓
Run check_source_health
  ↓
Any failed source?
  ├─ No
  │   └─ Review query, date range, product modality, indication, sponsor name, and known limitations.
  │
  └─ Yes
      ↓
    Run list_source_failures
      ↓
    failure_type = egress_policy?
      ├─ Yes
      │   └─ Treat as runtime/network policy issue. Do not interpret as no data.
      │
      └─ No
          ↓
        failure_type = api_status or parser/schema failure?
          ├─ Yes
          │   └─ Investigate source endpoint, connector code, parser assumptions, or official API changes.
          │
          └─ Unknown
              └─ Preserve evidence and escalate for manual review.
```

---

## 6. Claude Code Web versus Codespaces/local

Claude Code Web may run through an environment with restricted external network access. A source that works in Codespaces or local execution may fail in Claude Code Web with an allowlist error.

When this happens:

1. classify the failure as `egress_policy`,
2. preserve the raw message such as `Host not in allowlist`,
3. report it as a runtime access limitation,
4. rerun the same source check in Codespaces/local if live validation is needed,
5. do not change connector code unless Codespaces/local also fails or the official response has changed.

For MVP v1, the key live-source hosts are:

```text
www.fda.gov
www.fda.gov.tw
clinicaltrials.gov
```

---

## 7. When to modify connector code

Modify connector code only when evidence indicates a connector or source-structure problem, such as:

- the source is reachable from an approved runtime but the connector fails,
- the official API returns a changed schema,
- required fields are missing or renamed,
- HTML selectors no longer match official pages,
- attachment extraction fails after source access is confirmed,
- date parsing fails on official date strings,
- source health passes but normalized records are malformed,
- tests demonstrate a reproducible connector defect.

Do not modify connector code merely because:

- Claude Code Web cannot access the host,
- an allowlist blocks the request,
- a query returns no records while source health is unknown,
- a company or indication name is too narrow,
- a future-phase source is not yet active.

---

## 8. No-result interpretation rules

A no-result interpretation is allowed only after source failure is ruled out.

For regulatory update tracking:

```text
No result means no matching records were found under the selected source, date range, topic, and modality filters.
It does not mean no regulatory activity exists globally.
```

For clinical trial tracking:

```text
No result means no matching official registry records were found under the selected indication, sponsor, status, phase, and date filters.
It does not mean the company has no pipeline, no trial activity, no results, or no clinical development strategy.
```

For company comparison:

```text
Sponsor-name matching is not corporate-family resolution.
More trials does not mean better company.
Phase 3 activity does not imply approval probability.
Trial activity does not imply clinical success.
```

---

## 9. Code-writing checklist for future agents

Before writing or changing code, agents should ask:

1. Does this change support official regulatory or clinical intelligence tracking?
2. Does it preserve official source URL, date fields, and source traceability?
3. Does it distinguish source failure from no matching records?
4. Does it avoid unsupported conclusions about regulatory activity, clinical success, or company superiority?
5. Does it keep MVP v1 source scope unchanged unless expansion was explicitly approved?
6. Does it add or update tests for failure paths, not only happy paths?
7. Does it keep MCP tool names and output contracts stable?
8. Does it document known limitations clearly enough for Claude to report safely?

If the answer is no or uncertain, keep the implementation smaller and document the limitation.

---

## 10. Recommended wording for reports

When `egress_policy` occurs:

```text
The source could not be reached from the current runtime due to a network or allowlist restriction. This is not evidence that the official source is offline, and it must not be interpreted as no matching regulatory updates or no matching clinical trials.
```

When `api_status` occurs:

```text
The source health check did not complete successfully. Downstream search results from this source may be incomplete until source availability or connector behavior is confirmed.
```

When no records are found after healthy source checks:

```text
No matching records were found for the specified source, date range, and filters. This should be interpreted only within the stated query scope and known limitations.
```

---

## 11. Phase boundary

This runbook does not approve new sources, new tools, scheduling, alerting, persistence, dashboarding, or automatic GitHub Issue creation.

It supports MVP v1 by making source-failure interpretation safer for the active scope:

```text
FDA + TFDA + ClinicalTrials.gov
```

EMA, NMPA, PMDA, WHO ICTRP, EU CTIS, literature, patent, finance, advanced monitoring, and automated alerting remain later-phase work unless separately approved.
