# Regulatory Date Range Offline Smoke Example

## Purpose

This document explains the offline smoke example for validating `search_regulatory_updates(date_range=...)` and related date filters.

The example exists because live FDA or TFDA access can fail due to runtime network policy, egress allowlist, temporary source availability, or connector source access issues. Those failures should not be confused with failure of date range normalization or date filtering itself.

## Command

Run from the repository root:

    python examples/offline_regulatory_date_range_smoke.py

## What it validates

- `date_range="1m"`
- `date_range="1y"`
- `date_range="custom"`
- `custom_date_range.start_date`
- `custom_date_range.end_date`
- `date_from` / `date_to` backward compatibility
- invalid `date_range` structured error handling
- ambiguous date input rejection when `date_range` is combined with `date_from` or `date_to`
- `query_metadata.filters_applied.date_range`
- `query_metadata.filters_applied.custom_date_range`
- `query_metadata.filters_applied.date_from`
- `query_metadata.filters_applied.date_to`

## What it does not validate

- live FDA website/API availability
- live TFDA website/API availability
- egress allowlist configuration
- real-world source completeness
- final regulatory interpretation
- correctness of source publication dates beyond the mocked fixture records

## Interpretation rule

Passing this smoke example means the offline date range normalization and filtering path is working.

It does not mean FDA or TFDA live source access is healthy.

A live source error must still be interpreted using `check_source_health`, `list_source_failures`, and the Source Failure Diagnostic Runbook.
