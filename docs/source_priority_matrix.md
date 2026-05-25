# Source Priority Matrix

## 1. Purpose

This document defines the approved source priority rules for the Pharmaceutical Regulatory and Clinical Intelligence System.

It governs which official sources should be used first, which fallback sources are allowed, and which sources should not be used as primary evidence.

This file is a **source governance document**, not a parser implementation guide.

Detailed parser logic, HTML selectors, retry logic, and code-level handling should be implemented in source code and tests, not in this document.

---

## 2. Global Source Priority Rule

All connectors must follow the same source priority order:

```text
Official API
  > Official RSS feed
  > Official open data portal
  > Official downloadable file
  > Official HTML page
  > Controlled fallback parser
```

A lower-priority source must not be implemented before a higher-priority source has been evaluated, tested, or explicitly marked unavailable.

Non-official sources may only be used for supplementary context. They must not be used as the primary evidence for regulatory or clinical trial conclusions.

---

## 3. Source Trust Level

| Trust Level | Source Type | Description | Use as Primary Evidence |
|---|---|---|---|
| Level 1 | Official API | Structured API provided by the official agency or registry | Yes |
| Level 2 | Official RSS / official open data | Official update feed or government open data portal | Yes |
| Level 3 | Official downloadable dataset | CSV, JSON, XML, XLSX, PDF, or other downloadable official file | Yes |
| Level 4 | Official HTML page | Official webpage without structured API or download | Yes, with parser health checks |
| Level 5 | Supplementary non-official source | Academic, industry, commercial, or third-party source | No, supplementary only |

---

## 4. Implementation Phase Control

The repository must not attempt to implement every source at once.

| Phase | Included Sources | Main Objective |
|---|---|---|
| MVP v1 | FDA, TFDA, ClinicalTrials.gov | Build a working end-to-end system |
| v2 | EMA | Add EU regulatory intelligence after MVP v1 is stable |
| v3 | NMPA / CDE, PMDA | Add China and Japan sources with stronger parser monitoring |
| Future | WHO ICTRP, EU CTIS, literature, patents, commercial intelligence | Only add after explicit approval |

---

## 5. MVP v1 Source Matrix

### 5.1 FDA

| Source | Type | Priority | Phase | Intended Use | Risk Level | Fallback Rule |
|---|---|---:|---|---|---|---|
| openFDA | Official API | 1 | MVP v1 | Drug labels, recalls, adverse events, NDC, device/food datasets where relevant | Low | If endpoint unavailable, log source health event |
| FDA RSS / What's New pages | Official RSS / official page | 2 | MVP v1 | Recent regulatory updates, announcements, drug updates | Low to Medium | Use official page parser only if RSS is insufficient |
| FDA Guidance Search / Guidance Documents | Official structured search / official HTML | 3 | MVP v1 | Draft and final guidance tracking | Medium | Parser must validate dates, titles, document links, and attachment links |
| FDA PDF / attachment links | Official downloadable file | 4 | MVP v1 | Guidance PDF, supporting documents, official attachments | Medium | Record file metadata and download status |
| Non-official FDA summaries | Supplementary source | 99 | Not primary | Background only | High | Do not use as primary evidence |

### 5.2 TFDA

| Source | Type | Priority | Phase | Intended Use | Risk Level | Fallback Rule |
|---|---|---:|---|---|---|---|
| TFDA DataAction API / official data endpoints | Official API / open data | 1 | MVP v1 | TFDA news, announcements, and structured public data where available | Low to Medium | If endpoint schema changes, log source health event |
| data.gov.tw TFDA datasets | Official open data portal | 2 | MVP v1 | Taiwan clinical trial and regulatory datasets | Low to Medium | Validate dataset format and update date |
| TFDA RSS | Official RSS | 3 | MVP v1 | Update detection and monitoring | Low to Medium | Use official page parser only if RSS is insufficient |
| TFDA official announcement pages | Official HTML | 4 | MVP v1 | Regulatory announcements not available through API/RSS | Medium | Parser must include empty result and selector validation |
| Non-official Taiwan regulatory summaries | Supplementary source | 99 | Not primary | Background only | High | Do not use as primary evidence |

### 5.3 ClinicalTrials.gov

| Source | Type | Priority | Phase | Intended Use | Risk Level | Fallback Rule |
|---|---|---:|---|---|---|---|
| ClinicalTrials.gov API v2 | Official API | 1 | MVP v1 | Trial search, study details, sponsor, phase, status, outcomes, results availability | Low | If API fails, log source health event; do not replace with unofficial trial databases |
| ClinicalTrials.gov study page | Official HTML | 2 | MVP v1 fallback | Human-readable verification only | Medium | Do not use as primary extraction source unless API data is unavailable |
| Third-party clinical trial databases | Supplementary source | 99 | Not primary | Background only | High | Do not use as primary evidence unless explicitly approved |

---

## 6. v2 Source Matrix

### 6.1 EMA

| Source | Type | Priority | Phase | Intended Use | Risk Level | Fallback Rule |
|---|---|---:|---|---|---|---|
| EMA RSS feeds | Official RSS | 1 | v2 | Recent EMA news, updates, and announcements | Low | If RSS unavailable, use official EMA update pages |
| EMA medicine data downloads | Official downloadable dataset | 2 | v2 | Medicine-level structured information and regulatory status | Low to Medium | Validate file format and update date |
| EMA scientific guideline pages | Official HTML | 3 | v2 | Human medicines scientific guidelines and regulatory guidance | Medium | Parser must validate title, date, status, and document links |
| EMA PDF / attachment links | Official downloadable file | 4 | v2 | Guideline PDFs, reflection papers, procedural documents | Medium | Record file metadata and parent page |
| Non-official EMA summaries | Supplementary source | 99 | Not primary | Background only | High | Do not use as primary evidence |

---

## 7. v3 Source Matrix

### 7.1 NMPA / CDE

| Source | Type | Priority | Phase | Intended Use | Risk Level | Fallback Rule |
|---|---|---:|---|---|---|---|
| NMPA official pages | Official HTML | 1 | v3 | Regulatory notices, official announcements, policy updates | Medium to High | Parser must include strong source health checks |
| CDE official pages | Official HTML | 2 | v3 | Technical guidelines, drug review notices, CDE updates | Medium to High | Parser must validate title, publication date, attachment links, and Chinese text encoding |
| NMPA / CDE downloadable files | Official downloadable file | 3 | v3 | PDF, Word, Excel, and other official attachments | Medium to High | Record file type, file hash, and download status |
| Non-official China regulatory summaries | Supplementary source | 99 | Not primary | Background only | High | Do not use as primary evidence |

### 7.2 PMDA

| Source | Type | Priority | Phase | Intended Use | Risk Level | Fallback Rule |
|---|---|---:|---|---|---|---|
| PMDA RSS feeds | Official RSS | 1 | v3 | Recent PMDA updates and notifications | Low to Medium | If RSS unavailable, use official PMDA What's New page |
| PMDA What's New pages | Official HTML | 2 | v3 | Update detection and official notices | Medium | Parser must validate title, date, and links |
| PMDA review / approved product pages | Official HTML / downloadable file | 3 | v3 | Approved products, review information, product-specific regulatory documents | Medium | Parser must preserve source URL and attachment metadata |
| PMDA PDF / attachment links | Official downloadable file | 4 | v3 | Review reports, safety updates, official documents | Medium | Record file metadata and parent source page |
| Non-official Japan regulatory summaries | Supplementary source | 99 | Not primary | Background only | High | Do not use as primary evidence |

---

## 8. Later or Optional Sources

The following sources are not part of MVP v1 unless explicitly approved.

| Source | Type | Suggested Phase | Intended Use | Restriction |
|---|---|---|---|---|
| WHO ICTRP | Official international registry portal | Future | Cross-registry clinical trial discovery | Supplement ClinicalTrials.gov, do not replace it |
| EU CTIS / EU clinical trial sources | Official EU trial source | Future | EU trial tracking | Implement only after ClinicalTrials.gov workflow is stable |
| Literature databases | Academic / literature source | Future | Scientific publication context | Not a regulatory primary source |
| Patent databases | Patent source | Future | Patent intelligence | Out of current scope |
| Commercial drug intelligence platforms | Commercial source | Future | Market and competitive intelligence | Out of current scope unless explicitly approved |

---

## 9. Fallback Rule

Fallback sources are allowed only when higher-priority official sources are unavailable, incomplete, or unsuitable for the specific data field.

Fallback implementation must follow these rules:

1. Document why fallback is needed.
2. Preserve the original official URL.
3. Add parser validation.
4. Add source health checks.
5. Avoid treating fallback-derived fields as higher quality than API-derived fields.
6. Clearly mark the source type in the normalized record.

Fallback use must not silently change the meaning of a record.

---

## 10. Source Health Trigger Rule

A source health event must be generated when any of the following occurs:

1. API request fails repeatedly.
2. API response schema changes.
3. RSS feed becomes unavailable.
4. RSS response contains no items unexpectedly.
5. HTML parser returns zero results unexpectedly.
6. Required fields are missing, such as title, date, official URL, or document link.
7. Attachment download fails.
8. File hash changes unexpectedly.
9. DOM structure or selector behavior changes.
10. Retrieved data volume is significantly lower or higher than expected.
11. Date parsing fails.
12. Character encoding causes corrupted text.
13. Duplicate records increase unexpectedly.
14. A source has not been successfully checked within the expected interval.

Each source health event should include:

- Source ID
- Agency or registry
- Endpoint or page URL
- Failure type
- Detection time
- Last successful check time, if available
- Error message
- Suggested connector or parser file to review
- Suggested severity

---

## 11. Restricted and Do-Not-Use Sources

The following sources must not be used as primary evidence:

1. Blog posts
2. Law firm summaries
3. Consulting firm summaries
4. Commercial database previews
5. News articles
6. Social media posts
7. Search engine snippets
8. AI-generated summaries
9. Reposted PDFs without official source confirmation
10. Unofficial translated versions without official source confirmation

These may be used only as supplementary context when explicitly requested, and the official source must still be preferred.

---

## 12. Connector Creation Rule

A new connector may be created only if:

1. The source is listed in this matrix.
2. The implementation phase allows it.
3. The source type and priority are clear.
4. Expected fields are defined.
5. Source health behavior is defined.
6. Tests can be written for normal and failure cases.

Do not create a new connector only because a webpage appears useful.

---

## 13. MCP and Claude Use Rule

Claude-facing MCP tools should query normalized, source-governed data.

Claude should not bypass this matrix by directly scraping agency websites during normal project execution.

The MCP layer should preserve enough source metadata for Claude to produce traceable outputs, including:

- Agency or registry
- Source URL
- Publication date or update date
- Retrieval date
- Source type
- Attachment links, if available
- Known source limitations

---

## 14. Maintenance Rule

This document must be updated before any of the following changes are made:

1. Adding a new agency
2. Adding a new registry
3. Adding a new source endpoint
4. Adding a new fallback source
5. Changing a source priority
6. Promoting a supplementary source to primary use
7. Moving a source from a later phase into MVP v1
8. Deprecating a source
9. Changing the source health expectation for a source

If this document conflicts with code, this document governs source selection and priority.

If this document conflicts with `PROJECT_INSTRUCTION.md`, `PROJECT_INSTRUCTION.md` governs the overall project scope and phase boundary.

---

## 15. Current Build Instruction

For the current build stage, implement only MVP v1 sources:

```text
FDA
TFDA
ClinicalTrials.gov
```

Do not implement EMA, NMPA / CDE, PMDA, WHO ICTRP, EU CTIS, literature, patent, or commercial intelligence sources until the user explicitly approves moving to the next phase.

