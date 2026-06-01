# Product Modality Regulatory Search Offline Smoke Example

## Purpose

This document explains the offline smoke example for validating `search_regulatory_updates(product_modality=...)`.

The example exists because live FDA or TFDA access can fail due to runtime network policy, egress allowlist, temporary source availability, or connector source access issues. Those failures should not be confused with failure of the product modality filter itself.

## Command

Run from the repository root:

    python examples/offline_product_modality_regulatory_search_smoke.py

## What it validates

- `product_modality` as a string
- `product_modality` as a list of strings
- invalid `product_modality` structured error handling
- no-result behavior after modality filtering
- `query_metadata.filters_applied.product_modality`
- FDA mocked regulatory update records
- TFDA mocked regulatory update records

## What it does not validate

- live FDA website/API availability
- live TFDA website/API availability
- egress allowlist configuration
- real-world source completeness
- final regulatory interpretation
- final product modality classification

## Interpretation rule

Passing this smoke example means the offline product modality filter path is working.

It does not mean FDA or TFDA live source access is healthy.

A live source error must still be interpreted using `check_source_health`, `list_source_failures`, and the Source Failure Diagnostic Runbook.
