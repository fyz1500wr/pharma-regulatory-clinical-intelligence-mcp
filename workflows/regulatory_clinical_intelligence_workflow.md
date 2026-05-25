# Regulatory Clinical Intelligence Workflow

## 1. Purpose

This document defines the end-to-end workflow for the Pharmaceutical Regulatory and Clinical Intelligence System.

It explains how official regulatory and clinical trial data should move through the system:

```text
Official source
  → Source connector
  → Raw data snapshot
  → Normalization
  → Classification
  → Processed data store / index
  → MCP tools
  → Claude analysis
  → Digest / tracker / impact matrix
```

This file is a **workflow governance document**. It is not implementation code, a parser specification, a database schema, or a report template.

---

## 2. Relationship to Core Documents

This workflow depends on the following core documents:

```text
PROJECT_INSTRUCTION.md
docs/source_priority_matrix.md
docs/product_modality_taxonomy.md
docs/data_dictionary.md
docs/mcp_tool_contract.md
```

Each document has a distinct role:

| Document | Role |
|---|---|
| `PROJECT_INSTRUCTION.md` | Governs overall project scope, phase boundaries, and non-expansion rules |
| `docs/source_priority_matrix.md` | Defines approved sources and source priority |
| `docs/product_modality_taxonomy.md` | Defines approved product modality labels |
| `docs/data_dictionary.md` | Defines normalized data fields |
| `docs/mcp_tool_contract.md` | Defines Claude-facing MCP tools |
| `workflows/regulatory_clinical_intelligence_workflow.md` | Defines how the system runs end to end |

If this workflow conflicts with `PROJECT_INSTRUCTION.md`, the project instruction governs the project scope.

---

## 3. Repository Path Rule

All referenced repository paths must use lowercase directory names except standard root files.

Approved examples:

```text
docs/source_priority_matrix.md
docs/product_modality_taxonomy.md
docs/data_dictionary.md
docs/mcp_tool_contract.md
workflows/regulatory_clinical_intelligence_workflow.md
templates/regulatory_update_digest_template.md
```

Do not use:

```text
DOCS/
Docs/
WORKFLOWS/
Templates/
```

Standard root files may remain uppercase:

```text
README.md
PROJECT_INSTRUCTION.md
CLAUDE.md
AGENTS.md
LICENSE
```

---

## 4. Workflow Overview

The system should follow this high-level workflow:

```text
1. Select approved sources
2. Retrieve data through source connectors
3. Save raw data snapshots
4. Normalize records into standard data structures
5. Classify product modality, topic, indication, and impact
6. Deduplicate and validate records
7. Store processed records and indexes
8. Expose data through MCP tools
9. Claude queries MCP tools
10. Claude generates digest, tracker, comparison, or impact matrix
11. Source health monitoring runs continuously
12. Failures are logged as SourceHealthEvent records
```

The system should not skip directly from raw source scraping to Claude-generated reports.

---

## 5. MVP v1 Workflow Scope

MVP v1 should implement only the minimum workflow needed to prove the system works end to end.

### 5.1 Included Sources

MVP v1 includes:

```text
FDA
TFDA
ClinicalTrials.gov
```

### 5.2 Included Workflows

MVP v1 includes:

```text
FDA regulatory update workflow
TFDA regulatory update workflow
ClinicalTrials.gov clinical trial workflow
Basic product modality classification
Basic regulatory topic classification
Basic source health monitoring
Basic MCP query workflow
Basic Claude digest generation
```

### 5.3 Excluded from MVP v1

Do not implement the following until explicitly approved for later phases:

```text
EMA
NMPA / CDE
PMDA
WHO ICTRP
EU CTIS
literature intelligence
patent intelligence
commercial intelligence
advanced dashboards
Slack / Teams / Notion integration
```

---

## 6. Regulatory Update Workflow

### 6.1 Purpose

The regulatory update workflow collects official regulatory information from approved agency sources and converts it into normalized `RegulatoryUpdate` records.

### 6.2 Workflow Steps

```text
1. Read approved sources from docs/source_priority_matrix.md
2. Select active MVP v1 sources
3. Retrieve updates from official API, RSS, open data, downloadable file, or official HTML page
4. Save raw response or raw snapshot
5. Extract title, date, official URL, document type, document status, and attachment links
6. Normalize extracted fields into RegulatoryUpdate format
7. Classify product modality
8. Classify regulatory topic
9. Estimate impact level conservatively
10. Validate required fields
11. Deduplicate records
12. Store processed records
13. Expose records through MCP tools
```

### 6.3 MVP v1 Regulatory Sources

MVP v1 should prioritize:

```text
FDA openFDA
FDA RSS / official update pages
FDA guidance pages
TFDA DataAction API / official data endpoints
data.gov.tw TFDA datasets
TFDA RSS / official announcement pages
```

### 6.4 Required Normalized Record

The output should follow:

```text
RegulatoryUpdate
```

as defined in:

```text
docs/data_dictionary.md
```

### 6.5 Required MCP Support

The regulatory update workflow should support:

```text
search_regulatory_updates
get_regulatory_document_detail
generate_regulatory_digest
```

After MVP v1 is stable, it may also support:

```text
compare_regulatory_updates
```

---

## 7. Clinical Trial Workflow

### 7.1 Purpose

The clinical trial workflow collects official clinical trial registry data and converts it into normalized `ClinicalTrialRecord` records.

### 7.2 Workflow Steps

```text
1. Read approved clinical trial sources from docs/source_priority_matrix.md
2. Select active MVP v1 registries
3. Query ClinicalTrials.gov API v2 by indication, company, phase, status, and date range
4. Retrieve study details and result availability
5. Save raw API response
6. Normalize study fields into ClinicalTrialRecord format
7. Classify product modality based on intervention name and study description
8. Normalize sponsor and collaborator names
9. Validate trial ID, official URL, title, sponsor, phase, status, and last update date
10. Deduplicate trial records by official trial ID
11. Store processed trial records
12. Expose records through MCP tools
```

### 7.3 MVP v1 Clinical Trial Sources

MVP v1 should prioritize:

```text
ClinicalTrials.gov API v2
```

TFDA clinical trial open data may be added within MVP v1 if the FDA / TFDA / ClinicalTrials.gov core flow remains stable.

### 7.4 Required Normalized Record

The output should follow:

```text
ClinicalTrialRecord
```

as defined in:

```text
docs/data_dictionary.md
```

### 7.5 Required MCP Support

The clinical trial workflow should support:

```text
search_clinical_trials_by_indication
generate_regulatory_digest
```

After MVP v1 is stable, it may also support:

```text
compare_companies_by_indication
```

---

## 8. Raw Data Snapshot Workflow

### 8.1 Purpose

Raw snapshots preserve evidence of what the connector retrieved before normalization.

### 8.2 Snapshot Rule

For each source retrieval, the system should preserve enough information to debug later issues.

Recommended snapshot metadata:

```text
source_id
agency_or_registry
source_type
endpoint_url
retrieved_at
raw_file_path
response_status
content_hash
record_count
known_limitations
```

### 8.3 Storage Rule

Raw snapshots should be stored separately from processed records.

Suggested directory:

```text
data/raw/
```

Processed records should not overwrite raw snapshots.

---

## 9. Normalization Workflow

### 9.1 Purpose

Normalization converts heterogeneous source data into standard records defined in `docs/data_dictionary.md`.

### 9.2 Regulatory Normalization

Regulatory source data should normalize into:

```text
RegulatoryUpdate
```

Required actions:

```text
extract official title
extract publication date or last update date
extract official URL
extract attachment links
normalize agency and region
normalize document type
normalize document status
preserve source type
preserve retrieval timestamp
record known limitations
```

### 9.3 Clinical Trial Normalization

Clinical trial source data should normalize into:

```text
ClinicalTrialRecord
```

Required actions:

```text
preserve official trial ID
preserve official registry URL
extract title and brief summary
extract indication or condition
extract sponsor and collaborators
extract intervention names
extract phase and status
extract country information
extract start and completion dates
extract results availability
preserve retrieval timestamp
record known limitations
```

### 9.4 Validation

After normalization, the system should validate:

```text
required fields are present
dates are parseable
official URL is present
source_type is present
product_modality uses approved labels
unknown and requires_manual_review are used when appropriate
```

---

## 10. Product Modality Classification Workflow

### 10.1 Purpose

Product modality classification allows regulatory updates and clinical trials to be filtered by therapeutic product type.

### 10.2 Approved Taxonomy

Classification must use:

```text
docs/product_modality_taxonomy.md
```

MVP v1 supported top-level labels:

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

### 10.3 Classification Steps

```text
1. Preserve source-provided product description
2. Match explicit modality terms first
3. Use intervention names and document text only when sufficiently clear
4. Assign primary modality
5. Assign secondary modalities only when needed
6. Assign classification confidence
7. Use unknown or requires_manual_review when uncertain
```

### 10.4 Do Not Over-Classify

Do not create new modality labels for:

```text
targets
mechanisms of action
payloads
formulations
routes of administration
disease areas
regulatory pathways
```

These should be handled as separate fields if needed.

---

## 11. Regulatory Topic and Impact Classification Workflow

### 11.1 Purpose

Regulatory topic and impact classification helps Claude identify which updates may affect CMC, clinical, quality, regulatory affairs, or other functions.

### 11.2 Approved Topic Labels

Use topic labels defined in:

```text
docs/data_dictionary.md
docs/mcp_tool_contract.md
```

Examples:

```text
CMC
quality
clinical
nonclinical
GMP
GCP
GLP
pharmacovigilance
labeling
submission
eCTD
manufacturing
inspection
safety
post_approval
general
unknown
requires_manual_review
```

### 11.3 Impact Levels

Use:

```text
low
medium
high
critical
unknown
requires_manual_review
```

### 11.4 Classification Steps

```text
1. Read title, summary, document type, and source category
2. Identify topic keywords conservatively
3. Identify impacted functions only when supported
4. Estimate impact level conservatively
5. Record classification confidence
6. Add classification notes for uncertain items
```

### 11.5 Impact Classification Restriction

The system may suggest likely impact, but it must not make final regulatory, legal, clinical, or filing decisions.

Claude reports should clearly state that impact assessment is an intelligence support output.

---

## 12. Deduplication Workflow

### 12.1 Purpose

Deduplication prevents repeated source entries from creating duplicated reports.

### 12.2 Regulatory Deduplication Keys

Use a combination of:

```text
agency
official_url
title
publication_date
last_update_date
content_hash
```

### 12.3 Clinical Trial Deduplication Keys

Use:

```text
registry
trial_id
official_url
last_update_date
```

### 12.4 Deduplication Rule

Do not delete potential duplicates without preserving a deduplication reason.

When uncertain, keep records separate and mark:

```text
requires_manual_review
```

---

## 13. Source Health Monitoring Workflow

### 13.1 Purpose

Source health monitoring detects source failure, parser failure, schema drift, and webpage redesign.

### 13.2 Health Check Types

The system should check:

```text
HTTP status
API response schema
RSS feed availability
HTML selector behavior
attachment download success
empty result anomaly
data volume anomaly
date parsing
character encoding
duplicate anomaly
```

### 13.3 SourceHealthEvent Creation

When a source issue occurs, create:

```text
SourceHealthEvent
```

as defined in:

```text
docs/data_dictionary.md
```

### 13.4 Required Failure Metadata

Each source health event should include:

```text
failure_id
source_id
agency_or_registry
source_type
endpoint_url
status
failure_type
severity
detected_at
error_message
suggested_fix
suggested_connector_file
```

### 13.5 Required MCP Support

Source health monitoring should support:

```text
check_source_health
list_source_failures
```

### 13.6 GitHub Issue Creation

Automatic GitHub Issue creation is a v3 feature unless explicitly approved earlier.

MVP v1 should at minimum create structured source health records.

---

## 14. Processed Data Store and Index Workflow

### 14.1 Purpose

Processed data should be stored in a format that can be queried by MCP tools.

### 14.2 MVP v1 Storage

MVP v1 may use simple storage such as:

```text
JSONL
SQLite
local JSON files
lightweight search index
```

The exact storage implementation should be chosen during coding.

### 14.3 Storage Requirements

Processed storage must preserve:

```text
normalized records
source metadata
retrieval date
official URL
classification output
known limitations
source health status
```

### 14.4 Do Not Overbuild

Do not implement a complex production database before MVP v1 works end to end.

---

## 15. MCP Query Workflow

### 15.1 Purpose

MCP tools provide Claude with controlled access to processed intelligence data.

### 15.2 Query Flow

```text
Claude asks a source-based question
  → MCP tool receives structured parameters
  → MCP tool queries processed data
  → MCP tool returns source-traceable results
  → Claude summarizes and reports results
```

### 15.3 Approved MCP Tools

MVP v1 should support:

```text
search_regulatory_updates
get_regulatory_document_detail
search_clinical_trials_by_indication
check_source_health
list_source_failures
generate_regulatory_digest
```

After MVP v1 is stable, add:

```text
compare_regulatory_updates
compare_companies_by_indication
```

### 15.4 MCP Restrictions

MCP tools should not:

```text
return raw parser output directly
hide source failures
use non-official sources as primary evidence
silently include out-of-phase sources
silently omit partial failure warnings
```

---

## 16. Claude Report Generation Workflow

### 16.1 Purpose

Claude uses MCP results to generate structured intelligence outputs.

### 16.2 Supported Output Types

The workflow should support:

```text
regulatory update digest
product modality-specific regulatory update report
cross-agency comparison table
regulatory impact matrix
indication-based clinical trial tracker
company-by-company clinical trial comparison
source health failure report
```

### 16.3 Report Generation Steps

```text
1. User specifies date range, sources, product modality, indication, company, or topic
2. Claude calls relevant MCP tools
3. Claude reviews returned records and source metadata
4. Claude identifies key updates and limitations
5. Claude generates summary, tables, or impact matrix
6. Claude clearly states date range and sources searched
7. Claude includes official source URLs from MCP outputs
8. Claude flags partial results or uncertain classifications
```

### 16.4 Report Restrictions

Claude should not:

```text
invent missing source data
claim regulatory approval likelihood without evidence
treat trial status as clinical success
treat draft guidance as final guidance
hide source health failures
ignore known limitations
```

---

## 17. Error Handling Workflow

### 17.1 Error Categories

Use structured error categories:

```text
SOURCE_UNAVAILABLE
INVALID_PARAMETER
NO_RESULTS
PARTIAL_RESULTS
DATA_NOT_INGESTED
CLASSIFICATION_UNCERTAIN
INTERNAL_ERROR
```

### 17.2 No-Result Handling

No results should distinguish among:

```text
no matching records exist
source was not searched because it is out of phase
source was unavailable
query was too narrow
data has not yet been ingested
```

### 17.3 Partial Results

When some sources fail but others succeed, return partial results with a clear warning.

Do not silently present partial results as complete.

---

## 18. Phase Expansion Workflow

### 18.1 v2 Expansion

v2 may add:

```text
EMA RSS connector
EMA medicine data downloader
EMA scientific guideline parser
improved regulatory topic classification
improved product modality taxonomy
cross-agency comparison reports
```

Before v2 implementation, update or confirm:

```text
docs/source_priority_matrix.md
docs/mcp_tool_contract.md
docs/data_dictionary.md
```

### 18.2 v3 Expansion

v3 may add:

```text
NMPA / CDE parser
PMDA RSS and webpage parser
PDF and attachment parser
selector break detector
schema drift detector
GitHub Issue auto-notification
advanced source health reporting
```

Before v3 implementation, update or confirm:

```text
docs/source_priority_matrix.md
docs/mcp_tool_contract.md
docs/data_dictionary.md
AGENTS.md
```

### 18.3 Future Expansion

Future sources or features must not be added unless explicitly approved.

Examples:

```text
WHO ICTRP
EU CTIS
literature search
patent intelligence
commercial intelligence
Notion integration
Slack / Teams bot
```

---

## 19. Maintenance Workflow

### 19.1 When This Workflow Must Be Updated

Update this workflow before:

```text
adding a new source workflow
adding a new MCP tool
adding a new normalized record type
adding a new report output type
changing phase boundaries
changing source health handling
changing Claude execution behavior
```

### 19.2 Consistency Check

Before implementing workflow changes, confirm consistency with:

```text
PROJECT_INSTRUCTION.md
docs/source_priority_matrix.md
docs/product_modality_taxonomy.md
docs/data_dictionary.md
docs/mcp_tool_contract.md
```

### 19.3 Non-Expansion Rule

Do not add new workflow files unless the workflow cannot reasonably fit into this document.

Prefer updating this workflow over creating duplicate workflow documents.

---

## 20. Current Build Instruction

For the current build stage, implement only the MVP v1 workflow:

```text
FDA regulatory update workflow
TFDA regulatory update workflow
ClinicalTrials.gov clinical trial workflow
basic normalization
basic product modality classification
basic source health monitoring
basic MCP query workflow
basic Claude digest generation
```

Do not implement v2 or v3 workflows until the user explicitly approves moving to the next phase.

