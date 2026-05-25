# Pharmaceutical Regulatory & Clinical Intelligence MCP

This repository is for building a **Pharmaceutical Regulatory and Clinical Intelligence System** in GitHub/Codex, with final execution through Claude using MCP tools.

The system is intended to track regulatory updates and clinical trial developments from official or high-reliability public sources, normalize the data, classify it by biologic product type and indication, and make the results available for Claude-based analysis and reporting.

---

## Current Build Phase

**Current phase:** MVP v1

MVP v1 focuses on proving the end-to-end workflow:

```text
Official source
  → Connector
  → Normalization
  → Classification
  → Storage / Index
  → MCP tools
  → Claude analysis and reports
```

---

## MVP v1 Scope

MVP v1 should focus only on the minimum working system.

Included in MVP v1:

1. FDA regulatory and open data sources
2. TFDA regulatory and open data sources
3. ClinicalTrials.gov API v2
4. Basic biologic product type classification
5. Basic indication and company tracking
6. Basic regulatory update digest
7. Basic source health check
8. Basic MCP tools for regulatory and clinical trial search

The initial build target is:

```text
FDA + TFDA + ClinicalTrials.gov
```

EMA, NMPA, PMDA, and advanced monitoring should be added only after MVP v1 works end to end.

---

## What This Repository Does

This repository is designed to:

- Track regulatory updates from FDA, EMA, TFDA, NMPA, and PMDA
- Record publication dates, update dates, official URLs, and attachment links
- Classify regulatory updates by biologic product type and regulatory topic
- Track clinical trials by indication, sponsor/company, phase, status, and results availability
- Use official APIs, RSS feeds, open data portals, and official source pages where available
- Detect source failures, webpage structure changes, and parser issues
- Expose standardized MCP tools for Claude-based querying and reporting

---

## What This Repository Does Not Do

This repository is not intended to:

- Replace professional regulatory, clinical, legal, or medical judgment
- Make final regulatory filing decisions
- Predict approval outcomes without evidence
- Use non-official sources as primary regulatory evidence
- Circumvent website access controls
- Collect confidential or non-public company data
- Automatically submit anything to regulatory authorities

---

## Core Documents

The governing document for this project is:

```text
PROJECT_INSTRUCTION.md
```

`PROJECT_INSTRUCTION.md` defines the project scope, source priority rules, implementation phases, MCP design principles, and non-expansion rules.

Additional core documents to be created next:

```text
docs/source_priority_matrix.md
docs/biologics_taxonomy.md
docs/mcp_tool_contract.md
docs/data_dictionary.md
workflows/regulatory_clinical_intelligence_workflow.md
CLAUDE.md
AGENTS.md
```

---

## Development Order

Recommended setup order:

1. Finalize `PROJECT_INSTRUCTION.md`
2. Create this thin `README.md`
3. Create `docs/source_priority_matrix.md`
4. Create `docs/biologics_taxonomy.md`
5. Create `docs/mcp_tool_contract.md`
6. Create `docs/data_dictionary.md`
7. Create `workflows/regulatory_clinical_intelligence_workflow.md`
8. Create `CLAUDE.md`
9. Create `AGENTS.md`
10. Start MVP v1 implementation

The README may be revised later after the source matrix, taxonomy, MCP contract, workflow, Claude instructions, and agent instructions are finalized.

Any README revision should be reviewed and approved before changes are applied.

---

## Claude / MCP Execution Concept

Claude should not directly scrape raw regulatory or clinical trial websites during normal operation.

The intended execution model is:

```text
GitHub / Codex builds the system
GitHub Actions runs scheduled ingestion and source checks
MCP exposes controlled tools
Claude queries MCP tools
Claude generates summaries, comparisons, and reports
```

Claude should use MCP tools to perform tasks such as:

- Search regulatory updates
- Retrieve regulatory document details
- Compare agencies
- Search clinical trials by indication
- Compare companies by indication
- Check source health status
- Generate regulatory or clinical intelligence digests

---

## Non-Expansion Reminder

This repository should stay controlled and phase-based.

Do not add new agencies, tools, workflows, or markdown files unless they clearly support the current phase or have been explicitly approved.

When uncertain, keep the implementation smaller and document the limitation clearly.
