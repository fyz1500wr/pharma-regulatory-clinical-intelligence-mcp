# Project State — Pharma Regulatory Clinical Intelligence MCP

Last updated: 2026-06-02

Repository: `fyz1500wr/pharma-regulatory-clinical-intelligence-mcp`
Current stable branch: `main`
Current completed release: `v0.2.5-offline-tfda-bilingual-regulatory-search-smoke`

---

## 1. Current Status

The repository is currently at a clean post-v0.2.5 checkpoint after the TFDA bilingual offline smoke example was merged.

Latest confirmed functional release commit:

```text
1515075 Add offline TFDA bilingual regulatory search smoke example (#54)
```

Latest confirmed release tag:

```text
v0.2.5-offline-tfda-bilingual-regulatory-search-smoke
```

Important correction note:

The v0.2.5 tag was initially created after a duplicated root `PROJECT_STATE.md` commit appeared on `main`. The duplicate root file was removed in PR #55, and the v0.2.5 tag was corrected to point to the cleaned post-v0.2.5 main state.

---

## 2. Completed Work Since Previous Project State

### v0.2.3 — Offline regulatory date range smoke example

PR:

```text
#49 Add offline date range regulatory search smoke example
```

Main commit:

```text
68b1f59 Add offline date range smoke example (#49)
```

Initial release tag:

```text
v0.2.3-offline-regulatory-date-range-smoke
```

Scope:

- Added offline mocked smoke example for `search_regulatory_updates(date_range=...)`.
- Added documentation for the date range smoke example.
- Added pytest wrapper for the smoke example.
- Added README documentation index entry.

Validation result on main after merge:

```text
python examples/offline_regulatory_date_range_smoke.py
offline regulatory date range smoke passed

python -m pytest -q
172 passed
```

Important interpretation:

Passing this offline smoke confirms the mocked date range normalization and filtering path. It does not validate live FDA or TFDA availability.

---

### v0.2.3.1 — Hotfix for smoke import path and README reminder

PR:

```text
#50 Fix offline date range smoke import path and README reminder
```

Main commit:

```text
66677e6 Fix offline date range smoke import path and README reminder (#50)
```

Patch release tag:

```text
v0.2.3.1-offline-regulatory-date-range-smoke-hotfix
```

Scope:

- Made `examples/offline_regulatory_date_range_smoke.py` robust when run from the repository root by explicitly adding the repository root to `sys.path`.
- Restored the README `Non-Expansion Reminder` text that was unintentionally removed during the v0.2.3 README index update.

Validation result on main after merge:

```text
python examples/offline_regulatory_date_range_smoke.py
offline regulatory date range smoke passed

python -m pytest -q
172 passed
```

---

### v0.2.4 — Bilingual product modality keyword taxonomy

PR:

```text
#51 Expand bilingual product modality keyword taxonomy
```

Main commit:

```text
79ba7f5 Expand bilingual product modality keyword taxonomy (#51)
```

Release tag:

```text
v0.2.4-bilingual-product-modality-taxonomy
```

Scope:

- Expanded MVP product modality keyword taxonomy with English and Traditional Chinese terms.
- Added regression tests for bilingual keyword classification.
- Preserved scope control: taxonomy/config/tests only.

Files changed:

```text
config/taxonomy/product_modality_keywords.yaml
tests/test_product_modality_classifier.py
```

Additional regression coverage:

- Bilingual English/Traditional Chinese keyword matching across MVP modality labels.
- ADC phrases should classify as `adc`, not plain `antibody`.
- `mRNA疫苗` should prioritize `mrna_rna` over general `vaccine`.
- Unresolved Chinese content should remain `requires_manual_review`.

Validation result on main after merge and corrected tag:

```text
python -m pytest tests/test_product_modality_classifier.py -q
10 passed

python -m pytest -q
176 passed
```

---

### v0.2.5 — Offline TFDA bilingual regulatory search smoke example

PR:

```text
#54 Add offline TFDA bilingual regulatory search smoke example
```

Main commit:

```text
1515075 Add offline TFDA bilingual regulatory search smoke example (#54)
```

Release tag:

```text
v0.2.5-offline-tfda-bilingual-regulatory-search-smoke
```

Scope:

- Added an offline mocked TFDA-style bilingual regulatory search smoke example.
- Added documentation for the TFDA bilingual regulatory search smoke example.
- Added pytest wrapper for the smoke example.
- Added README documentation index entry.
- Preserved scope control: offline example/docs/tests only.

Files added or updated:

```text
examples/offline_tfda_bilingual_regulatory_search_smoke.py
docs/tfda_bilingual_regulatory_search_smoke_example.md
tests/test_offline_tfda_bilingual_regulatory_search_smoke_example.py
README.md
```

Validated behavior:

- TFDA bilingual query retrieval for `mRNA疫苗`
- TFDA bilingual query retrieval for `抗體藥物複合體 ADC`
- TFDA bilingual query retrieval for `生物相似性藥品`
- product modality classification from Chinese title and summary text
- `product_modality="mrna_rna"`
- `product_modality="adc"`
- `product_modality="biosimilar"`
- `product_modality` as a list of strings
- no-result behavior after product modality filtering
- invalid `product_modality` structured error handling
- `query_metadata.filters_applied.query`
- `query_metadata.filters_applied.product_modality`

Validation result on main after merge:

```text
python examples/offline_tfda_bilingual_regulatory_search_smoke.py
offline TFDA bilingual regulatory search smoke passed

python -m pytest tests/test_offline_tfda_bilingual_regulatory_search_smoke_example.py -q
1 passed

python -m pytest -q
177 passed
```

Important interpretation:

Passing this offline smoke confirms the TFDA-style bilingual query retrieval and product modality filter path in mocked records. It does not validate live TFDA source availability.

---

## 3. Important Workflow Correction

Use this workflow for future PRs:

```text
Create branch → implement → run focused tests → run full tests → open PR → confirm mergeable/review comments → merge → pull main → rerun relevant tests → tag
```

Do not tag before confirming that the PR has actually been merged into `main`.

Do not suggest merge before running tests when the PR branch can be tested in Codespaces.

---

## 4. Current Guardrails

MVP source scope remains limited to:

```text
FDA
TFDA
ClinicalTrials.gov
```

Do not add the following unless explicitly approved:

- Additional agencies such as EMA, NMPA, PMDA, WHO ICTRP, EU CTIS
- Literature integration
- Patent integration
- Finance integration
- Scheduler
- Alerts
- Persistence layer
- Dashboard
- HTTP/SSE transport
- GitHub issue automation
- New MCP tools
- `.mcp.json` changes

For uncertain work, keep the implementation smaller and document limitations clearly.

---

## 5. Current Known Notes

### Testing environment

The Codespaces environment may not always have dev dependencies installed. If `pytest` is missing, install the project with dev dependencies first:

```bash
python -m pip install -e ".[dev]"
```

Do not commit generated or accidental dependency files such as `poetry.lock` unless dependency management is explicitly approved as part of the task.

### Product modality classifier behavior

The current classifier is keyword mapping driven. v0.2.4 expanded the mapping and tests without changing core classifier logic.

Current classifier priority is determined by the order of labels in `config/taxonomy/product_modality_keywords.yaml`. This is intentional for the current MVP implementation and is covered by tests for ADC and mRNA vaccine priority behavior.

---

## 6. Recommended Next Step

Recommended next version:

```text
v0.2.6 — Decide next controlled post-smoke improvement
```

Recommended options:

- Add a documentation-only maintenance note for offline smoke example conventions.
- Add a small test-only regression for README documentation index consistency.
- Add a small offline smoke for query metadata consistency across FDA and TFDA mocked regulatory search.

Keep the next step small and phase-controlled.

Do not add new source scope, MCP tools, `.mcp.json` changes, scheduler, alerts, persistence, dashboard, HTTP/SSE transport, GitHub issue automation, EMA/NMPA/PMDA/WHO ICTRP/EU CTIS, literature, patent, or finance integrations.
