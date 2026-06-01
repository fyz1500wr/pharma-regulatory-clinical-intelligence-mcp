# Claude Code Web MCP Smoke Test Note

## Purpose

This note records the Claude Code Web MCP client smoke test performed after the MCP stdio transport wrapper and Claude Code MCP configuration were added.

It is intended to prevent future confusion between:

- MCP transport or tool registration failure
- live-source connector failure
- Claude Code Web outbound network allowlist restrictions
- genuine no-result findings

This note is documentation-only and does not approve any source expansion.

---

## Related Changes

| PR | Change | Status |
|---|---|---|
| #39 | Added MCP stdio transport wrapper | Merged |
| #40 | Added project-scoped `.mcp.json` for Claude Code Web / Claude Code | Merged |

---

## MVP v1 Active Scope

The active MVP v1 live sources remain:

```text
FDA
TFDA
ClinicalTrials.gov
```

No EMA, NMPA, PMDA, WHO ICTRP, EU CTIS, literature, patent, finance, scheduler, alerting, persistence, or advanced reporting scope is added by this smoke test.

---

## Validation Summary

| Validation layer | Result | Notes |
|---|---|---|
| Codespaces MCP SDK client | PASS | MCP stdio server started, tools listed, and `check_source_health` was callable. |
| Claude Code Web project `.mcp.json` detection | PASS | `.mcp.json` was detected from the repository root. |
| Claude Code Web MCP server startup | PASS | `pharma-rci` MCP server connected. |
| Claude Code Web MCP tool exposure | PASS | 8 MVP v1 tools were exposed. |
| Claude Code Web `check_source_health` tool call | PASS | Tool invocation succeeded and returned structured JSON. |
| Claude Code Web `list_source_failures` tool call | PASS | Tool invocation succeeded and returned structured failure records. |
| Claude Code Web live-source network access | BLOCKED | External requests to MVP v1 live sources returned `403 Host not in allowlist`. |

---

## Tools Confirmed in Claude Code Web

The `pharma-rci` MCP server exposed the 8 MVP v1 tools:

```text
search_regulatory_updates
get_regulatory_document_detail
compare_regulatory_updates
search_clinical_trials_by_indication
compare_companies_by_indication
check_source_health
list_source_failures
generate_regulatory_digest
```

---

## Claude Code Web Live-Source Result

The Claude Code Web runtime was able to start the MCP server and call MCP tools, but live source calls were blocked by the runtime network policy.

Observed direct HTTP checks from Claude Code Web runtime:

| Target | URL | Result |
|---|---|---|
| FDA homepage | `https://www.fda.gov/` | `403 Host not in allowlist` |
| TFDA homepage | `https://www.fda.gov.tw/` | `403 Host not in allowlist` |
| ClinicalTrials.gov homepage | `https://clinicaltrials.gov/` | `403 Host not in allowlist` |
| ClinicalTrials.gov API v2 sample | `https://clinicaltrials.gov/api/v2/studies?pageSize=1` | `403 Host not in allowlist` |

The exact host requirements may evolve with connector implementation, but MVP v1 currently requires outbound access to at least:

```text
www.fda.gov
www.fda.gov.tw
clinicaltrials.gov
```

---

## Interpretation Rule

`403 Host not in allowlist` in Claude Code Web means the runtime environment blocked outbound access.

It must be interpreted as:

```text
source unavailable / degraded due to runtime egress policy
```

It must not be interpreted as:

```text
no matching regulatory records
no matching clinical trials
no relevant TFDA requirement
no relevant FDA update
no relevant ClinicalTrials.gov activity
```

---

## Failure Handling Confirmed

When the Claude Code Web runtime blocked live-source access, the MCP tools correctly surfaced the condition as source failures.

Observed `list_source_failures` result:

```text
open_failure_count: 2
high_failure_count: 2
critical_failure_count: 0
```

Observed open failures included:

```text
TFDA_DataAction-api_status-open
ClinicalTrialsGov_API-api_status-open
```

This confirms that Claude Code Web was able to invoke failure-handling tools and that the system preserved the distinction between source failure and genuine no-result findings.

---

## Operational Guidance

### Use Claude Code Web for

```text
MCP project configuration checks
MCP transport startup checks
MCP tool registration checks
MCP failure-handling behavior checks
Repository editing and documentation work
```

### Do not use Claude Code Web for live-source validation unless allowlist is configured

Claude Code Web should not be treated as the reliable live-source validation runtime while the relevant hosts are blocked by the environment allowlist.

Until the allowlist is updated, use Codespaces or another approved local/dev runtime for live-source validation.

---

## Required Caveat for Downstream Outputs

Any report, digest, comparison, tracker, or management summary produced while Claude Code Web live sources are blocked must disclose:

```text
Claude Code Web live-source access was blocked by egress allowlist.
Outputs are partial and limited by source failure.
No-result interpretations are not valid until sources are reachable and rechecked.
```

---

## Recommended Follow-Up

If Claude Code Web is intended to perform live-source validation, configure the environment allowlist for MVP v1 source hosts and rerun:

```text
check_source_health
list_source_failures
search_regulatory_updates
search_clinical_trials_by_indication
```

If allowlist configuration is not available, keep live-source validation in Codespaces or another controlled runtime and use Claude Code Web only for MCP transport, tool registration, and failure-handling checks.
