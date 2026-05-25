# AGENTS.md

## 1. Purpose

This document defines engineering rules for Codex, coding agents, and other AI development agents working in this repository.

It governs how agents should create code, modify files, maintain MCP tool contracts, implement connectors, write tests, and avoid uncontrolled project expansion.

This file is an **engineering execution rule document**. It is not a Claude report guide, parser specification, database schema, or regulatory strategy document.

---

## 2. Agent Role

Coding agents should help implement and maintain the Pharmaceutical Regulatory and Clinical Intelligence System.

Agents may work on:

```text
source connectors
normalization logic
classification logic
MCP server implementation
source health monitoring
tests
documentation synchronization
repository maintenance
```

Agents should not act as:

```text
final regulatory decision makers
legal advisors
medical advisors
clinical success predictors
business strategy decision makers
```

Agents must not generate unsupported regulatory, medical, legal, or clinical conclusions.

---

## 3. Required Reading Order

Before modifying the repository, agents must read or check the following files in order:

```text
1. PROJECT_INSTRUCTION.md
2. README.md
3. docs/source_priority_matrix.md
4. docs/product_modality_taxonomy.md
5. docs/data_dictionary.md
6. docs/mcp_tool_contract.md
7. workflows/regulatory_clinical_intelligence_workflow.md
8. CLAUDE.md
9. AGENTS.md
```

Agents must use these files to understand:

```text
project scope
current implementation phase
approved sources
product modality labels
normalized data fields
MCP tool names and parameters
workflow sequence
Claude execution rules
engineering rules
```

---

## 4. Current MVP v1 Boundary

The current implementation phase is:

```text
MVP v1
```

MVP v1 active sources are:

```text
FDA
TFDA
ClinicalTrials.gov
```

Agents may implement:

```text
FDA regulatory update connectors
TFDA regulatory update connectors
ClinicalTrials.gov API v2 connector
basic normalization
basic product_modality classification
basic source health monitoring
basic MCP tools
basic tests
```

Agents must not implement the following during MVP v1 unless explicitly approved:

```text
EMA
NMPA
CDE
PMDA
WHO ICTRP
EU CTIS
literature intelligence
patent intelligence
commercial intelligence
Notion integration
Slack / Teams bot integration
advanced dashboard
automatic GitHub Issue creation, unless specifically requested
```

Agents may leave later-phase placeholders only if they are clearly marked as inactive and do not create working code paths.

---

## 5. Repository Path Rule

All directory names must use lowercase.

Approved directory names:

```text
docs/
workflows/
templates/
config/
src/
tests/
data/
.github/
```

Do not create or reference:

```text
DOCS/
Docs/
WORKFLOWS/
Workflows/
TEMPLATES/
Templates/
CONFIG/
SRC/
TESTS/
DATA/
```

Standard root files may use uppercase:

```text
README.md
PROJECT_INSTRUCTION.md
CLAUDE.md
AGENTS.md
LICENSE
```

When adding references in markdown, code, tests, or configuration, use the exact lowercase paths.

---

## 6. File Creation Rule

Agents must avoid unnecessary file creation.

Before creating a new file, confirm that the content cannot reasonably fit into an existing core file.

Do not create new markdown files unless needed.

Prefer updating existing files:

```text
PROJECT_INSTRUCTION.md
README.md
docs/source_priority_matrix.md
docs/product_modality_taxonomy.md
docs/data_dictionary.md
docs/mcp_tool_contract.md
workflows/regulatory_clinical_intelligence_workflow.md
CLAUDE.md
AGENTS.md
```

Do not create duplicate files with similar purpose.

Examples of files that should not be created during MVP v1 without explicit approval:

```text
docs/biologics_taxonomy.md
AGENT_TOPOLOGY.md
docs/agent_topology.md
docs/advanced_architecture.md
docs/full_database_schema.md
docs/ema_connector_spec.md
docs/nmpa_connector_spec.md
docs/pmda_connector_spec.md
```

---

## 7. Connector Development Rule

Connectors must follow:

```text
docs/source_priority_matrix.md
```

Source priority order:

```text
Official API
  > Official RSS feed
  > Official open data portal
  > Official downloadable file
  > Official HTML page
  > Controlled fallback parser
```

Agents must not use non-official sources as primary evidence.

Agents must not implement a lower-priority source before a higher-priority source has been evaluated, tested, or explicitly marked unavailable.

Each connector should preserve:

```text
source_id
agency_or_registry
source_type
endpoint_url
retrieved_at
official_url
publication_date or last_update_date
raw response or snapshot metadata
known limitations
```

---

## 8. MVP v1 Connector Scope

### 8.1 FDA

MVP v1 FDA work may include:

```text
openFDA connector
FDA RSS or official update page connector
FDA guidance page connector
FDA attachment metadata extraction
```

FDA connector outputs should normalize into:

```text
RegulatoryUpdate
```

### 8.2 TFDA

MVP v1 TFDA work may include:

```text
TFDA DataAction API or official data endpoint connector
data.gov.tw TFDA dataset connector
TFDA RSS or official announcement page connector
TFDA attachment metadata extraction
```

TFDA connector outputs should normalize into:

```text
RegulatoryUpdate
```

### 8.3 ClinicalTrials.gov

MVP v1 ClinicalTrials.gov work may include:

```text
ClinicalTrials.gov API v2 connector
trial search by indication
trial search by sponsor/company
trial filtering by phase and status
trial results availability extraction
```

ClinicalTrials.gov connector outputs should normalize into:

```text
ClinicalTrialRecord
```

---

## 9. MCP Server Development Rule

MCP tools must follow:

```text
docs/mcp_tool_contract.md
```

Approved core MCP tools:

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

MVP v1 should prioritize:

```text
search_regulatory_updates
get_regulatory_document_detail
search_clinical_trials_by_indication
check_source_health
list_source_failures
generate_regulatory_digest
```

Do not invent new MCP tool names.

Do not rename MCP tools without updating:

```text
docs/mcp_tool_contract.md
CLAUDE.md
README.md
tests/
```

MCP tools should query normalized data, not raw parser output.

---

## 10. Data Model Rule

Normalized records must follow:

```text
docs/data_dictionary.md
```

Core record types:

```text
RegulatoryUpdate
ClinicalTrialRecord
SourceHealthEvent
DigestRecord
```

Agents must preserve required fields and controlled vocabulary.

Do not add new normalized record types without updating:

```text
docs/data_dictionary.md
docs/mcp_tool_contract.md
workflows/regulatory_clinical_intelligence_workflow.md
```

Do not silently change field meanings.

---

## 11. Product Modality Rule

Agents must use:

```text
product_modality
```

Do not introduce or reintroduce:

```text
biologic_type
```

Product modality labels must come from:

```text
docs/product_modality_taxonomy.md
```

MVP v1 supported labels:

```text
small_molecule
peptide
oligonucleotide
mrna_rna
antibody
adc
recombinant_protein
biosimilar
vaccine
cell_therapy
gene_therapy
radiopharmaceutical
combination_product
unknown
requires_manual_review
```

If classification is uncertain, use:

```text
unknown
requires_manual_review
```

Do not force modality classification based on weak keywords.

---

## 12. Source Health Rule

Agents must implement source health handling for connectors and MCP tools.

Source health issues include:

```text
API unavailable
API schema drift
RSS unavailable
HTML selector breakage
empty result anomaly
data volume anomaly
attachment download failure
date parsing failure
encoding issue
duplicate anomaly
```

When source health issues occur, create or return structured information compatible with:

```text
SourceHealthEvent
```

defined in:

```text
docs/data_dictionary.md
```

MCP tools must not hide source failures.

Use partial-result warnings when some sources succeed and others fail.

---

## 13. Error Handling Rule

Agents must implement structured errors.

Recommended error codes:

```text
SOURCE_UNAVAILABLE
INVALID_PARAMETER
NO_RESULTS
PARTIAL_RESULTS
DATA_NOT_INGESTED
CLASSIFICATION_UNCERTAIN
INTERNAL_ERROR
```

Do not silently fail.

Do not return empty results without explaining whether the cause is:

```text
no matching records
source unavailable
source out of phase
data not ingested
query too narrow
internal error
```

---

## 14. Testing Rule

Agents should add or update tests when adding or changing:

```text
connectors
normalization logic
classification logic
MCP tools
source health checks
data field mappings
date parsing
deduplication logic
```

Tests should cover:

```text
normal successful result
no result
partial result
source unavailable
schema drift or missing required field
invalid parameter
classification uncertainty
deduplication behavior
```

Do not implement only happy-path tests.

---

## 15. Documentation Sync Rule

When changing source behavior, update or confirm:

```text
docs/source_priority_matrix.md
```

When changing product modality labels, update or confirm:

```text
docs/product_modality_taxonomy.md
```

When changing normalized fields, update or confirm:

```text
docs/data_dictionary.md
```

When changing MCP tool names, parameters, or outputs, update or confirm:

```text
docs/mcp_tool_contract.md
CLAUDE.md
```

When changing workflow order, phase boundary, or execution behavior, update or confirm:

```text
workflows/regulatory_clinical_intelligence_workflow.md
PROJECT_INSTRUCTION.md
```

When changing repo onboarding or user-facing entry points, update or confirm:

```text
README.md
```

---

## 16. No Unapproved Expansion Rule

Agents must not expand project scope without explicit approval.

Do not add:

```text
new agencies
new registries
new data sources
new MCP tools
new report types
new agent topology files
new dashboards
new integrations
new storage systems
```

unless the user has approved the change and the relevant governance documents are updated.

When uncertain, implement less and document the limitation.

---

## 17. Raw Data and Processed Data Rule

Raw source data and processed normalized data must be kept conceptually separate.

Suggested structure:

```text
data/raw/
data/processed/
data/snapshots/
data/indexes/
```

Raw snapshots should preserve retrieval evidence.

Processed records should follow:

```text
docs/data_dictionary.md
```

Do not overwrite raw snapshots with processed summaries.

Do not expose raw parser output directly through MCP tools.

---

## 18. Security and Access Rule

Agents must not:

```text
store secrets in the repository
commit API keys
hard-code credentials
bypass access controls
scrape private or restricted data
collect non-public company information
submit anything to regulatory authorities
send emails or external notifications unless explicitly approved
```

Use environment variables for secrets.

If an API key is required, document it in:

```text
.env.example
```

without including real credentials.

---

## 19. Coding Style Rule

Unless the user specifies otherwise, agents should prefer:

```text
clear modular code
small functions
typed data models where practical
explicit error handling
testable connector functions
stable interfaces
minimal dependencies
readable configuration files
```

Avoid:

```text
large monolithic scripts
hidden global state
hard-coded source URLs scattered across code
silent exception swallowing
uncontrolled retries
unstructured JSON output
```

---

## 20. Dependency Rule

Agents should keep dependencies minimal.

Before adding a new dependency, verify that:

```text
it is necessary
it is actively maintained
it does not duplicate existing functionality
it is compatible with the intended runtime
it does not create unnecessary cost or licensing concerns
```

Do not add heavy frameworks before MVP v1 works end to end.

---

## 21. Configuration Rule

Source endpoints, phase activation, date range presets, and alert behavior should be configurable.

Suggested configuration directories:

```text
config/sources/
config/taxonomy/
config/runtime/
```

Do not hard-code phase activation or source priority only in application code.

Configuration must remain consistent with:

```text
docs/source_priority_matrix.md
PROJECT_INSTRUCTION.md
```

---

## 22. Pull Request / Change Summary Rule

When completing a change, agents should summarize:

```text
files changed
purpose of the change
whether any governance document was updated
tests added or updated
known limitations
next recommended step
```

If tests were not run, agents should state that clearly.

Do not claim that code was tested if no test was run.

---

## 23. Relationship to Claude

`CLAUDE.md` governs Claude analysis and reporting behavior.

`AGENTS.md` governs coding-agent engineering behavior.

Coding agents should not modify `CLAUDE.md` unless the change affects Claude execution rules, MCP usage, or reporting behavior.

Claude should not modify code unless explicitly asked to perform implementation work.

---

## 24. Current Build Instruction

For the current build stage, agents should focus on MVP v1 only:

```text
FDA regulatory update connector
TFDA regulatory update connector
ClinicalTrials.gov API v2 connector
basic normalization
basic product_modality classification
basic source health monitoring
basic MCP tools
basic tests
```

Do not implement v2 or v3 sources until the user explicitly approves moving to the next phase.

