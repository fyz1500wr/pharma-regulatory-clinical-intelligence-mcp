# Product-Value / Usability Calibration Runbook

## Purpose

This runbook defines how to check whether the current MVP v1 tools produce outputs that are usable by PM, RA, clinical, or management reviewers as working intelligence drafts.

The calibration question is:

```text
Can the current FDA + TFDA + ClinicalTrials.gov MVP output be read safely without confusing source limitations with true zero results?
```

This is a usability review workflow. It is not a source expansion approval.

---

## MVP scope reminder

Use only the current MVP v1 scope:

- FDA
- TFDA
- ClinicalTrials.gov
- existing MCP tools

Do not add new sources, MCP tools, dashboards, schedulers, alerts, persistence, HTTP/SSE transport, `.mcp.json`, or external intelligence integrations during this calibration.

---

## Recommended scenario

Use this controlled scenario unless another scenario is explicitly approved:

```text
Indication: gastric cancer
Companies: AstraZeneca, Merck
Regulatory sources: FDA, TFDA
Clinical registry: ClinicalTrials.gov
Digest type: combined
Digest date range: 1y
Company comparison date range: 3y
Limit/page size: 5
```

This scenario checks whether the MVP can show source health, clinical trial activity, company comparison, and source limitations in a way that a reviewer can understand.

---

## Pre-checks

Run from a clean checkout:

```bash
git checkout main
git pull --ff-only origin main
git status --short
python -m pip install -e ".[dev]"
pytest -q
```

---

## Source-health-first rule

Before interpreting any digest, run source health checks:

```bash
PYTHONPATH=. python - <<'PY'
from pprint import pprint
from src.mcp_server.tools_healthcheck import check_source_health, list_source_failures

print("check_source_health")
pprint(check_source_health())

print("list_source_failures")
pprint(list_source_failures())
PY
```

Key rule:

```text
SOURCE_UNAVAILABLE, BLOCKED_SOURCE, proxy failure, or runtime access failure must not be interpreted as no data.
```

---

## Scenario commands

Run the digest:

```bash
PYTHONPATH=. python - <<'PY'
from pprint import pprint
from src.mcp_server.tools_digest import generate_regulatory_digest

result = generate_regulatory_digest(
    digest_type="combined",
    agencies=["FDA", "TFDA"],
    registries=["ClinicalTrials.gov"],
    indications=["gastric cancer"],
    companies=["AstraZeneca", "Merck"],
    topics=["submission"],
    date_range="1y",
    limit=5,
    include_impact_matrix=True,
    include_source_health_summary=True,
)
pprint(result)
PY
```

Run the company comparison:

```bash
PYTHONPATH=. python - <<'PY'
from pprint import pprint
from src.mcp_server.tools_clinical_trials import compare_companies_by_indication

result = compare_companies_by_indication(
    indication="gastric cancer",
    companies=["AstraZeneca", "Merck"],
    registries=["ClinicalTrials.gov"],
    date_range="3y",
    include_completed_trials=True,
    include_results=True,
    page_size=5,
)
pprint(result)
PY
```

---

## Required interpretation rules

### Source unavailable

Use this interpretation when a source returns `SOURCE_UNAVAILABLE`, `BLOCKED_SOURCE`, proxy failure, or runtime access failure.

Allowed statement:

```text
The source was unavailable in this run; source-dependent findings are not evaluable.
```

Avoid:

```text
There were no records.
```

### No matching records

Use this interpretation only when the source was reachable and the tool explicitly returns `NO_MATCHING_RECORDS`.

Allowed statement:

```text
No matching records were returned under the selected MVP query parameters.
```

Avoid:

```text
There is no activity or no requirement.
```

### Not evaluable company activity

Use this interpretation when company comparison returns `activity_evaluable = false`.

Allowed statement:

```text
Company activity is not evaluable for this run because the source lookup failed.
```

Avoid:

```text
The company has zero trial activity.
```

### Evaluable zero records

Use this interpretation when source access succeeded and `activity_evaluable = true` with `trial_count = 0`.

Allowed statement:

```text
Zero matching records were returned under this query. This remains limited by MVP query scope and matching rules.
```

---

## Usability status definitions

| Status | Meaning |
|---|---|
| PASS | Output is readable, source-aware, and usable as a working-intelligence draft after manual verification. |
| PARTIAL | Output is understandable but has source limitations, sparse records, broad matching, or manual review gaps. |
| BLOCKED_SOURCE | Runtime or source access prevents content-bearing assessment. |
| FAIL_OUTPUT | Output hides source errors, presents unavailable data as zero, or invites over-interpretation. |
| NOT_RUN | Scenario was not executed. |

---

## Review checklist

Before using the output in a PM/RA summary, confirm:

- [ ] Source health was checked first.
- [ ] Source errors remain visible.
- [ ] `SOURCE_UNAVAILABLE` is not treated as zero records.
- [ ] `NO_MATCHING_RECORDS` is used only when source access succeeded.
- [ ] `activity_evaluable = false` is described as not evaluable, not zero activity.
- [ ] Trial counts are not used to rank companies.
- [ ] Highest phase is not interpreted as approval probability.
- [ ] ClinicalTrials.gov sponsor matching limitations are stated.
- [ ] Important records are manually verified through official URLs.

---

## Calibration record template

```text
Scenario:
Runtime:
Source-health status:
Digest status:
Company comparison status:
Overall usability status:
Main limitation:
Recommended next action:
```

Recommended next actions should stay small: documentation update, usage example improvement, output caveat wording, regression test for misleading output, or rerun in an approved runtime.
