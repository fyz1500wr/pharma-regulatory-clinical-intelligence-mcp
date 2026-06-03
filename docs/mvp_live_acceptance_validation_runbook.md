# MVP Live Acceptance Validation Runbook

This runbook defines how to validate whether the current MVP can be used against live sources for basic regulatory and clinical trial intelligence tasks.

It is a validation workflow, not a feature expansion.

## Purpose

The goal is to answer one practical question:

> Can the current MVP tools produce usable results from FDA, TFDA, and ClinicalTrials.gov in a real working environment?

This runbook should be used after offline smoke tests and metadata consistency checks have already passed.

## Approved source scope

The live acceptance validation remains limited to the current MVP sources:

- FDA
- TFDA
- ClinicalTrials.gov

Do not add EMA, NMPA, PMDA, WHO ICTRP, EU CTIS, literature, patent, finance, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, `.mcp.json` changes, GitHub issue automation, or new MCP tools during this validation.

## Prerequisites

Run from a clean repository checkout:

```bash
git checkout main
git pull --ff-only origin main
git status --short
```

Install development dependencies if needed:

```bash
python -m pip install -e ".[dev]"
```

Confirm local regression tests pass before live validation:

```bash
pytest -q
```

## Acceptance status definitions

Use these statuses for each check:

| Status | Meaning |
|---|---|
| PASS | Tool runs and returns usable structured output for the intended MVP use. |
| PARTIAL | Tool runs but output has limited metadata, sparse records, source caveats, or manual review needs. |
| BLOCKED_SOURCE | Tool code runs, but the live source, network, egress policy, or API availability prevents validation. |
| FAIL_CODE | Tool fails due to project code, parser, schema, parameter handling, or normalization defects. |
| NOT_RUN | Check was not executed. |

Important: `BLOCKED_SOURCE` is not the same as zero matching records.

## Step 1 — Confirm tool registry loads

```bash
PYTHONPATH=. python - <<'PY'
from src.mcp_server.server import TOOL_REGISTRY

print(sorted(TOOL_REGISTRY))
assert "search_regulatory_updates" in TOOL_REGISTRY
assert "get_regulatory_document_detail" in TOOL_REGISTRY
assert "compare_regulatory_updates" in TOOL_REGISTRY
assert "search_clinical_trials_by_indication" in TOOL_REGISTRY
assert "compare_companies_by_indication" in TOOL_REGISTRY
assert "check_source_health" in TOOL_REGISTRY
assert "list_source_failures" in TOOL_REGISTRY
assert "generate_regulatory_digest" in TOOL_REGISTRY
PY
```

Expected result: PASS if all eight MVP tools are present.

## Step 2 — Check live source health

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

Record whether FDA, TFDA, and ClinicalTrials.gov are reachable. If one source is blocked, continue validating the other sources and classify the blocked source as `BLOCKED_SOURCE`.

## Step 3 — FDA regulatory search

```bash
PYTHONPATH=. python - <<'PY'
from pprint import pprint
from src.mcp_server.tools_regulatory import search_regulatory_updates

result = search_regulatory_updates(
    query="oncology guidance",
    agencies=["FDA"],
    product_modality="antibody",
    date_range="1y",
    limit=5,
)
pprint(result)
PY
```

Assess:

- Does the tool return structured output or a structured error?
- Are agency, title, date, official URL, product modality, topic, and query metadata present when records exist?
- If no records are returned, is the reason distinguishable from source failure?

## Step 4 — TFDA regulatory search

```bash
PYTHONPATH=. python - <<'PY'
from pprint import pprint
from src.mcp_server.tools_regulatory import search_regulatory_updates

result = search_regulatory_updates(
    query="藥品 查驗登記",
    agencies=["TFDA"],
    date_range="1y",
    limit=5,
)
pprint(result)
PY
```

Assess:

- Does the tool return structured output or a structured error?
- Are agency, title, date, official URL, product modality, topic, and query metadata present when records exist?
- If TFDA is blocked or inaccessible, record `BLOCKED_SOURCE` rather than interpreting the result as no regulatory updates.

## Step 5 — cross-agency regulatory comparison

```bash
PYTHONPATH=. python - <<'PY'
from pprint import pprint
from src.mcp_server.tools_regulatory import compare_regulatory_updates

result = compare_regulatory_updates(
    query="oncology",
    agencies=["FDA", "TFDA"],
    date_range="1y",
    limit=5,
)
pprint(result)
PY
```

Assess whether the comparison output is usable for preliminary analysis and whether source limitations remain visible.

## Step 6 — ClinicalTrials.gov indication search

```bash
PYTHONPATH=. python - <<'PY'
from pprint import pprint
from src.mcp_server.tools_clinical_trials import search_clinical_trials_by_indication

result = search_clinical_trials_by_indication(
    "gastric cancer",
    page_size=5,
)
pprint(result)
PY
```

Assess:

- Does the tool return structured trial records?
- Are trial ID, registry, official URL, title, sponsor, indication, intervention, phase, status, last update date, result availability, and query metadata present?
- Is ClinicalTrials.gov source failure distinguishable from zero matching trials?

## Step 7 — Company-by-indication comparison

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

Assess:

- Does the output show `company_comparison`, `landscape_summary`, and `query_metadata`?
- Are data gaps and non-superiority interpretation visible?
- Does the tool avoid implying clinical superiority, approval probability, or commercial strength?

## Step 8 — Regulatory digest

```bash
PYTHONPATH=. python - <<'PY'
from pprint import pprint
from src.mcp_server.tools_digest import generate_regulatory_digest

result = generate_regulatory_digest(
    digest_type="combined",
    agencies=["TFDA"],
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

Assess whether the digest clearly remains a working intelligence draft and whether source limitations are visible.

Interpret the digest result using these rules:

- If FDA is currently classified as `BLOCKED_SOURCE`, do not include FDA in the final source-limited digest check.
- `BLOCKED_SOURCE` is a source-health limitation, not a zero-result regulatory finding.
- The digest must remain a working intelligence draft, not a final regulatory, clinical, legal, medical, or competitive assessment.
- If a requested source is unavailable, the source limitation should remain visible and should not be silently converted into zero results.

## Step 9 — Record results

Use `docs/mvp_live_acceptance_validation_results_template.md` to record:

- Environment
- Commands run
- Source health status
- Tool-level result status
- Evidence snippets
- Blockers
- Follow-up classification
- Final MVP live acceptance conclusion

## Final acceptance decision

Use one of these final decisions:

| Decision | Meaning |
|---|---|
| ACCEPT_FOR_CONTROLLED_MVP_USE | Core MVP tools work with live sources and limitations are visible. |
| ACCEPT_WITH_SOURCE_LIMITATIONS | Core tool logic works, but one or more live sources are blocked or unstable. |
| DO_NOT_ACCEPT_YET | Code-level or output-contract failures prevent controlled MVP use. |

## Stop conditions

Stop and open a focused follow-up issue or PR if any of the following occurs:

- A live source failure is incorrectly presented as zero results.
- A tool returns unstructured exceptions instead of structured output or structured errors.
- Clinical trial comparison implies superiority, approval probability, or commercial strength.
- A fix would require adding new sources, new tools, persistence, scheduler, alerts, dashboard, or transport changes.

## Important interpretation

This live acceptance validation does not certify regulatory completeness, clinical completeness, legal compliance, medical correctness, CMC adequacy, or business decision readiness. It only determines whether the current MVP tools can be used as a controlled working-intelligence aid within the approved MVP source scope.
