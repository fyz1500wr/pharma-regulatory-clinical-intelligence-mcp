# Query Metadata Consistency Offline Smoke Example

This document describes the offline query metadata consistency smoke example.

## Purpose

The smoke example validates that normalized regulatory search output keeps a stable metadata contract across FDA-style and TFDA-style mocked records.

It checks that search results consistently preserve:

- agency metadata
- source type metadata
- query metadata
- date range metadata
- derived date_from / date_to metadata
- product_modality metadata
- normalized record fields such as title, official URL, publication date, update date, topics, and content hash

## Scope

This is an offline smoke example. It uses mocked FDA and TFDA records and does not call live FDA or TFDA sources.

It does not validate live source availability, webpage structure stability, or official API uptime.

## Why this matters

Future source expansion should not create inconsistent output shapes. Before adding additional agencies or live source behavior, new source outputs should align with this metadata contract.

## How to run

Run the smoke example:

    python examples/offline_query_metadata_consistency_smoke.py

Expected final line:

    offline query metadata consistency smoke passed

The pytest wrapper is:

    pytest tests/test_offline_query_metadata_consistency_smoke_example.py -q

## Important interpretation

Passing this smoke means the normalized offline regulatory search metadata shape is consistent across mocked FDA and TFDA records.

It does not approve EMA, NMPA, PMDA, scheduler, alerting, persistence, dashboard, or new MCP tool expansion.
