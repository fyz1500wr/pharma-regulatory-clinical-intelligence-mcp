"""MVP dashboard export artifact prototype.

Reads a fixture/mock dashboard record set and writes a minimal set of
dashboard artifacts to an output directory:

    dashboard_snapshot.json
    dashboard_summary.md
    regulatory_updates.csv
    clinical_trials.csv
    source_health.json

This is a fixture-only prototype. It does not perform any live HTTP calls
and does not add a runtime dashboard renderer, MCP tool, scheduler, alerts,
persistence layer, HTTP/SSE surface, or GitHub Actions workflow.

The prototype enforces MVP guardrails:

* Only FDA, TFDA, ClinicalTrials.gov are listed as MVP active runtime sources.
* Source unavailable / partial results are preserved as caveats, not as
  no-matching-records.
* Forbidden inference fields (approval_probability, clinical_success_score,
  commercial_strength_score, product_ownership, company_alias,
  corporate_family) are stripped from all exported artifacts.
* Clinical trial sponsor/company fields remain registry-reported only.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Iterable

DEFAULT_FIXTURE_PATH = (
    Path(__file__).resolve().parents[2]
    / "tests"
    / "fixtures"
    / "dashboard_mvp_fixture.json"
)

MVP_ACTIVE_SOURCES: tuple[str, ...] = ("FDA", "TFDA", "ClinicalTrials.gov")

FORBIDDEN_INFERENCE_FIELDS: frozenset[str] = frozenset(
    {
        "approval_probability",
        "clinical_success",
        "clinical_success_score",
        "commercial_strength",
        "commercial_strength_score",
        "company_superiority",
        "product_ownership",
        "company_alias",
        "corporate_family",
        "ownership_inference",
    }
)

REGULATORY_CSV_HEADERS: tuple[str, ...] = (
    "record_id",
    "source",
    "agency",
    "title",
    "document_type",
    "publication_date",
    "last_update_date",
    "official_url",
    "product_modality",
    "topic",
    "source_health_status",
    "result_state",
    "human_review_required",
    "display_caveats",
)

CLINICAL_CSV_HEADERS: tuple[str, ...] = (
    "record_id",
    "registry",
    "registry_id",
    "brief_title",
    "condition_or_indication",
    "sponsor_or_collaborator",
    "intervention_name",
    "trial_phase",
    "trial_status",
    "start_date",
    "primary_completion_date",
    "completion_date",
    "last_update_posted",
    "results_available",
    "registry_url",
    "source_health_status",
    "result_state",
    "human_review_required",
    "display_caveats",
)


def load_fixture(fixture_path: Path) -> dict[str, Any]:
    """Load a mock dashboard fixture from disk."""
    with fixture_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _scrub(value: Any) -> Any:
    """Recursively remove forbidden inference fields."""
    if isinstance(value, dict):
        return {
            key: _scrub(sub)
            for key, sub in value.items()
            if key not in FORBIDDEN_INFERENCE_FIELDS
        }
    if isinstance(value, list):
        return [_scrub(item) for item in value]
    return value


def _normalize_records(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for record in records:
        scrubbed = _scrub(dict(record))
        scrubbed.setdefault("human_review_required", True)
        normalized.append(scrubbed)
    return normalized


def _filter_mvp_sources(sources: Iterable[str]) -> list[str]:
    seen: list[str] = []
    for source in sources:
        if source in MVP_ACTIVE_SOURCES and source not in seen:
            seen.append(source)
    return seen


def _flatten_for_csv(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple)):
        return "; ".join(_flatten_for_csv(item) for item in value)
    return str(value)


def build_snapshot(fixture: dict[str, Any]) -> dict[str, Any]:
    """Build the dashboard_snapshot.json payload from the fixture."""
    regulatory = _normalize_records(fixture.get("regulatory_updates", []))
    clinical = _normalize_records(fixture.get("clinical_trials", []))
    source_health = _normalize_records(fixture.get("source_health", []))
    digest_summaries = _normalize_records(fixture.get("digest_summaries", []))

    declared_sources = fixture.get("mvp_active_sources", list(MVP_ACTIVE_SOURCES))
    mvp_active_sources = _filter_mvp_sources(declared_sources)

    return {
        "artifact_kind": "mvp_dashboard_export_prototype_snapshot",
        "artifact_version": "0.1-prototype",
        "fixture_id": fixture.get("fixture_id"),
        "execution_mode": "fixture_only_manual_export",
        "mvp_active_sources": mvp_active_sources,
        "regulatory_updates": regulatory,
        "clinical_trials": clinical,
        "source_health": source_health,
        "digest_summaries": digest_summaries,
        "human_review_required": True,
        "limitations": [
            "Fixture/mock data only; no live source calls were performed.",
            "MVP active sources only: FDA, TFDA, ClinicalTrials.gov.",
            "Source unavailable or partial results must not be interpreted as zero records.",
            "Clinical trial sponsor/company values are registry-reported only.",
        ],
    }


def _render_markdown_summary(snapshot: dict[str, Any]) -> str:
    digest = (snapshot.get("digest_summaries") or [{}])[0]
    lines: list[str] = []
    lines.append("# MVP Dashboard Export Prototype Summary")
    lines.append("")
    lines.append("Fixture/mock data only. This is not a runtime dashboard.")
    lines.append("")
    lines.append("## Execution Context")
    lines.append("")
    lines.append(f"- Execution mode: {snapshot.get('execution_mode')}")
    lines.append(
        "- MVP active sources: "
        + ", ".join(snapshot.get("mvp_active_sources", []))
    )
    lines.append(f"- Fixture id: {snapshot.get('fixture_id')}")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append(
        f"- Regulatory updates: {len(snapshot.get('regulatory_updates', []))}"
    )
    lines.append(
        f"- Clinical trial records: {len(snapshot.get('clinical_trials', []))}"
    )
    lines.append(
        f"- Source health records: {len(snapshot.get('source_health', []))}"
    )
    lines.append(
        f"- Digest summaries: {len(snapshot.get('digest_summaries', []))}"
    )
    lines.append("")
    lines.append("## Source Coverage")
    lines.append("")
    coverage = digest.get("source_coverage_summary") or (
        "No digest source coverage summary in fixture."
    )
    lines.append(f"- Source coverage summary: {coverage}")
    excluded = digest.get("excluded_or_unavailable_sources") or []
    if excluded:
        lines.append("- Excluded or unavailable sources:")
        for item in excluded:
            lines.append(f"  - {item}")
    else:
        lines.append("- Excluded or unavailable sources: none reported in fixture.")
    lines.append("")
    lines.append("## Partial Result Warnings")
    lines.append("")
    partial = digest.get("partial_result_warnings") or []
    if partial:
        for warning in partial:
            lines.append(f"- {warning}")
    else:
        lines.append("- No partial result warnings recorded in fixture.")
    lines.append("")
    lines.append("## Source Health Highlights")
    lines.append("")
    for record in snapshot.get("source_health", []):
        status = record.get("status", "unknown")
        source = record.get("source", "unknown")
        failure_type = record.get("failure_type") or "none"
        lines.append(
            f"- {source}: status={status}, failure_type={failure_type}"
        )
    lines.append("")
    lines.append("## Human Review")
    lines.append("")
    lines.append(
        "- Human review required: all records in this prototype carry "
        "`human_review_required = true`."
    )
    lines.append(
        "- Source unavailable or partial results must not be interpreted "
        "as zero records."
    )
    lines.append(
        "- Clinical trial sponsor/company values are registry-reported only. "
        "No alias, ownership, or corporate-family inference is applied."
    )
    lines.append("")
    lines.append("## Limitations")
    lines.append("")
    for limitation in snapshot.get("limitations", []):
        lines.append(f"- {limitation}")
    lines.append("")
    return "\n".join(lines)


def _write_csv(
    path: Path, headers: tuple[str, ...], rows: Iterable[dict[str, Any]]
) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        for row in rows:
            writer.writerow([_flatten_for_csv(row.get(header)) for header in headers])


def export_artifacts(fixture: dict[str, Any], out_dir: Path) -> dict[str, Path]:
    """Write all dashboard artifacts and return a map of artifact name to path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    snapshot = build_snapshot(fixture)

    snapshot_path = out_dir / "dashboard_snapshot.json"
    summary_path = out_dir / "dashboard_summary.md"
    regulatory_csv_path = out_dir / "regulatory_updates.csv"
    clinical_csv_path = out_dir / "clinical_trials.csv"
    source_health_path = out_dir / "source_health.json"

    with snapshot_path.open("w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")

    summary_path.write_text(_render_markdown_summary(snapshot), encoding="utf-8")

    _write_csv(
        regulatory_csv_path, REGULATORY_CSV_HEADERS, snapshot["regulatory_updates"]
    )
    _write_csv(clinical_csv_path, CLINICAL_CSV_HEADERS, snapshot["clinical_trials"])

    source_health_payload = {
        "artifact_kind": "mvp_dashboard_export_prototype_source_health",
        "artifact_version": "0.1-prototype",
        "mvp_active_sources": snapshot["mvp_active_sources"],
        "source_health": snapshot["source_health"],
        "human_review_required": True,
        "limitations": [
            "Fixture/mock data only.",
            "Source unavailable status must not be interpreted as zero records.",
        ],
    }
    with source_health_path.open("w", encoding="utf-8") as fh:
        json.dump(source_health_payload, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")

    return {
        "dashboard_snapshot": snapshot_path,
        "dashboard_summary": summary_path,
        "regulatory_updates_csv": regulatory_csv_path,
        "clinical_trials_csv": clinical_csv_path,
        "source_health": source_health_path,
    }


def run_export(out_dir: Path, fixture_path: Path = DEFAULT_FIXTURE_PATH) -> dict[str, Path]:
    """High-level entry point: load fixture and write artifacts."""
    fixture = load_fixture(fixture_path)
    return export_artifacts(fixture, out_dir)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Export MVP dashboard artifacts from a fixture/mock record set. "
            "Fixture-only; does not call live sources."
        )
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output directory for dashboard artifacts.",
    )
    parser.add_argument(
        "--fixture",
        default=str(DEFAULT_FIXTURE_PATH),
        help="Path to the dashboard fixture JSON file.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    artifacts = run_export(Path(args.out), Path(args.fixture))
    for name, path in artifacts.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
