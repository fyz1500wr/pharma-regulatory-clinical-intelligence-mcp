"""Tests for the MVP dashboard export artifact prototype.

These tests confirm the fixture-only exporter writes the expected artifacts
into a temporary directory, preserves source unavailable / partial-result
caveats, and does not leak forbidden non-MVP inference fields.

The exporter is fixture-only by design: there is no live source client to
patch, so the structural absence of network calls is asserted by ensuring
no `requests`/`urllib`/`httpx` modules are imported by the exporter module.
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from src.dashboard_export import mvp_fixture_export
from src.dashboard_export.mvp_fixture_export import (
    CLINICAL_CSV_HEADERS,
    DEFAULT_FIXTURE_PATH,
    FORBIDDEN_INFERENCE_FIELDS,
    MVP_ACTIVE_SOURCES,
    REGULATORY_CSV_HEADERS,
    export_artifacts,
    load_fixture,
    run_export,
)


EXPECTED_ARTIFACT_FILES = {
    "dashboard_snapshot.json",
    "dashboard_summary.md",
    "regulatory_updates.csv",
    "clinical_trials.csv",
    "source_health.json",
}


@pytest.fixture()
def fixture_payload() -> dict[str, Any]:
    return load_fixture(DEFAULT_FIXTURE_PATH)


@pytest.fixture()
def exported(tmp_path: Path) -> dict[str, Path]:
    return run_export(tmp_path)


def _walk_strings(value: Any) -> list[str]:
    collected: list[str] = []
    if isinstance(value, dict):
        for key, sub in value.items():
            collected.append(str(key))
            collected.extend(_walk_strings(sub))
    elif isinstance(value, list):
        for item in value:
            collected.extend(_walk_strings(item))
    elif value is not None:
        collected.append(str(value))
    return collected


def _walk_keys(value: Any) -> list[str]:
    collected: list[str] = []
    if isinstance(value, dict):
        for key, sub in value.items():
            collected.append(str(key))
            collected.extend(_walk_keys(sub))
    elif isinstance(value, list):
        for item in value:
            collected.extend(_walk_keys(item))
    return collected


def test_export_creates_all_expected_files(exported: dict[str, Path], tmp_path: Path) -> None:
    written = {path.name for path in tmp_path.iterdir() if path.is_file()}
    assert EXPECTED_ARTIFACT_FILES.issubset(written)
    for path in exported.values():
        assert path.exists()
        assert path.stat().st_size > 0


def test_snapshot_contains_required_sections(exported: dict[str, Path]) -> None:
    snapshot = json.loads(exported["dashboard_snapshot"].read_text(encoding="utf-8"))
    for section in ("regulatory_updates", "clinical_trials", "source_health", "digest_summaries"):
        assert section in snapshot, f"missing section: {section}"
        assert isinstance(snapshot[section], list)
        assert len(snapshot[section]) >= 1

    assert snapshot["mvp_active_sources"] == list(MVP_ACTIVE_SOURCES)
    assert snapshot["execution_mode"] == "fixture_only_manual_export"
    assert snapshot["human_review_required"] is True
    assert isinstance(snapshot["limitations"], list)
    assert any("fixture" in item.lower() for item in snapshot["limitations"])


def test_markdown_summary_includes_coverage_and_review_caveats(
    exported: dict[str, Path],
) -> None:
    text = exported["dashboard_summary"].read_text(encoding="utf-8")
    assert "# MVP Dashboard Export Prototype Summary" in text
    assert "Source Coverage" in text
    assert "Partial Result Warnings" in text
    assert "Human Review" in text
    assert "human_review_required" in text
    assert "registry-reported" in text
    assert "Fixture/mock data only" in text


def test_csv_files_have_expected_headers(exported: dict[str, Path]) -> None:
    with exported["regulatory_updates_csv"].open(encoding="utf-8") as fh:
        reader = csv.reader(fh)
        regulatory_headers = next(reader)
        regulatory_rows = list(reader)
    assert tuple(regulatory_headers) == REGULATORY_CSV_HEADERS
    assert len(regulatory_rows) >= 2

    with exported["clinical_trials_csv"].open(encoding="utf-8") as fh:
        reader = csv.reader(fh)
        clinical_headers = next(reader)
        clinical_rows = list(reader)
    assert tuple(clinical_headers) == CLINICAL_CSV_HEADERS
    assert len(clinical_rows) >= 2


def test_forbidden_inference_fields_absent_in_artifacts(
    exported: dict[str, Path],
) -> None:
    snapshot = json.loads(exported["dashboard_snapshot"].read_text(encoding="utf-8"))
    source_health = json.loads(exported["source_health"].read_text(encoding="utf-8"))

    for blob in (snapshot, source_health):
        keys = set(_walk_keys(blob))
        leaked = keys & FORBIDDEN_INFERENCE_FIELDS
        assert not leaked, f"forbidden inference fields leaked: {leaked}"

    summary_text = exported["dashboard_summary"].read_text(encoding="utf-8")
    csv_text = "\n".join(
        [
            exported["regulatory_updates_csv"].read_text(encoding="utf-8"),
            exported["clinical_trials_csv"].read_text(encoding="utf-8"),
        ]
    )
    for forbidden in FORBIDDEN_INFERENCE_FIELDS:
        assert forbidden not in summary_text
        assert forbidden not in csv_text


def test_source_unavailable_preserved_as_caveat(exported: dict[str, Path]) -> None:
    source_health = json.loads(exported["source_health"].read_text(encoding="utf-8"))
    statuses = [record["status"] for record in source_health["source_health"]]
    assert "source_unavailable" in statuses

    snapshot = json.loads(exported["dashboard_snapshot"].read_text(encoding="utf-8"))
    digest = snapshot["digest_summaries"][0]
    partial_warnings = digest.get("partial_result_warnings", [])
    assert partial_warnings, "expected partial result warnings to be preserved"
    assert any(
        "must not be treated as zero" in warning.lower()
        or "must not be interpreted as zero" in warning.lower()
        for warning in partial_warnings
    )

    excluded = digest.get("excluded_or_unavailable_sources", [])
    assert excluded, "excluded_or_unavailable_sources must be preserved"


def test_only_mvp_active_sources_listed_as_runtime_sources(
    exported: dict[str, Path],
) -> None:
    snapshot = json.loads(exported["dashboard_snapshot"].read_text(encoding="utf-8"))
    assert set(snapshot["mvp_active_sources"]) <= set(MVP_ACTIVE_SOURCES)

    non_mvp_candidates = {"EMA", "NMPA", "CDE", "PMDA", "WHO ICTRP", "EU CTIS", "ICH"}
    for source in non_mvp_candidates:
        assert source not in snapshot["mvp_active_sources"]


def test_clinical_trial_sponsor_remains_registry_reported(
    exported: dict[str, Path], fixture_payload: dict[str, Any]
) -> None:
    snapshot = json.loads(exported["dashboard_snapshot"].read_text(encoding="utf-8"))
    fixture_sponsors = {
        record.get("sponsor_or_collaborator")
        for record in fixture_payload["clinical_trials"]
    }
    exported_sponsors = {
        record.get("sponsor_or_collaborator")
        for record in snapshot["clinical_trials"]
    }
    assert exported_sponsors == fixture_sponsors

    for record in snapshot["clinical_trials"]:
        assert "company_alias" not in record
        assert "corporate_family" not in record
        assert "product_ownership" not in record


def test_exporter_does_not_import_live_source_clients() -> None:
    source_text = Path(mvp_fixture_export.__file__).read_text(encoding="utf-8")
    forbidden_imports = (
        "import requests",
        "import urllib.request",
        "from urllib.request",
        "import httpx",
        "from src.connectors",
        "from src.mcp_server",
    )
    for fragment in forbidden_imports:
        assert fragment not in source_text, (
            f"exporter must remain fixture-only; found forbidden import: {fragment}"
        )


def test_partial_metadata_record_preserved_with_caveat(
    exported: dict[str, Path],
) -> None:
    snapshot = json.loads(exported["dashboard_snapshot"].read_text(encoding="utf-8"))
    partial_clinical = [
        record
        for record in snapshot["clinical_trials"]
        if record.get("start_date") is None
    ]
    assert partial_clinical, "expected at least one clinical trial record with missing dates"
    for record in partial_clinical:
        assert record.get("result_state") != "no_matching_records"
        caveats = record.get("display_caveats", [])
        assert any("partial" in caveat.lower() or "missing" in caveat.lower() for caveat in caveats)


def test_cli_writes_artifacts_to_out_directory(tmp_path: Path) -> None:
    out_dir = tmp_path / "dashboard_mvp"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.dashboard_export.mvp_fixture_export",
            "--out",
            str(out_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "dashboard_snapshot" in result.stdout
    for filename in EXPECTED_ARTIFACT_FILES:
        assert (out_dir / filename).exists()


def test_export_artifacts_function_returns_paths(tmp_path: Path) -> None:
    fixture = load_fixture(DEFAULT_FIXTURE_PATH)
    artifacts = export_artifacts(fixture, tmp_path)
    assert set(artifacts.keys()) == {
        "dashboard_snapshot",
        "dashboard_summary",
        "regulatory_updates_csv",
        "clinical_trials_csv",
        "source_health",
    }
    for path in artifacts.values():
        assert path.exists()
