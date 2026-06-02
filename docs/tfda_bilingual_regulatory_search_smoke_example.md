# TFDA Bilingual Regulatory Search Offline Smoke Example

## Purpose

This document explains the offline smoke example for validating TFDA-style bilingual regulatory search behavior using `search_regulatory_updates(...)`.

The example exists because live TFDA access can fail due to runtime network policy, egress allowlist, temporary source availability, website changes, or connector source access issues. Those failures should not be confused with failure of bilingual query handling, product modality classification, or product modality filtering itself.

## Command

Run from the repository root:

    python examples/offline_tfda_bilingual_regulatory_search_smoke.py

## What it validates

- TFDA-style Chinese / bilingual query retrieval for `mRNA疫苗`
- TFDA-style Chinese / bilingual query retrieval for `抗體藥物複合體 ADC`
- TFDA-style Chinese / bilingual query retrieval for `生物相似性藥品`
- product modality classification from Chinese title and summary text
- `product_modality="mrna_rna"`
- `product_modality="adc"`
- `product_modality="biosimilar"`
- `product_modality` as a list of strings
- no-result behavior after product modality filtering
- invalid `product_modality` structured error handling
- `query_metadata.filters_applied.query`
- `query_metadata.filters_applied.product_modality`

## What it does not validate

- live TFDA website/API availability
- live FDA website/API availability
- egress allowlist configuration
- real-world TFDA source completeness
- final regulatory interpretation
- final product modality classification for real submissions or regulatory decisions

## Interpretation rule

Passing this smoke example means the offline TFDA-style bilingual retrieval and product modality filter path is working.

It does not mean TFDA live source access is healthy.

A live source error must still be interpreted using `check_source_health`, `list_source_failures`, and the Source Failure Diagnostic Runbook.
