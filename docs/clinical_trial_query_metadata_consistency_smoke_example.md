# Clinical Trial Query Metadata Consistency Offline Smoke Example

This document describes the offline clinical trial query metadata consistency smoke example.

## Purpose

The smoke example validates that ClinicalTrials.gov-style clinical trial search output keeps a stable metadata contract for indication, sponsor/company, phase, trial status, result availability, official URL, and query metadata.

It checks that clinical trial results consistently preserve:

- ClinicalTrials.gov registry metadata
- NCT ID / trial ID metadata
- official trial URL metadata
- indication metadata
- sponsor/company metadata
- intervention and product modality metadata
- phase and status metadata
- start, primary completion, and last update dates
- result availability metadata
- primary outcome metadata
- query metadata and filter metadata

## Scope

This is an offline smoke example. It uses mocked ClinicalTrials.gov-style records and does not call the live ClinicalTrials.gov API.

It does not validate live source availability, API uptime, ClinicalTrials.gov schema stability, or trial-result interpretation.

## Why this matters

The project needs stable clinical trial query metadata before expanding toward indication-by-company tracking. This smoke locks the expected output shape for clinical trial search and company comparison without adding live-source behavior.

## How to run

Run the smoke example:

    python examples/offline_clinical_trial_query_metadata_consistency_smoke.py

Expected final line:

    offline clinical trial query metadata consistency smoke passed

The pytest wrapper is:

    pytest tests/test_offline_clinical_trial_query_metadata_consistency_smoke_example.py -q

## Important interpretation

Passing this smoke means the normalized offline ClinicalTrials.gov-style clinical trial query metadata shape is consistent for mocked records.

It does not approve EMA, NMPA, PMDA, WHO ICTRP, EU CTIS, scheduler, alerting, persistence, dashboard, new MCP tool expansion, live ClinicalTrials.gov behavior changes, clinical superiority ranking, or trial success probability inference.
