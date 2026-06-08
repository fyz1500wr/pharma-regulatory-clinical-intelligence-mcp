from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPO_ROOT / "README.md"
INDEX_HEADING = "## Post-MVP Documentation Index"

EXPECTED_INDEX_ENTRIES = [
    "docs/mvp_v1_completion_note.md",
    "docs/mcp_usage_examples.md",
    "docs/sample_prompts.md",
    "docs/tool_output_review_checklist.md",
    "docs/live_source_behavior_notes.md",
    "docs/post_mvp_source_expansion_decision_matrix.md",
    "docs/claude_project_validation_workflow.md",
    "docs/claude_code_web_mcp_smoke_test_note.md",
    "docs/source_failure_diagnostic_runbook.md",
    "docs/product_value_usability_calibration.md",
    "docs/regulatory_clinical_digest_report_workflow.md",
    "docs/regulatory_clinical_digest_example_memo.md",
    "docs/regulatory_clinical_digest_prompt_pack.md",
    "docs/regulatory_clinical_digest_memo_validation_exercise.md",
    "docs/regulatory_clinical_digest_report_template_contract.md",
    "docs/regulatory_clinical_digest_clean_source_dry_run.md",
    "docs/cmc_submission_readiness_mapping_workflow.md",
    "docs/product_modality_regulatory_search_smoke_example.md",
    "docs/regulatory_date_range_smoke_example.md",
    "docs/tfda_bilingual_regulatory_search_smoke_example.md",
    "docs/offline_smoke_example_conventions.md",
    "docs/query_metadata_consistency_smoke_example.md",
    "docs/clinical_trial_query_metadata_consistency_smoke_example.md",
    "docs/mvp_live_acceptance_validation_runbook.md",
    "docs/mvp_live_acceptance_validation_results_template.md",
    "docs/release_handoff_checklist.md",
    "docs/v0.2.15_source_resilience_scope_plan.md",
    ".ai/PROJECT_STATE.md",
]


def _readme_text() -> str:
    return README_PATH.read_text(encoding="utf-8")


def _post_mvp_index_section(readme_text: str) -> str:
    assert INDEX_HEADING in readme_text
    section = readme_text.split(INDEX_HEADING, maxsplit=1)[1]
    return section.split("\n---", maxsplit=1)[0]


def _indexed_paths(index_section: str) -> list[str]:
    return re.findall(r"\|\s*`([^`]+)`\s*\|", index_section)


def test_readme_post_mvp_documentation_index_exists() -> None:
    section = _post_mvp_index_section(_readme_text())

    assert "| Document | Use |" in section
    assert "|---|---|" in section


def test_readme_post_mvp_documentation_index_contains_expected_entries() -> None:
    indexed_paths = set(_indexed_paths(_post_mvp_index_section(_readme_text())))

    missing_entries = sorted(set(EXPECTED_INDEX_ENTRIES) - indexed_paths)

    assert missing_entries == []


def test_readme_post_mvp_documentation_index_entries_exist() -> None:
    indexed_paths = _indexed_paths(_post_mvp_index_section(_readme_text()))

    missing_files = [path for path in indexed_paths if not (REPO_ROOT / path).exists()]

    assert missing_files == []


def test_readme_post_mvp_documentation_index_has_no_duplicate_entries() -> None:
    indexed_paths = _indexed_paths(_post_mvp_index_section(_readme_text()))

    duplicate_paths = sorted(
        path for path in set(indexed_paths) if indexed_paths.count(path) > 1
    )

    assert duplicate_paths == []


def test_release_handoff_checklist_is_indexed_with_expected_scope() -> None:
    section = _post_mvp_index_section(_readme_text())

    expected_row = (
        "| `docs/release_handoff_checklist.md` | Defines the merge, tag, "
        "project-state, branch cleanup, and final verification checklist for "
        "controlled release handoff. |"
    )

    assert expected_row in section


def test_digest_report_template_contract_is_indexed_with_expected_scope() -> None:
    section = _post_mvp_index_section(_readme_text())

    expected_row = (
        "| `docs/regulatory_clinical_digest_report_template_contract.md` | "
        "Defines the fixed input, output, source coverage, sponsor association, "
        "and acceptance criteria contract for controlled digest memo templates. |"
    )

    assert expected_row in section


def test_clean_source_digest_dry_run_is_indexed_with_expected_scope() -> None:
    section = _post_mvp_index_section(_readme_text())

    expected_row = (
        "| `docs/regulatory_clinical_digest_clean_source_dry_run.md` | "
        "Records a controlled clean-source dry-run memo validating TFDA and "
        "ClinicalTrials.gov memo behavior without FDA unavailable-source interference. |"
    )

    assert expected_row in section


def test_cmc_submission_readiness_mapping_workflow_is_indexed_with_expected_scope() -> None:
    section = _post_mvp_index_section(_readme_text())

    expected_row = (
        "| `docs/cmc_submission_readiness_mapping_workflow.md` | "
        "Defines the docs/spec-only CMC submission readiness mapping workflow "
        "for Module 3 gaps, vendor dependencies, critical path, and PM follow-up. |"
    )

    assert expected_row in section
