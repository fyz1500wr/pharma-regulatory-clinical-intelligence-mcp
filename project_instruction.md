# PROJECT_INSTRUCTION.md

## 1. Project Purpose

This repository is designed to build a **Pharmaceutical Regulatory and Clinical Intelligence System** that can be developed in GitHub/Codex and later executed through Claude using MCP tools.

The system tracks regulatory updates and clinical trial developments from official or high-reliability public sources, normalizes the data, classifies it by biologic product type and indication, and makes the results available for Claude-based analysis and reporting.

The primary use cases are:

1. Track regulatory laws, guidelines, notices, Q&A documents, and industry guidance from FDA, EMA, TFDA, NMPA, and PMDA.
2. Capture the publication date, update date, source agency, official URL, document status, and attachment links for each regulatory update.
3. Search and classify updates by biologic product type, regulatory topic, and development impact.
4. Track clinical trials by indication, sponsor/company, product type, phase, recruitment status, country, trial update date, and results availability.
5. Detect source failure, API schema changes, HTML structure changes, missing attachments, and webpage redesigns.
6. Expose standardized tools through MCP so Claude can query, summarize, compare, and generate reports without directly scraping raw websites.

This project is not intended to be a simple web scraper. It is a controlled intelligence pipeline with source governance, reproducible data processing, MCP-based access, and audit-friendly source traceability.

---

## 2. Core System Principles

### 2.1 Official Source First

The system must prioritize official and authoritative data sources.

Source priority order:

1. Official API
2. Official RSS feed
3. Official open data portal
4. Official downloadable dataset, such as CSV, JSON, XML, XLSX, or PDF
5. Official HTML page
6. Fallback HTML parser only when no structured official source exists

Non-official sources may only be used for supplementary context and must not replace official sources for regulatory or clinical trial conclusions.

### 2.2 Traceability Required

Every regulatory or clinical trial record must retain enough metadata for source tracing.

At minimum, each record should include:

- Source agency or registry
- Official title
- Publication date or last update date
- Official URL
- Attachment URL, if available
- Retrieval date
- Source type, such as API, RSS, open data, download file, or HTML parser
- Data hash or content fingerprint, when available

Claude-generated reports must be able to reference the original official source.

### 2.3 Claude Does Not Directly Scrape Raw Sources

Claude should not directly browse or scrape FDA, EMA, TFDA, NMPA, PMDA, or clinical trial registry pages during normal operation.

Claude should query the standardized MCP tools provided by this repository.

The intended architecture is:

```text
Official sources
  → Connectors
  → Normalization
  → Classification
  → Storage / Index
  → MCP tools
  → Claude analysis and reports
```

### 2.4 Controlled Expansion

This project must not expand randomly.

New data sources, new MCP tools, new markdown files, and new workflows may only be added when they clearly support the current project scope or the current implementation phase.

When in doubt, update an existing core document instead of creating a new one.

---

## 3. Target Data Domains

The system covers two primary data domains.

### 3.1 Regulatory Intelligence

Regulatory Intelligence includes:

- Laws and regulations
- Draft guidance
- Final guidance
- Scientific guidelines
- Q&A documents
- Consultation documents
- Regulatory notices
- GMP / GCP / GLP / pharmacovigilance updates
- CMC-related regulatory updates
- Clinical development guidance
- eCTD and submission-related updates
- Labeling and post-approval requirements
- Biologic-specific regulatory updates

### 3.2 Clinical Trial Intelligence

Clinical Trial Intelligence includes:

- Clinical trial registry updates
- Trial status changes
- New trial registration
- Sponsor or collaborator changes
- Phase changes
- Recruitment status changes
- Primary completion date changes
- Results posted or updated
- Indication-specific trial landscape
- Company-specific clinical pipeline tracking
- Biologic modality and intervention classification

---

## 4. Covered Agencies and Sources

The system is designed to support the following agencies and registries.

### 4.1 Regulatory Agencies

| Agency | Region | Scope |
|---|---|---|
| FDA | United States | Drug, biologics, CBER, CDER, guidance, openFDA data, safety, labeling, recalls |
| EMA | European Union | Human medicines, scientific guidelines, medicine data, RSS updates |
| TFDA | Taiwan | News, announcements, open data, clinical trial datasets, regulatory updates |
| NMPA / CDE | China | Regulatory notices, technical guidelines, CDE guidance, drug review-related updates |
| PMDA | Japan | RSS, review services, safety updates, approved products, regulatory notices |

### 4.2 Clinical Trial Sources

| Source | Priority | Intended Use |
|---|---|---|
| ClinicalTrials.gov API v2 | Primary | Global trial search, study details, status, phase, sponsor, results |
| TFDA open data | Secondary | Taiwan clinical trial tracking |
| EU clinical trial sources | Later phase | EU trial tracking where structured data is available |
| WHO ICTRP | Later phase / supplementary | Cross-registry reference and broader trial discovery |

---

## 5. Source Priority Rule

All connectors must follow this source priority rule.

```text
Official API
  > Official RSS feed
  > Official open data portal
  > Official downloadable file
  > Official HTML page
  > Controlled fallback parser
```

### 5.1 API Rule

If an official API exists, the connector must use the API before attempting web scraping.

Examples:

- openFDA for FDA public drug/device/food datasets
- ClinicalTrials.gov API v2 for clinical trial data
- TFDA DataAction or open data endpoints where available

### 5.2 RSS Rule

If an official RSS feed exists, it should be used for update detection.

RSS is especially useful for:

- Recently published updates
- News and announcements
- Monitoring changes without scraping full webpages

### 5.3 HTML Parser Rule

HTML parsing is allowed only when no official API, RSS feed, or downloadable data source is available.

HTML parsers must include:

- Selector validation
- Empty result detection
- Link extraction validation
- Date parsing validation
- Source health event generation when parsing fails

### 5.4 Attachment Rule

When regulatory pages link to PDF, Word, Excel, or other attachments, the connector should store attachment metadata.

At minimum:

- Attachment URL
- File name
- File type
- Download status
- File hash, if downloaded
- Parent source URL

---

## 6. Date Range Rule

The system must support the following standard date ranges:

```text
1m  = last 1 month
3m  = last 3 months
6m  = last 6 months
1y  = last 1 year
3y  = last 3 years
5y  = last 5 years
```

Date filters should be applied based on the most appropriate available date field:

1. Official publication date
2. Official update date
3. Registry last updated date
4. Retrieval date, only when no official date is available

The system should clearly distinguish:

- Publication date
- Last updated date
- Retrieval date
- Effective date, if available
- Consultation deadline, if available

Claude reports must not confuse retrieval date with publication date.

---

## 7. Biologic Product Type Scope

The system must support biologic product type classification.

The detailed taxonomy is maintained in:

```text
docs/biologics_taxonomy.md
```

At the project instruction level, the supported top-level biologic categories are:

- Monoclonal antibody
- Bispecific antibody
- Antibody-drug conjugate
- Biosimilar
- Vaccine
- Cell therapy
- Gene therapy
- Recombinant protein
- Plasma-derived product
- Nucleic acid drug
- Microbiome or live biotherapeutic product
- Other biologic or advanced therapy product

Classification must be conservative.

If the system cannot confidently classify a document or trial, it should use:

```text
unknown
```

or

```text
requires_manual_review
```

rather than guessing.

---

## 8. Clinical Trial Tracking Scope

Clinical trial tracking should support indication- and company-based search.

The system should allow users to search by:

- Indication
- Disease area
- Sponsor or company
- Collaborator
- Intervention name
- Biologic product type
- Trial phase
- Trial status
- Country or region
- Study start date
- Primary completion date
- Last update date
- Results availability

The system should prioritize official registry data and preserve official trial identifiers.

For ClinicalTrials.gov records, the NCT number must be preserved.

The system should not make unsupported claims about clinical success, regulatory approval likelihood, or competitive superiority unless such conclusions are explicitly supported by official trial results, publications, or regulatory documents.

---

## 9. MCP Design Principle

The MCP layer is the controlled interface between Claude and the processed intelligence data.

Claude should use MCP tools to perform tasks such as:

- Search regulatory updates
- Retrieve regulatory document details
- Compare regulatory updates across agencies
- Search clinical trials by indication
- Compare companies by indication
- Check source health status
- List source failures
- Generate regulatory or clinical intelligence digests

The MCP layer should expose clean, stable tools. Tool names and parameters should not change casually.

Detailed MCP tool definitions are maintained in:

```text
docs/mcp_tool_contract.md
```

---

## 10. GitHub / Codex / Claude Responsibility Split

### 10.1 GitHub Responsibilities

GitHub is responsible for:

- Version control
- Repository structure
- Pull requests and change history
- GitHub Actions scheduling
- Issue tracking for parser failures and source changes
- Storing configuration, documentation, and source code

### 10.2 Codex Responsibilities

Codex is responsible for assisting with:

- Writing connectors
- Writing MCP server code
- Writing tests
- Refactoring code
- Debugging parser failures
- Updating source health checks
- Maintaining data normalization logic
- Maintaining classification logic

Codex should follow the rules in:

```text
AGENTS.md
```

### 10.3 Claude Responsibilities

Claude is responsible for:

- Querying MCP tools
- Summarizing regulatory updates
- Comparing agencies
- Producing indication-based clinical trial summaries
- Generating regulatory impact matrices
- Drafting weekly, monthly, or custom intelligence reports
- Explaining source health failures in business-friendly language

Claude should follow the rules in:

```text
CLAUDE.md
```

Claude should not silently invent missing source data.

---

## 11. Implementation Phase Boundary

The project must be implemented in phases to prevent uncontrolled growth.

### 11.1 MVP v1 Scope

MVP v1 focuses on the minimum working system.

Included in MVP v1:

1. FDA regulatory and open data sources
2. TFDA regulatory and open data sources
3. ClinicalTrials.gov API v2
4. Basic biologic product type classification
5. Basic indication and company tracking
6. Basic regulatory update digest
7. Basic source health check
8. Basic MCP tools for regulatory and clinical trial search

MVP v1 should prove that the full architecture works end to end:

```text
source → connector → normalization → classification → storage/index → MCP → Claude report
```

### 11.2 v2 Scope

v2 expands the system to EMA and improves classification depth.

Included in v2:

1. EMA RSS connector
2. EMA medicine data downloader
3. EMA scientific guideline parser
4. Improved biologic taxonomy
5. Improved regulatory topic classification
6. Regulatory impact matrix enhancement
7. Better report templates for cross-agency comparison

### 11.3 v3 Scope

v3 expands the system to NMPA, CDE, PMDA, and advanced monitoring.

Included in v3:

1. NMPA / CDE regulatory parser
2. PMDA RSS and webpage parser
3. PDF and attachment parser
4. Selector break detector
5. Schema drift detector
6. GitHub Issue auto-notification for source failures
7. Advanced source health dashboard or status report

### 11.4 Future Scope

The following items are not part of MVP v1 unless explicitly requested:

- Full EU CTIS integration
- WHO ICTRP integration
- Literature search MCP integration
- Patent intelligence
- Commercial drug sales intelligence
- Automated regulatory strategy recommendation engine
- Full local LLM deployment
- Enterprise document management integration
- Notion integration
- Slack or Teams bot integration

---

## 12. Source Health and Website Change Monitoring

The system must detect and report source failures.

Source health monitoring should include:

1. HTTP status check
2. API response validation
3. RSS feed validation
4. HTML selector validation
5. Attachment download validation
6. Empty result detection
7. Unexpected data volume detection
8. Schema drift detection
9. Content hash or DOM structure change detection, where appropriate

When a source failure is detected, the system should create a structured source health event.

A source health event should include:

- Source ID
- Agency or registry
- Endpoint URL
- Failure type
- Detection time
- Error message
- Last successful check time, if available
- Suggested file or connector to review
- Suggested severity

For later phases, the system may automatically create a GitHub Issue for source failures.

---

## 13. Output Expectations

The system should support the following output types:

1. Regulatory update digest
2. Biologic-specific regulatory update report
3. Cross-agency comparison table
4. Regulatory impact matrix
5. Indication-based clinical trial tracker
6. Company-by-company clinical trial comparison
7. Source health failure report
8. Parser failure or webpage change issue summary

All outputs should preserve source traceability.

Reports should clearly show:

- Date range
- Search criteria
- Agencies or registries searched
- Included product types
- Included indications
- Source URLs
- Data freshness
- Known limitations

---

## 14. Out of Scope

The following are out of scope unless explicitly added later:

1. Replacing professional regulatory judgment
2. Making final regulatory filing decisions
3. Predicting regulatory approval outcomes without evidence
4. Scraping non-official sources as primary evidence
5. Circumventing website access controls
6. Collecting private, confidential, or non-public company data
7. Automatically submitting anything to regulatory authorities
8. Automatically contacting companies, investigators, or agencies
9. Generating legal advice
10. Making medical treatment recommendations

This system is an intelligence support tool, not a substitute for regulatory, clinical, legal, or medical review.

---

## 15. Non-Expansion Rule

To prevent the project from becoming too large or disorganized, all contributors and AI coding agents must follow these rules:

1. Do not create new markdown files unless the current file clearly cannot contain the required instruction.
2. Prefer updating existing core documents over adding new documents.
3. Do not expand beyond the current implementation phase unless explicitly requested.
4. Do not add new agencies, registries, or data sources without updating the source priority matrix.
5. Do not add new MCP tools without updating the MCP tool contract.
6. Do not add new biologic product categories without updating the biologics taxonomy.
7. Do not change output formats without updating the relevant template or workflow document.
8. Do not create duplicate instructions in multiple files.
9. Do not add speculative features that are not required for regulatory or clinical intelligence.
10. When uncertain, keep the implementation smaller and document the limitation clearly.

---

## 16. Initial Core Markdown Files

The project should begin with the following core markdown files only:

```text
README.md
PROJECT_INSTRUCTION.md
CLAUDE.md
AGENTS.md
docs/source_priority_matrix.md
docs/biologics_taxonomy.md
docs/mcp_tool_contract.md
docs/data_dictionary.md
workflows/regulatory_clinical_intelligence_workflow.md
```

Additional files should only be created when the project needs them and when they do not duplicate existing documents.

---

## 17. Development Sequence

The recommended development order is:

1. Finalize `PROJECT_INSTRUCTION.md`
2. Create `docs/source_priority_matrix.md`
3. Create `docs/biologics_taxonomy.md`
4. Create `docs/mcp_tool_contract.md`
5. Create `docs/data_dictionary.md`
6. Create `workflows/regulatory_clinical_intelligence_workflow.md`
7. Create `CLAUDE.md`
8. Create `AGENTS.md`
9. Create `README.md`
10. Start MVP v1 implementation

This sequence ensures that the project rules, source scope, taxonomy, MCP contract, and workflow are controlled before code generation begins.

---

## 18. Current Recommended MVP v1 Build Target

The first build target should be:

```text
FDA + TFDA + ClinicalTrials.gov
```

MVP v1 should produce:

1. A working regulatory update ingestion pipeline for FDA and TFDA
2. A working ClinicalTrials.gov API connector
3. A normalized data format
4. A simple biologic type classifier
5. A simple indication/company search capability
6. A basic source health check
7. A basic MCP server exposing query tools
8. A Claude-generated regulatory or clinical intelligence report based on MCP results

Only after MVP v1 works end to end should EMA, NMPA, PMDA, and advanced monitoring be added.

