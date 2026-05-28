# Post-MVP Source Expansion Decision Matrix

## Purpose

This document defines a practical decision gate for evaluating whether a new source should be added after MVP v1.

It is intentionally conservative.

The goal is to prevent the project from expanding into a broad, hard-to-maintain intelligence platform that tries to cover everything but becomes less useful for real regulatory and clinical work.

This document does not select the next source.

It does not authorize source expansion.

It only defines how future source expansion requests should be evaluated.

---

## Default Position: Do Not Expand by Default

The default post-MVP position is:

```text
Do not add a new source unless it solves a defined recurring user workflow or decision-support need.
```

A source should not be added only because it is important, interesting, available, or commonly referenced.

A source should be considered only when it supports a clear use case such as:

- regulatory update tracking for a defined region
- clinical trial landscape review for a defined registry gap
- source-backed project follow-up work
- recurring management or PM intelligence summaries
- documented regulatory or clinical review workflows

If the use case is unclear, the source should remain out of scope.

---

## Current MVP v1 Baseline

MVP v1 active sources are limited to:

- FDA
- TFDA
- ClinicalTrials.gov

MVP v1 should not be expanded casually into:

- EMA
- NMPA / CDE
- PMDA
- WHO ICTRP
- EU CTIS
- literature
- patents
- finance data
- commercial intelligence
- broad web or news crawling
- internal database persistence
- scheduler or alerting workflows
- automated GitHub issue creation
- advanced report generation

Any source expansion should be handled as a separate approved post-MVP phase.

---

## Source Expansion Evaluation Criteria

Evaluate each proposed source using practical criteria.

| Criterion | Review question |
|---|---|
| User workflow fit | Does this source support a real recurring workflow? |
| Scope fit | Does it fit regulatory or clinical intelligence rather than general business intelligence? |
| Officialness / reliability | Is it an official or high-reliability source? |
| Unique value | Does it add information not already covered by MVP v1 sources? |
| Access feasibility | Is there a stable API, RSS feed, download page, or reliably structured public source? |
| Maintenance burden | Can the source be maintained without excessive scraping, manual repair, or frequent parser breakage? |
| Output interpretability | Can outputs be interpreted conservatively without encouraging unsupported conclusions? |
| Field usefulness | Does the source provide fields that are actually useful for downstream review? |
| Validation feasibility | Can outputs be tested with predictable smoke tests or fixtures? |
| Human review path | Are official URLs or source records available for manual verification? |

Do not add a source if it scores well on interest but poorly on workflow fit, access feasibility, or maintenance burden.

---

## Simple Scoring Matrix

Use a simple 0-2 score for each criterion.

```text
0 = not suitable / unclear / high risk
1 = potentially useful but not ready or not clearly prioritized
2 = clearly useful, scope-aligned, and feasible to maintain
```

Suggested scoring criteria:

| Criterion | Score 0 | Score 1 | Score 2 |
|---|---|---|---|
| User workflow fit | No defined workflow | Occasional use only | Recurring practical workflow |
| Scope fit | Outside regulatory/clinical scope | Adjacent but not core | Core regulatory/clinical scope |
| Source reliability | Unofficial or unclear | Mixed reliability | Official or high-reliability |
| Unique value | Duplicates existing sources | Some incremental value | Clear unique value |
| Access feasibility | Unstable scraping only | Possible but fragile | API/RSS/download/stable structure |
| Maintenance burden | High burden | Moderate burden | Low to moderate burden |
| Interpretability | High over-inference risk | Manageable with caveats | Conservative interpretation is practical |
| Validation feasibility | Hard to test | Partially testable | Smoke-testable and fixture-friendly |
| Manual verification | No clear official URL | Some source traceability | Strong official URL/source traceability |

Suggested decision thresholds:

| Total score | Decision |
|---|---|
| 0-8 | Do not add. |
| 9-12 | Keep in backlog only. Revisit when workflow is clearer. |
| 13-15 | Consider scoped design note before implementation. |
| 16-18 | Candidate for a small approved post-MVP source expansion PR. |

The score should not override judgment. A source with very high maintenance burden or poor reliability should not be added even if the total score looks acceptable.

---

## Candidate Source Categories

This section lists possible future categories only.

It does not approve implementation.

### Regulatory agency sources

Possible candidates:

- EMA
- NMPA / CDE
- PMDA

Potential value:

- regional regulatory update tracking
- cross-agency comparison
- product modality or CMC-related intelligence

Primary risk:

- source parsing complexity
- language and terminology differences
- over-interpreting agency differences as final regulatory divergence

### Clinical trial registry sources

Possible candidates:

- EU CTIS
- WHO ICTRP

Potential value:

- broader clinical trial registry coverage
- regional trial visibility beyond ClinicalTrials.gov

Primary risk:

- registry duplication
- inconsistent sponsor naming
- inconsistent status and phase fields
- false sense of global completeness

### Evidence support sources

Possible candidates:

- literature databases
- patents

Potential value:

- technical or evidence context for later phases

Primary risk:

- large scope expansion
- copyright or access restrictions
- weak linkage to official regulatory/clinical source outputs
- increased risk of unsupported scientific, commercial, or IP conclusions

### Sources to avoid unless separately approved

Avoid adding these to this project by default:

- finance data
- stock market data
- commercial intelligence
- sales forecasts
- market share databases
- broad news crawling
- general competitor intelligence
- social media signals

These may be useful in another project, but they are not part of the core regulatory and clinical intelligence MVP.

---

## Recommended Priority Logic

Use this priority logic before proposing any source expansion.

### Priority 1: Strengthen existing MVP use cases

Prefer improvements that make FDA, TFDA, and ClinicalTrials.gov outputs more useful and safer.

Examples:

- better examples
- better caveats
- clearer output review workflows
- stronger tests
- clearer source behavior documentation

### Priority 2: Fill a defined regulatory or clinical gap

Only consider a new source when a specific workflow needs it.

Examples:

- a project needs EU regulatory tracking before EMA is considered
- a project needs China regulatory tracking before NMPA / CDE is considered
- a project needs Japan regulatory tracking before PMDA is considered
- a project needs EU trial registry coverage before EU CTIS is considered

### Priority 3: Add only one source at a time

Do not add multiple agencies or registries in one PR.

Each source expansion should include:

- a source-specific design note
- minimal connector implementation
- smoke tests
- limitations and caveats
- usage examples
- source health behavior where applicable

### Priority 4: Defer broad evidence intelligence

Literature, patents, and advanced evidence synthesis should remain deferred unless a separate phase is approved.

These areas can grow quickly and should not be mixed into the core MVP casually.

---

## Source Expansion Request Template

Use this template before proposing a new source.

```text
Proposed source:

Source category:
- Regulatory agency
- Clinical trial registry
- Evidence support
- Other

User workflow supported:

Why current MVP v1 sources are insufficient:

Expected users:

Official source URL or access path:

Access method:
- API
- RSS
- Download
- Structured web page
- Manual-only
- Other

Expected output fields:

Official URL or manual verification path:

Expected update frequency:

Maintenance burden:
- Low
- Moderate
- High

Over-inference risks:

Required caveats:

Testing approach:

Recommended decision:
- Do not add
- Backlog only
- Design note first
- Candidate for scoped implementation PR
```

A source should not move to implementation unless this template is filled with a clear use case.

---

## Do Not Add a Source If

Do not add a source if any of the following are true:

- no recurring user workflow needs it
- it only satisfies curiosity
- it duplicates existing MVP v1 outputs without clear added value
- it requires unstable scraping as the only access method
- official source traceability is weak
- outputs cannot be tested or smoke-checked reasonably
- it encourages unsupported approval probability conclusions
- it encourages unsupported company superiority conclusions
- it shifts the project into finance, market intelligence, sales forecasting, or broad competitor intelligence
- it requires large architecture changes before there is a clear user need
- it would make the project harder to use for the core regulatory/clinical workflows

When in doubt, do not add the source.

Add a backlog note instead.

---

## Required Pre-Implementation Questions

Before any source implementation PR, answer:

1. What exact user workflow will this source support?
2. What current MVP limitation does it solve?
3. What is the smallest useful version of this source integration?
4. What fields will be returned?
5. What official URL or verification path will be preserved?
6. What limitations must be shown to the user?
7. What smoke tests are required?
8. What will explicitly remain out of scope?
9. How will the source affect existing tool outputs?
10. Could this be handled with documentation or manual workflow instead of a connector?

If these questions cannot be answered clearly, do not implement the source.

---

## Minimal Approval Gate

A post-MVP source expansion should require explicit approval on all of the following:

- source name
- exact workflow supported
- scope of first implementation
- output fields
- known limitations
- testing approach
- what is explicitly out of scope

Suggested approval statement:

```text
Approve adding [SOURCE] for [WORKFLOW] only, with MVP fields [FIELDS], official URL preservation, known limitations, and smoke tests. Do not expand into unrelated sources or advanced analysis.
```

---

## Safe Decision Outcomes

Use one of these decision outcomes after evaluating a source.

### Outcome 1: Do not add

Use when the source is interesting but not needed.

```text
Do not add this source. No recurring workflow or clear decision-support need has been defined.
```

### Outcome 2: Backlog only

Use when the source may be useful later but is not ready.

```text
Keep this source in the backlog. Revisit when a specific workflow, output fields, and maintenance approach are defined.
```

### Outcome 3: Design note first

Use when the source is likely useful but implementation risk needs review.

```text
Create a source-specific design note before implementation. Do not build the connector yet.
```

### Outcome 4: Scoped implementation candidate

Use only when the source is clearly useful, feasible, and approved.

```text
Proceed with a small scoped implementation PR for this source only. Do not bundle other sources or advanced analysis.
```

---

## Relationship to Existing Documentation

Use this document with:

| Document | Main use |
|---|---|
| `docs/mvp_v1_completion_note.md` | Records the MVP v1 baseline and active scope. |
| `docs/mcp_usage_examples.md` | Shows safe practical usage examples for current tools. |
| `docs/sample_prompts.md` | Provides copy-paste prompts within MVP v1 boundaries. |
| `docs/tool_output_review_checklist.md` | Helps review tool outputs before use. |
| `docs/live_source_behavior_notes.md` | Explains live-source behavior and interpretation caveats. |

This document should be used before any future source expansion proposal.

---

## Final Rule

The project should stay useful before it becomes broad.

Do not expand source coverage unless the new source makes a real recurring regulatory or clinical workflow better.

```text
Usefulness first.
Scope control second.
Implementation last.
```
