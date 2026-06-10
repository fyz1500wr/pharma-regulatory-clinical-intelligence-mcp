# Source And Guidance Expansion Feasibility Matrix — EMA / NMPA / PMDA / ICH

## Purpose

This document evaluates whether EMA, NMPA/CDE, PMDA, and ICH should be considered for future expansion beyond the current MVP v1 source scope.

This is a docs/spec-only feasibility matrix. It does not approve or implement new connectors, runtime sources, MCP tools, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, `.mcp.json`, GitHub automation, company alias database, corporate-family mapping, product ownership inference, literature/patent/finance/news integration, or CMC weekly report work.

## Current Runtime Scope Remains Unchanged

Approved MVP v1 active sources remain:

```text
FDA
TFDA
ClinicalTrials.gov
```

EMA, NMPA/CDE, PMDA, and ICH remain candidate post-MVP sources only.

## Important Classification Distinction

EMA, NMPA/CDE, and PMDA are regulatory agency / regulator-linked sources.

ICH is different. ICH should be classified as a global harmonisation guidance source, not as a drug-review agency and not as a clinical trial registry.

This distinction matters because ICH guidance should not be forced into the same source model as agency approval, review report, or trial registry sources. A future ICH integration would most likely use a dedicated guidance-source profile.

## Execution Discipline Guardrail

When the user explicitly states that a PR has already been confirmed or merged, do not repeatedly block progress by asking for the same confirmation again. For repository-changing work, perform a single verification pass when needed, then proceed with the next approved step.

## Evidence Basis

Survey date: 2026-06-10

Primary evidence reviewed:

| Source | Official source evidence reviewed | Notes |
|---|---|---|
| EMA | `https://www.ema.europa.eu/en/news-events/rss-feeds` | EMA provides RSS feeds for news, public consultations, regulatory/procedural guidelines, scientific guidelines, EPARs, inspections, and other categories. |
| EMA | `https://www.ema.europa.eu/en/medicines/download-medicine-data` | EMA provides downloadable medicine data tables and states that website data is available in JSON format for automated use. |
| NMPA / CDE | `https://english.nmpa.gov.cn/` | English NMPA site provides news, drugs, regulatory information, laws/regulations, policy interpretation, database, and links to affiliated institutions including CDE. |
| NMPA / CDE | `https://www.cde.org.cn/` | CDE site provides policy/law/guideline sections, public information, accepted products, priority review, breakthrough therapy, implied clinical trial permission, marketed drug information, and rolling dated notices. |
| PMDA | `https://www.pmda.go.jp/english/` | PMDA English site provides What's new, RSS icons/feeds, review-related services, safety information, approved product information, and regulatory information sections. |
| PMDA | `https://www.pmda.go.jp/english/review-services/reviews/approved-information/drugs/0002.html` | PMDA provides list of approved products and links to review reports for drugs and other product categories. |
| PMDA | `https://www.pmda.go.jp/english/review-services/regulatory-info/0002.html` | PMDA provides regulatory information and early consideration links grouped by topic, area, procedure, and approved product information. |
| ICH | `https://www.ich.org/` | ICH is the official source for harmonised international technical requirements and guidelines. |
| ICH | `https://www.ich.org/page/ich-guidelines` | ICH guidelines are grouped by topic families such as Quality, Safety, Efficacy, Multidisciplinary, and Implementation. |
| ICH | `https://www.ich.org/page/quality-guidelines` | ICH Quality guidelines are highly relevant to CMC, analytical, stability, quality risk, pharmaceutical development, and lifecycle topics. |

## Feasibility Summary

| Source | Source class | Feasibility rating | Best initial source type | Primary value | Main blocker | Recommendation |
|---|---|---:|---|---|---|---|
| EMA | Regulatory agency | High | RSS + downloadable tables + JSON website data | Strong fit for regulatory updates, medicines data, EPARs, guidelines, consultations, and date-based monitoring. | Need controlled mapping between EMA categories and current internal normalized fields. | Best first candidate for a future agency-source pilot, after explicit approval. |
| ICH | Global harmonisation guidance source | High | Guidelines pages + topic-family pages + news/update pages | Strong fit for guidance tracking, CMC/quality intelligence, and cross-agency harmonised requirements. | Needs a guidance-source profile distinct from agency approval/review sources. | Best first candidate for a future guidance-source pilot, after explicit approval. |
| PMDA | Regulatory agency | Medium to high | PMDA English What's new/RSS + approved products + review reports + regulatory information pages | Useful for Japan review reports, approved products, safety updates, regulatory information, and new modalities. | Some content is page/PDF/Excel-oriented; English pages may lag or be partial relative to Japanese pages. | Feasible after EMA or in parallel as a lower-complexity read-only metadata source. |
| NMPA / CDE | Regulatory agency / review center | Medium | CDE official pages + NMPA English/Chinese pages | Important for China drug review updates, guidance principles, registration/public review information, and biologics-related policy signals. | No confirmed stable public API/RSS in this review; Chinese-language parsing and page-structure variability require extra source-health design. | Feasible as docs/planning next; runtime connector should wait for source-access and parser validation. |

## Source-Level Feasibility Matrix

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
| Recommended status | Candidate 1 for agency-source expansion feasibility follow-up. | Do not implement until explicit approval. |

### ICH

| Dimension | Finding | Feasibility interpretation |
|---|---|---|
| Source class | ICH is a global harmonisation body for technical requirements and guidance, not a marketing-authorisation agency. | Requires a guidance-source profile, not an agency-review profile. |
| Official guideline source | ICH provides official guideline pages and topic-family groupings including Quality, Safety, Efficacy, Multidisciplinary, and Implementation. | Strong fit for official guidance tracking. |
| CMC relevance | Quality guidelines cover highly relevant CMC topics such as stability, analytical validation, pharmaceutical development, quality risk management, lifecycle, impurities, and related quality topics. | High value for PM/RA/CMC intelligence use. |
| Update detection | ICH guideline pages and news/update content can support monitoring of new, revised, adopted, draft, and consultation-stage guidelines if fields are mapped carefully. | Feasible, but update-stage normalization must be designed. |
| Date-window support | Guideline status, revision history, and news/update pages may provide date signals, but exact source-specific fields need source review. | Feasible after schema review. |
| Structured data | This review did not confirm a stable public JSON/API/RSS route comparable to EMA. | Treat as official webpage/PDF metadata source until proven otherwise. |
| Modality coverage | ICH is generally topic-based rather than product-modality-based; modality relevance must be inferred from guideline topic and scope. | Requires controlled guidance-topic mapping, not product ownership inference. |
| Access risk | Official public pages are available, but automated use pattern and page stability should be confirmed before connector work. | Low to medium risk. |
| Recommended status | Candidate 1 for guidance-source expansion feasibility follow-up. | Do not implement until explicit approval. |

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

## Proposed Source And Guidance Expansion Decision Gate

Before any EMA, NMPA/CDE, PMDA, or ICH runtime work is approved, require all of the following:

1. Confirm exact official source URLs and allowed use pattern.
2. Confirm whether RSS, JSON, table download, or API-like data access exists.
3. Confirm update-date and publication-date fields.
4. Confirm source health behavior for empty results, unavailable pages, and parser changes.
5. Define normalized fields that map into the current data dictionary.
6. Define whether the source is an agency-review source, guidance-source, product/medicine-data source, or clinical-registry source.
7. Define modality mapping and bilingual term handling where needed.
8. Define expected date-window behavior from 1 month to 5 years.
9. Confirm test strategy with mocked/offline examples before live-source tests.
10. Confirm that any new connector is explicitly approved by the user.
11. Confirm no `.mcp.json`, scheduler, alerts, dashboard, persistence, HTTP/SSE, or GitHub automation is introduced without separate approval.

## Recommended Expansion Order

Recommended order if the user later approves expansion planning:

```text
1. ICH guidance-source schema review: guideline families, stages, revision dates, and official links.
2. EMA agency-source schema review: RSS + JSON/table schema review.
3. PMDA agency-source schema review: What's new/RSS + review reports + regulatory information mapping.
4. NMPA/CDE agency-source schema review: source-access, Chinese-language parser, and bilingual taxonomy validation.
```

Rationale:

- ICH has high value and should be treated as guidance-source expansion rather than agency-source expansion.
- EMA has the clearest automated-use signal for agency expansion because the official site exposes RSS categories, downloadable tables, and JSON website data.
- PMDA has useful English update and review-report pages but may require mixed HTML/PDF/Excel handling.
- NMPA/CDE is highly relevant but likely requires the most bilingual normalization and parser-stability work.

## Architecture Impact Assessment

Adding ICH changes the future architecture classification more than it changes runtime scope.

| Area | Impact if only this document is added |
|---|---|
| Runtime code | None |
| MCP tools | None |
| Active sources | None |
| Tests | README index only |
| Source taxonomy | Adds need to distinguish agency sources from global harmonisation guidance sources. |
| Data model planning | Adds future need for guideline family, guideline stage/status, revision/adoption date, and implementation topic fields. |
| User workflow | Provides a decision basis for source/guidance expansion approval. |
| Risk | Low, because no source connector or automation is introduced. |

## Recommended Next Workstream After This Matrix

If this PR is accepted, the next safe step should be one of:

1. State sync after this feasibility matrix.
2. ICH-only guidance-source schema review document, still docs/spec-only.
3. EMA-only agency-source schema review document, still docs/spec-only.
4. PMDA-only agency-source schema review document, still docs/spec-only.
5. NMPA/CDE source-access feasibility note, still docs/spec-only.

Do not implement any connector until the user explicitly approves a specific source, source type, normalized fields, and validation plan.

## Explicit Non-Goals

This PR does not authorize:

- EMA connector implementation.
- NMPA/CDE connector implementation.
- PMDA connector implementation.
- ICH connector implementation.
- Runtime source or guidance expansion.
- New MCP tools.
- New dependencies.
- `.mcp.json` changes.
- Scheduler, alerts, dashboard, persistence, HTTP/SSE transport, or GitHub automation.
- Literature, patent, finance, or news integration.
- Company alias database, corporate-family mapping, or product ownership inference.
- CMC weekly management report template.
