# Source Expansion Feasibility Matrix — EMA / NMPA / PMDA

## Purpose

This document evaluates whether EMA, NMPA/CDE, and PMDA should be considered for future source expansion beyond the current MVP v1 scope.

This is a docs/spec-only feasibility matrix. It does not approve or implement new connectors, runtime sources, MCP tools, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, `.mcp.json`, GitHub automation, company alias database, corporate-family mapping, product ownership inference, literature/patent/finance/news integration, or CMC weekly report work.

## Current Runtime Scope Remains Unchanged

Approved MVP v1 active sources remain:

```text
FDA
TFDA
ClinicalTrials.gov
```

EMA, NMPA/CDE, and PMDA remain candidate post-MVP sources only.

## Execution Discipline Guardrail

When the user explicitly states that a PR has already been confirmed or merged, do not repeatedly block progress by asking for the same confirmation again. For repository-changing work, perform a single verification pass when needed, then proceed with the next approved step.

## Evidence Basis

Survey date: 2026-06-10

Primary evidence reviewed:

| Agency | Official source evidence reviewed | Notes |
|---|---|---|
| EMA | `https://www.ema.europa.eu/en/news-events/rss-feeds` | EMA provides RSS feeds for news, public consultations, regulatory/procedural guidelines, scientific guidelines, EPARs, inspections, and other categories. |
| EMA | `https://www.ema.europa.eu/en/medicines/download-medicine-data` | EMA provides downloadable medicine data tables and states that website data is available in JSON format for automated use. |
| NMPA / CDE | `https://english.nmpa.gov.cn/` | English NMPA site provides news, drugs, regulatory information, laws/regulations, policies interpretation, database, and links to affiliated institutions including CDE. |
| NMPA / CDE | `https://www.cde.org.cn/` | CDE site provides policy/law/guideline sections, public information, accepted products, priority review, breakthrough therapy, implied clinical trial permission, marketed drug information, and rolling dated notices. |
| PMDA | `https://www.pmda.go.jp/english/` | PMDA English site provides What's new, RSS icons/feeds, review-related services, safety information, approved product information, and regulatory information sections. |
| PMDA | `https://www.pmda.go.jp/english/review-services/reviews/approved-information/drugs/0002.html` | PMDA provides list of approved products and links to review reports for drugs and other product categories. |
| PMDA | `https://www.pmda.go.jp/english/review-services/regulatory-info/0002.html` | PMDA provides regulatory information and early consideration links grouped by topic, area, procedure, and approved product information. |

## Feasibility Summary

| Agency | Feasibility rating | Best initial source type | Primary value | Main blocker | Recommendation |
|---|---:|---|---|---|---|
| EMA | High | RSS + downloadable tables + JSON website data | Strong fit for regulatory updates, medicines data, EPARs, guidelines, consultations, and date-based monitoring. | Need controlled mapping between EMA categories and current internal normalized fields. | Best first candidate for a future source-expansion pilot, after explicit approval. |
| NMPA / CDE | Medium | CDE official pages + NMPA English/Chinese pages | Important for China drug review updates, guidance principles, registration/public review information, and biologics-related policy signals. | No confirmed stable public API/RSS in this review; Chinese-language parsing and page-structure variability require extra source-health design. | Feasible as docs/planning next; runtime connector should wait for source-access and parser validation. |
| PMDA | Medium to high | PMDA English What's new/RSS + approved products + review reports + regulatory information pages | Useful for Japan review reports, approved products, safety updates, regulatory information, and new modalities. | Some content is page/PDF/Excel-oriented; English pages may lag or be partial relative to Japanese pages. | Feasible after EMA or in parallel as a lower-complexity read-only metadata source. |

## Agency-Level Feasibility Matrix

### EMA

| Dimension | Finding | Feasibility interpretation |
|---|---|---|
| Official update feed | EMA provides RSS feeds across categories including news, public consultations, regulatory/procedural guidelines, scientific guidelines, EPARs, inspections, and others. | Strong candidate for date-window regulatory update tracking. |
| Structured data | EMA download page states data tables are available and automatically updated overnight; the page also states that the website is available in JSON format for automated use. | Strong candidate for structured metadata ingestion after schema review. |
| Product / medicine data | Downloadable tables cover approved medicines, withdrawn applications, status of opinions, post-authorisation procedures, referrals, PIPs, orphan designations, PSUSAs, DHPCs, shortages, and related medicine data. | Strong fit for medicine-level metadata and regulatory-event tracking. |
| Guidance coverage | EMA RSS categories include regulatory/procedural and scientific guidelines. | Strong fit for the original guidance-tracking requirement. |
| Modality coverage | Likely feasible through medicine metadata and guideline categories, but product modality mapping must be validated against current taxonomy. | Requires mapping test before connector approval. |
| Date-window support | RSS and download tables contain update/publication signals; exact field-level handling must be validated. | Likely feasible. |
| Access risk | Official RSS/JSON/table routes appear designed for automated access. | Lower access risk than scraping-only sites. |
| Recommended status | Candidate 1 for source expansion feasibility follow-up. | Do not implement until explicit approval. |

### NMPA / CDE

| Dimension | Finding | Feasibility interpretation |
|---|---|---|
| Official update feed | CDE home page exposes dated rolling notices and sections for policy/law/guidelines, news, public information, accepted products, priority review, breakthrough therapy, implied clinical trial permission, and marketed drug information. | Useful, but source structure needs parser and source-health validation. |
| English access | NMPA English site exposes News, Drugs, Resources, Database, Laws & Regulations, Regulatory Information, Policies Interpretation, and links to CDE. | Useful for high-level English monitoring, but likely incomplete compared with Chinese sources. |
| Structured data | Public pages and database links exist, but this review did not confirm a stable public API/RSS route suitable for immediate connector work. | Medium feasibility; needs technical source-discovery work before implementation. |
| Guidance coverage | CDE includes `指导原则` and policy interpretation sections. | Strong content relevance for China regulatory/guidance tracking. |
| Product / review data | CDE lists accepted product information, review task disclosure, priority review, breakthrough therapy, implied clinical trial permission, marketed drug information, and other public categories. | Strong relevance, but normalization and translation issues are likely. |
| Modality coverage | Biologics and cell/gene-related guidance can appear in notices/guidance, but modality classification would require Chinese-language term mapping. | Requires controlled bilingual taxonomy and validation. |
| Date-window support | Many CDE notices expose dates in `YYYYMMDD` form. | Feasible if page structure is stable. |
| Access risk | Public pages are official, but automated access terms/API stability are not yet confirmed. | Medium risk; do not scrape aggressively. |
| Recommended status | Candidate 2, but only after a controlled source-access / parser feasibility check. | Do not implement until explicit approval. |

### PMDA

| Dimension | Finding | Feasibility interpretation |
|---|---|---|
| Official update feed | PMDA English site exposes dated What's new entries, category filters, and RSS icons/feeds for updates. | Good candidate for date-window update tracking. |
| Product / review data | PMDA provides pages for approved products and review reports across drugs, medical devices, regenerative medical products, and related categories. | Strong relevance for approval/review-report monitoring. |
| Regulatory guidance | PMDA regulatory information page links to key guidance, early consideration, review topics, clinical trials, quality, vaccines/blood products, biosimilars, regenerative/gene therapy, and related areas. | Strong fit for guidance/topic tracking. |
| Structured data | This review found page/PDF/Excel-style public content, but did not confirm a stable public JSON/API route comparable to EMA. | Medium feasibility; connector design would need careful page/PDF handling rules. |
| English coverage | PMDA English pages exist and include review reports and regulatory information, but PMDA warns machine translation may not be accurate and files may not be translated. | English feed can be useful, but official Japanese source parity may require later review. |
| Modality coverage | Pages include drugs, regenerative medical products, biosimilars, radiopharmaceuticals, new modalities, NAMs, vaccines/blood products, and gene therapy-related categories. | Feasible with mapping. |
| Date-window support | What's new entries expose dates and categories. | Feasible for update monitoring. |
| Access risk | Official pages and RSS signals appear accessible, but content formats vary. | Medium risk. |
| Recommended status | Candidate 2 or 3 after EMA; useful for read-only metadata and review-report tracking. | Do not implement until explicit approval. |

## Proposed Source Expansion Decision Gate

Before any EMA, NMPA/CDE, or PMDA runtime work is approved, require all of the following:

1. Confirm exact official source URLs and allowed use pattern.
2. Confirm whether RSS, JSON, table download, or API-like data access exists.
3. Confirm update-date and publication-date fields.
4. Confirm source health behavior for empty results, unavailable pages, and parser changes.
5. Define normalized fields that map into the current data dictionary.
6. Define modality mapping and bilingual term handling where needed.
7. Define expected date-window behavior from 1 month to 5 years.
8. Confirm test strategy with mocked/offline examples before live-source tests.
9. Confirm that any new connector is explicitly approved by the user.
10. Confirm no `.mcp.json`, scheduler, alerts, dashboard, persistence, HTTP/SSE, or GitHub automation is introduced without separate approval.

## Recommended Expansion Order

Recommended order if the user later approves expansion planning:

```text
1. EMA feasibility deepening: RSS + JSON/table schema review.
2. PMDA feasibility deepening: What's new/RSS + review reports + regulatory information mapping.
3. NMPA/CDE feasibility deepening: source-access, Chinese-language parser, and bilingual taxonomy validation.
```

Rationale:

- EMA has the clearest automated-use signal because the official site exposes RSS categories, downloadable tables, and JSON website data.
- PMDA has useful English update and review-report pages but may require mixed HTML/PDF/Excel handling.
- NMPA/CDE is highly relevant but likely requires the most bilingual normalization and parser-stability work.

## MVP Impact Assessment

| Area | Impact if only this document is added |
|---|---|
| Runtime code | None |
| MCP tools | None |
| Active sources | None |
| Tests | README index only |
| User workflow | Provides a decision basis for source expansion approval |
| Risk | Low, because no source connector or automation is introduced |

## Recommended Next Workstream After This Matrix

If this PR is accepted, the next safe step should be one of:

1. State sync after this feasibility matrix.
2. EMA-only schema review document, still docs/spec-only.
3. PMDA-only schema review document, still docs/spec-only.
4. NMPA/CDE source-access feasibility note, still docs/spec-only.

Do not implement any connector until the user explicitly approves a specific source, source type, normalized fields, and validation plan.

## Explicit Non-Goals

This PR does not authorize:

- EMA connector implementation.
- NMPA/CDE connector implementation.
- PMDA connector implementation.
- Runtime source expansion.
- New MCP tools.
- New dependencies.
- `.mcp.json` changes.
- Scheduler, alerts, dashboard, persistence, HTTP/SSE transport, or GitHub automation.
- Literature, patent, finance, or news integration.
- Company alias database, corporate-family mapping, or product ownership inference.
- CMC weekly management report template.
