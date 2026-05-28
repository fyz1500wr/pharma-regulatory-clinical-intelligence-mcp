# Pharmaceutical Regulatory & Clinical Intelligence MCP

This repository is for building a **Pharmaceutical Regulatory and Clinical Intelligence System** in GitHub/Codex, with final execution through Claude using MCP tools.

The system is intended to track regulatory updates and clinical trial developments from official or high-reliability public sources, normalize the data, classify it by product modality and indication, and make the results available for Claude-based analysis and reporting.

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

4. Basic product modality classification
5. Basic indication and company tracking
6. Basic regulatory update digest
7. Basic source health check
8. Basic MCP tools for regulatory and clinical trial search

Product modality coverage includes small molecules, peptides, oligonucleotide/RNA-based products, antibodies, ADCs, vaccines, cell therapies, gene therapies, radiopharmaceuticals, combination products, and other therapeutic modalities.
The initial build target is:

```text
FDA + TFDA + ClinicalTrials.gov
```

EMA, NMPA, PMDA, and advanced monitoring should be considered only through a separate approved post-MVP source expansion decision.

---

## What This Repository Does

This repository is designed to:

- Track regulatory updates from official or high-reliability regulatory sources within the approved project phase
- Record publication dates, update dates, official URLs, and attachment links
- Classify regulatory updates by product modality and regulatory topic
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

Core and supporting documents include:

```text
CLAUDE.md
AGENTS.md
docs/source_priority_matrix.md
docs/product_modality_taxonomy.md
docs/mcp_tool_contract.md
docs/data_dictionary.md
workflows/regulatory_clinical_intelligence_workflow.md
```

---

## Development Order

Recommended setup order:

1. Finalize `PROJECT_INSTRUCTION.md`
2. Create this thin `README.md`
3. Create `docs/source_priority_matrix.md`
4. Create `docs/product_modality_taxonomy.md`
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

## MVP v1 MCP Tool Status

This status table is intended to keep MVP v1 implementation focused and prevent uncontrolled scope expansion.

| MCP Tool | MVP v1 Status | Notes |
|---|---|---|
| `search_regulatory_updates` | Implemented | FDA and TFDA regulatory update search. |
| `get_regulatory_document_detail` | Implemented, metadata-backed | Reconstructs detail from normalized search metadata; full document body and attachment parsing are not implemented yet. |
| `compare_regulatory_updates` | Implemented, metadata-backed | Compares FDA / TFDA updates by agency, topic, product modality, or document status. |
| `search_clinical_trials_by_indication` | Implemented | Uses ClinicalTrials.gov API v2. |
| `compare_companies_by_indication` | Implemented, minimal MVP aggregation | Compares sponsor-name-based ClinicalTrials.gov trial activity by indication; does not infer clinical success, approval probability, commercial strength, or company superiority. |
| `check_source_health` | Implemented | Checks FDA, TFDA, and ClinicalTrials.gov source health. |
| `list_source_failures` | Implemented, current snapshot | Converts current source health results into failure records; no historical event store. |
| `generate_regulatory_digest` | Implemented, minimal MVP aggregation | Generates a rule-based MVP v1 digest from existing regulatory search, clinical trial search, source health, and source failure outputs; not a final regulatory or clinical assessment. |

MVP v1 should continue to focus on FDA, TFDA, and ClinicalTrials.gov only. EMA, NMPA, PMDA, historical failure storage, scheduling, alerting, and advanced report generation should remain out of scope unless a separate post-MVP decision explicitly approves the change.

---

## Post-MVP Documentation Index

These documents make MVP v1 easier to use, review, and govern. They are not source expansion approvals.

| Document | Use |
|---|---|
| `docs/mvp_v1_completion_note.md` | Records the MVP v1 baseline, active sources, implemented tools, tag, validation, and limitations. |
| `docs/mcp_usage_examples.md` | Shows safe practical examples for using the MVP v1 MCP tools. |
| `docs/sample_prompts.md` | Provides copy-paste prompts that keep usage inside MVP v1 scope. |
| `docs/tool_output_review_checklist.md` | Provides checklist items for reviewing MCP outputs before regulatory, clinical, PM, or management-facing use. |
| `docs/live_source_behavior_notes.md` | Explains live-source behavior such as empty results, missing metadata, keyword sensitivity, and source health caveats. |
| `docs/post_mvp_source_expansion_decision_matrix.md` | Defines the gate for evaluating whether any future source expansion is justified and scope-controlled. |
| `docs/claude_project_validation_workflow.md` | Defines the Claude Project setup and validation workflow for safe MVP v1 MCP output use. |

---

## Non-Expansion Reminder

This repository should stay controlled and phase-based.

Do not add new agencies, tools, workflows, or markdown files unless they clearly support the current phase or have been explicitly approved.

When uncertain, keep the implementation smaller and document the limitation clearly.
