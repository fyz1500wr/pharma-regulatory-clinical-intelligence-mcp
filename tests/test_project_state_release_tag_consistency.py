from __future__ import annotations

import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_STATE_PATH = REPO_ROOT / ".ai" / "PROJECT_STATE.md"


def _project_state_text() -> str:
    return PROJECT_STATE_PATH.read_text(encoding="utf-8")


def _extract_inline_value(label: str, text: str) -> str:
    pattern = rf"^{re.escape(label)}: `([^`]+)`$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    assert match is not None, f"Missing project-state field: {label}"
    return match.group(1)


def _extract_fenced_value(label: str, text: str) -> str:
    pattern = rf"^{re.escape(label)}:\n\n```text\n([^\n]+)\n```"
    match = re.search(pattern, text, flags=re.MULTILINE)
    assert match is not None, f"Missing fenced project-state field: {label}"
    return match.group(1)


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def test_current_release_matches_latest_release_tag() -> None:
    text = _project_state_text()

    current_release = _extract_inline_value("Current completed release", text)
    latest_release_tag = _extract_fenced_value("Latest confirmed release tag", text)

    assert current_release == latest_release_tag
    assert re.fullmatch(r"v\d+\.\d+\.\d+-[a-z0-9][a-z0-9-]*", current_release)


def test_latest_main_commit_is_ancestor_of_current_head() -> None:
    text = _project_state_text()
    latest_main_commit = _extract_fenced_value("Latest confirmed main commit", text)
    short_sha = latest_main_commit.split(maxsplit=1)[0]

    assert re.fullmatch(r"[0-9a-f]{7,40}", short_sha)

    full_sha = _git("rev-parse", short_sha)
    _git("merge-base", "--is-ancestor", full_sha, "HEAD")


def test_current_release_section_mentions_release_tag_and_pr() -> None:
    text = _project_state_text()
    current_release = _extract_inline_value("Current completed release", text)

    release_title = current_release.removeprefix("v")
    major_minor_patch = re.match(r"\d+\.\d+\.\d+", release_title)
    assert major_minor_patch is not None
    version_heading_prefix = f"### v{major_minor_patch.group(0)}"

    matching_headings = [
        line for line in text.splitlines() if line.startswith(version_heading_prefix)
    ]
    assert matching_headings, f"Missing release section for {current_release}"

    section_start = text.index(matching_headings[0])
    following_text = text[section_start:]
    section = following_text.split("\n---\n", maxsplit=1)[0]

    assert f"Release tag: {current_release}" in section
    assert re.search(r"^PR: #\d+ ", section, flags=re.MULTILINE)
    assert re.search(r"^Main commit: [0-9a-f]{7,40} ", section, flags=re.MULTILINE)


def test_project_state_has_recommended_next_version() -> None:
    text = _project_state_text()

    assert "Recommended next version:" in text
    assert re.search(
        r"Recommended next version:\n\n```text\nv\d+\.\d+\.\d+ — .+\n```",
        text,
    )


def test_project_state_keeps_scope_guardrails_visible() -> None:
    text = _project_state_text()

    required_guardrails = [
        "No new source expansion",
        "No new MCP tools",
        "No `.mcp.json` changes",
        "No scheduler / alerts / persistence / dashboard work",
        "No EMA / NMPA / PMDA / WHO ICTRP / EU CTIS source additions",
    ]

    missing_guardrails = [guardrail for guardrail in required_guardrails if guardrail not in text]

    assert missing_guardrails == []
