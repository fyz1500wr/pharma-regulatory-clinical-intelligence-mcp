# Offline Smoke Example Conventions

## Purpose

This document defines conventions for adding offline smoke examples to this repository.

Offline smoke examples validate local normalization, filtering, metadata, and structured error behavior without depending on live FDA, TFDA, or ClinicalTrials.gov source availability.

They help distinguish implementation behavior from external-source problems such as network policy, egress allowlist restrictions, temporary source downtime, website changes, parser changes, or API changes.

## Naming convention

Use explicit, searchable names.

Recommended pattern:

```text
examples/offline_<source_or_feature>_<behavior>_smoke.py
docs/<source_or_feature>_<behavior>_smoke_example.md
tests/test_offline_<source_or_feature>_<behavior>_smoke_example.py
```

Current examples:

```text
examples/offline_product_modality_regulatory_search_smoke.py
docs/product_modality_regulatory_search_smoke_example.md
tests/test_offline_product_modality_smoke_example.py

examples/offline_regulatory_date_range_smoke.py
docs/regulatory_date_range_smoke_example.md
tests/test_offline_regulatory_date_range_smoke_example.py

examples/offline_tfda_bilingual_regulatory_search_smoke.py
docs/tfda_bilingual_regulatory_search_smoke_example.md
tests/test_offline_tfda_bilingual_regulatory_search_smoke_example.py
```

Prefer complete names for new files. Avoid shortening test names when the example name already includes important terms such as `regulatory_search`.

## Example script structure

Each offline smoke example should:

1. Be executable from the repository root.
2. Add the repository root to `sys.path`.
3. Monkey patch only the minimum required client or time dependency.
4. Restore patched objects in a `finally` block.
5. Use deterministic fixture records.
6. Print a JSON summary with `status`, `validated_cases`, and `important_interpretation`.
7. Print one stable pass message used by the pytest wrapper.

## Documentation structure

Each smoke example document should use this structure:

```text
# <Smoke Example Title>

## Purpose
## Command
## What it validates
## What it does not validate
## Interpretation rule
```

The document must clearly state that passing the offline smoke does not prove live-source availability or final regulatory interpretation.

## Pytest wrapper structure

The pytest wrapper should run the example through `subprocess.run(...)` from the repository root.

The wrapper should assert the stable pass message and several important validated cases from stdout. It should not duplicate the full validation logic already present in the example script.

## README index rule

When adding a new offline smoke document, add one row to the README Post-MVP Documentation Index.

Place the row near related smoke example documents, not at the top of the table.

## Scope control

Offline smoke examples must not add source scope.

Do not add the following as part of an offline smoke example unless explicitly approved:

- New agencies such as EMA, NMPA, PMDA, WHO ICTRP, or EU CTIS
- New MCP tools
- `.mcp.json` changes
- Scheduler
- Alerts
- Persistence layer
- Dashboard
- HTTP/SSE transport
- GitHub issue automation
- Literature integration
- Patent integration
- Finance integration

## Validation expectation

For documentation-only convention changes, runtime tests are usually not required.

For new offline smoke examples, run at minimum:

```bash
python examples/<offline_smoke_name>.py
python -m pytest tests/test_<offline_smoke_name>_example.py -q
python -m pytest -q
```

If the change is documentation-only but touches the README index or project state, validate with grep/file existence checks and consider running the full test suite if the branch is already in Codespaces.
