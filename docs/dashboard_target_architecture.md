# Dashboard-Oriented Target Architecture Contract

Status: Draft target architecture / docs-spec only  
Last updated: 2026-06-10

## 1. Purpose

This document re-anchors the project around the user's original target outcome: a dashboard-oriented regulatory and clinical intelligence system built in GitHub/Codex, with controlled execution and interpretation through Claude Project and MCP tools.

The target user experience is not only a collection of MCP tools or Markdown workflows. The intended end product is a recurring intelligence dashboard plus digest workflow that can show:

1. Regulatory and guidance updates from official or high-reliability sources.
2. Update dates, document dates, and direct official document links.
3. Date-window filtering from 1 month to 5 years.
4. Biologic or therapeutic modality filtering.
5. Clinical trial progress and results by indication and sponsor/company.
6. Source-health status and source-change warnings when webpages, APIs, or parsers change.

This document is an architecture contract only. It does not implement a dashboard, workflow schedule, connector, MCP tool, parser, database, GitHub Actions workflow, notification, or deployment.

## 2. Core Architecture Principle

The project should follow a dashboard-first, source-expansion-later approach.

```text
Official source / API / RSS / official page
  -> source connector or MCP-accessible retrieval layer
  -> normalization and source-health diagnostics
  -> canonical dashboard data schemas
  -> static dashboard artifacts and digest summaries
  -> Claude Project interpretation and PM/RA decision support
```

The dashboard contract should be defined before adding additional runtime source connectors. This prevents uncontrolled source-by-source implementation and ensures that every future source contributes to the same dashboard data model.

## 3. System Component Roles

| Component | Role | Should Do | Should Not Do |
|---|---|---|---|
| GitHub repository | System-of-build and versioned architecture | Store code, schemas, docs, tests, dashboard artifacts, and source profiles | Store confidential or official submission records |
| Codex / code assistant | Construction and code-editing environment | Create connectors, tests, schemas, documentation, dashboard rendering logic after approval | Act as long-running scheduler |
| GitHub Actions | Future scheduled execution layer | Run approved ingestion, source-health checks, validation, and dashboard artifact builds | Be added before an explicit runtime/scheduler approval |
| MCP server | Controlled query interface | Expose approved tools to Claude and local clients | Bypass source constraints or scrape restricted sources |
| Claude Project | Analysis and interpretation layer | Read dashboard summaries, compare updates, draft source-aware digests, and support PM/RA review | Serve as the scheduled ingestion runtime |
| GitHub Pages or workflow artifacts | Future display/distribution layer | Display static dashboard output or downloadable artifacts after approval | Store sensitive or non-public data |

## 4. Recommended Dashboard Tabs

### 4.1 Regulatory / Guidance Updates

Purpose: show regulatory, legal, and guidance updates by agency/source, date window, topic, and modality.

Candidate sources:

```text
FDA
EMA
TFDA
NMPA / CDE
PMDA
ICH
```

Important classification distinction:

- FDA, EMA, TFDA, NMPA/CDE, and PMDA are agency or regulator-linked source candidates.
- ICH is a global harmonisation guidance source, not a drug-review agency and not a clinical trial registry.

Minimum display fields:

```text
source_name
source_category
region
title
document_type
published_date
updated_date
effective_date_or_adoption_date
official_url
attachment_url
summary_or_snippet
topic_tags
modality_tags
date_window_bucket
source_reliability_flag
source_health_status
```

Supported dashboard date windows:

```text
1 month
3 months
6 months
1 year
3 years
5 years
```

### 4.2 Biologic / Therapeutic Modality View

Purpose: allow filtering regulatory and guidance updates by product modality.

Initial modality filters may include:

```text
small molecule
peptide
oligonucleotide / RNA-based product
recombinant protein
monoclonal antibody
antibody-drug conjugate
vaccine
cell therapy
gene therapy
radiopharmaceutical
biosimilar
combination product
other therapeutic modality
```

Classification approach:

1. Use rule-based tags first.
2. Allow AI-assisted classification later only after an explicit approval.
3. Preserve source evidence and avoid unsupported product ownership inference.
4. Allow human review and override of modality labels.

### 4.3 Clinical Trial Tracker

Purpose: track trial progress and results by indication, sponsor/company, intervention, phase, status, and official registry link.

Approved MVP source:

```text
ClinicalTrials.gov API v2
```

Future registry expansion candidates require separate feasibility and approval:

```text
EU CTIS
WHO ICTRP
Japan registry sources
China registry sources
other official registries
```

Minimum display fields:

```text
registry_id
registry_name
trial_title
condition_or_indication
sponsor
collaborators
intervention
phase
trial_status
start_date
primary_completion_date
completion_date
last_update_posted
results_available
results_first_posted
registry_url
results_url
source_health_status
```

The tracker must not infer clinical success, approval probability, commercial strength, company superiority, or ownership relationships without explicit evidence and a separately approved model.

### 4.4 Source Health / Change Monitor

Purpose: detect source access failures, webpage/API changes, parser issues, and abnormal record-count deltas before relying on dashboard outputs.

Minimum display fields:

```text
source_name
source_type
last_success_at
last_failure_at
status
failure_type
http_status
parser_error_message
schema_changed_flag
html_selector_changed_flag
record_count_delta
recommended_action
```

Interpretation rules:

- Source-health `pass` does not prove complete data coverage.
- Connector unavailable must not be interpreted as zero results.
- FDA abuse-detection, apologies, egress blocks, and parser failures are source-access limitations, not evidence that no records exist.
- Human verification remains required before regulatory or management-facing use.

## 5. GitHub Actions Execution Concept

GitHub Actions is the preferred future scheduled execution layer if Claude/Codex cannot or should not run ingestion directly.

Future approved workflow concept:

```text
scheduled workflow
  -> run approved source connectors or API clients
  -> write normalized JSON snapshots
  -> run source-health diagnostics
  -> build static dashboard HTML/Markdown artifacts
  -> upload artifacts or publish to an approved branch/site
  -> Claude Project reads digest/dashboard summary for interpretation
```

This document does not add any workflow file. Any GitHub Actions schedule, artifact publication, branch commit, or GitHub Pages deployment requires a later explicit approval.

## 6. Canonical Data Contract Families

Future dashboard implementation should define these schema families before runtime dashboard rendering:

```text
RegulatoryGuidanceUpdate
ClinicalTrialUpdate
SourceHealthEvent
DashboardDigestSummary
```

Recommended next schema contract fields:

- stable record ID
- source name and source category
- official URL and attachment URL
- date fields and date-window bucket
- topic tags
- modality tags
- indication tags where applicable
- source-health status
- evidence/caveat fields
- human-review flag

## 7. Claude Project Consumption Model

Claude Project should consume the dashboard through controlled artifacts, not by directly scraping raw source sites during normal operation.

Preferred Claude inputs:

```text
weekly_dashboard_summary.md
normalized_dashboard_snapshot.json
source_health_summary.md
regulatory_guidance_updates.csv or json
clinical_trial_updates.csv or json
```

Claude Project should use those artifacts to:

- summarize weekly or monthly changes;
- compare agencies or guidance sources;
- identify high-impact regulatory/guidance updates;
- highlight clinical trial status or result changes by indication;
- flag source-health caveats;
- prepare PM/RA digest memos with official links and caveats.

## 8. Phased Implementation Roadmap

### Phase A — Architecture Contract

Current proposed phase. Define dashboard target architecture, display tabs, source categories, execution boundaries, and non-goals.

### Phase B — Canonical Dashboard Data Schema Contract

Define `RegulatoryGuidanceUpdate`, `ClinicalTrialUpdate`, `SourceHealthEvent`, and `DashboardDigestSummary` schemas without implementing ingestion or rendering.

### Phase C — Static Dashboard Dry-Run Design

Use mock or existing fixture data to define layout, filters, and output expectations. No live scheduler or new source connector.

### Phase D — MVP Source Dashboard Export

Use approved MVP sources only: FDA, TFDA, and ClinicalTrials.gov. Produce dashboard-compatible artifacts without adding EMA/NMPA/PMDA/ICH runtime connectors.

### Phase E — Source-Specific Expansion Profiles

Only after explicit approval, add source profiles such as:

```text
ICH guidance-source profile
EMA agency-source profile
PMDA agency-source profile
NMPA/CDE agency-source profile
```

### Phase F — Approved Scheduled Dashboard Build

Only after explicit approval, add GitHub Actions workflow and artifact/publication rules.

## 9. Activation Gates Before Runtime Dashboard Work

Do not implement dashboard runtime, GitHub Actions scheduling, publication, or new source connectors until all of the following are true:

1. Dashboard architecture contract is accepted.
2. Canonical dashboard data schemas are accepted.
3. Source-health event model is accepted.
4. MVP source dashboard export scope is approved.
5. Storage/persistence/publication boundary is approved.
6. Human-review and confidentiality rules are accepted.

## 10. Explicit Non-Goals For This Contract

This document does not add or approve:

- runtime dashboard renderer;
- GitHub Actions workflow;
- scheduled ingestion;
- alerts or notifications;
- GitHub Pages publication;
- database or persistence layer;
- new MCP tool;
- `.mcp.json` change;
- EMA, NMPA/CDE, PMDA, ICH, EU CTIS, WHO ICTRP, literature, patent, finance, or news connector;
- company alias database;
- corporate-family mapping;
- product ownership inference;
- clinical success scoring;
- approval probability scoring;
- management decision automation;
- CMC weekly management report template;
- confidential or non-public record storage.

## 11. Recommended Next Step

After this contract is reviewed, the next controlled PR should be:

```text
Add canonical dashboard data schema contract
```

That next PR should remain docs/spec-only and should not implement runtime ingestion or dashboard rendering.
