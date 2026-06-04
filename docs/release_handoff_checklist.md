# Release / Tag / Project-State Handoff Checklist

## Purpose

This checklist defines the release handoff steps for small, controlled repository changes.

It is intended to prevent recurring operational mistakes such as tagging before merge, leaving project state behind the latest release, forgetting branch cleanup, or using long terminal heredocs that can be pasted incorrectly.

This document is process guidance only. It does not add source scope, MCP tools, runtime behavior, scheduling, persistence, dashboards, or external integrations.

## When to use this checklist

Use this checklist when preparing a versioned project increment such as:

- Documentation-only maintenance release
- Offline smoke example release
- Small test-only regression release
- Project-state housekeeping release

For code changes, still run the relevant focused tests and full test suite before merge.

## 1. Before creating the branch

Confirm the current state:

```bash
git checkout main
git pull --ff-only origin main
git status --short
git log -1 --oneline
```

Expected result:

- Working tree is clean.
- `main` is up to date with `origin/main`.
- The latest commit is the intended base for the next branch.

## 2. Branch naming

Use a branch name that reflects the release purpose.

Recommended patterns:

```text
docs/v0.2.x-<topic>
feature/v0.2.x-<topic>
tests/v0.2.x-<topic>
housekeeping/<topic>
```

For documentation-only release handoff work, prefer:

```text
docs/v0.2.x-<topic>
```

## 3. Scope check before implementation

Confirm the change stays inside the approved scope.

For MVP v1, do not add the following unless explicitly approved:

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

If the change is only a documentation or checklist update, do not modify runtime code or tests unless the task explicitly requires it.

## 4. Implementation rules

Prefer small commits with clear intent.

Avoid long terminal heredocs for markdown files. They are error-prone when pasted into Codespaces terminals.

Safer options:

- Use GitHub file operations when possible.
- Use the VS Code editor for long markdown text.
- Use short Python replacements for small text edits.
- Split large updates into smaller verified steps.

## 5. Pre-PR local validation

For documentation-only changes, run lightweight checks:

```bash
git status --short
git diff --stat
git diff -- <changed-file>
```

For new documentation index entries, check:

```bash
grep -n "<new_doc_file_name>" README.md
```

For project-state updates, check:

```bash
grep -n "Current completed release" .ai/PROJECT_STATE.md
grep -n "Recommended next version" .ai/PROJECT_STATE.md
```

For code or test changes, run focused tests and the full test suite.

## 6. Pull request checklist

Before merge, confirm:

- PR title is clear.
- PR body states scope and validation.
- Changed files match the intended scope.
- PR is mergeable.
- Review comments are resolved.
- No unrelated files are included.
- No generated files are accidentally committed.

For documentation-only changes, the PR body should explicitly state:

```text
Documentation-only.
No runtime code changes.
No test changes.
No source scope changes.
No MCP tool changes.
No .mcp.json changes.
```

## 7. Merge rule

Do not tag before the PR is merged.

Use one of these two release orders, depending on whether `.ai/PROJECT_STATE.md` needs to change for the release.

When no project-state update is needed:

```text
Open PR → review diff → confirm mergeable → resolve comments → merge → pull main → validate → tag
```

When a project-state update is needed:

```text
Open PR → review diff → confirm mergeable → resolve comments → merge → pull main → validate → update project state PR → merge project state PR → pull main → final tests/checks → tag final main commit
```

Do not ask to merge a PR again after it has already been merged. After merge, switch to post-merge validation, project-state handling if needed, and tagging.

For small documentation-only PRs, squash merge is preferred unless repository policy requires another method.

## 8. Post-merge main sync

After each merge:

```bash
git checkout main
git pull --ff-only origin main
git log -1 --oneline
git status --short
```

Expected result:

- Local `main` is updated to the merged PR commit.
- Working tree is clean.
- If project-state update is needed, `.ai/PROJECT_STATE.md` is updated in a follow-up PR before tagging.

## 9. Tagging rule

The release tag should point to the final clean main state for that release, usually the post-project-state main commit when a project-state update is needed.

If project-state update is needed, update `.ai/PROJECT_STATE.md` before tagging.

Create the tag only after confirming the intended final commit:

```bash
TAG="v0.2.x-<topic>"
git tag -a "$TAG" -m "Release $TAG"
git push origin "$TAG"
git show --no-patch --oneline "$TAG"
```

If a tag was created too early, correct it intentionally:

```bash
TAG="v0.2.x-<topic>"
git tag -d "$TAG"
git push origin ":refs/tags/$TAG"
git tag -a "$TAG" -m "Release $TAG" <final-main-commit>
git push origin "$TAG"
git show --no-patch --oneline "$TAG"
```

Do not move a tag casually. Move a tag only to correct a documented release-state mismatch.

## 10. Project-state update rule

If a release requires project-state continuity, update `.ai/PROJECT_STATE.md` after the release PR is merged and validated, but before the final release tag is created.

At minimum, update:

- Current completed release
- Current status
- Latest confirmed main commit
- Latest confirmed release tag, if the tag already exists; otherwise record the intended tag in the handoff notes and update the confirmed tag after tagging
- Completed work section for the release
- Recommended next version
- Guardrails, if they changed

Do not mark a release as completed before the release PR is merged and the intended final main commit is known.

## 11. Final verification

Run final checks after the release PR is merged, after any required project-state PR is merged, and before or immediately after tagging as appropriate for the release order:

```bash
git checkout main
git pull --ff-only origin main
git status --short
git log -1 --oneline
git tag --points-at HEAD
git show --no-patch --oneline <release-tag>
grep -n "Current completed release" .ai/PROJECT_STATE.md
```

Expected result:

- `main` points to the latest intended release commit, usually the post-project-state commit when project state was required.
- Release tag points to the intended final clean main state.
- Project state names the completed release when a project-state update was required.
- Working tree is clean.

## 12. Branch cleanup

After merge, delete merged local and remote branches when safe:

```bash
git branch -d <branch-name>
git push origin --delete <branch-name>
```

If GitHub already deleted the remote branch, remote deletion may report that the branch does not exist. That is acceptable.

## Direction calibration after a sequence of similar PRs

After completing a sequence of similar PRs, the assistant/project workflow must pause before continuing.

For this rule, similar PRs include repeated documentation-only PRs, repeated project-state PRs, repeated source-health/source-resilience PRs, repeated test-only regressions, or repeated release housekeeping PRs.

Before proposing the next PR, perform a direction calibration checkpoint. The checkpoint must ask:

1. Are we still solving the original project objective, or only extending the latest local document?
2. Has the work become too narrow, too repetitive, or too documentation-heavy?
3. Are we drifting from MVP value, user workflow, or actual regulatory/clinical intelligence utility?
4. Is the next step better as planning, implementation, testing, documentation cleanup, or stopping?
5. Should the next increment be paused until the user confirms the direction?

The assistant should summarize:

- what was just completed
- what pattern the recent PRs followed
- what risks of drift or over-narrowing exist
- recommended next direction options
- one preferred next step

The assistant must not automatically continue into another same-type PR unless the user explicitly approves that direction after calibration.

This rule is intended to prevent both scope drift and scope tunnel vision. It does not block urgent fixes, user-requested specific changes, or safety/compliance corrections, but even those should be summarized afterward.

## Long-context continuation checkpoint

When a conversation becomes long, response latency noticeably increases, multiple PR/tag/release steps have accumulated, or the user may need to continue in a new chat, the assistant/project workflow should proactively recommend creating `PROJECT_STATE_CONTINUATION.md`.

This checkpoint is intended to preserve continuity and reduce repeated context reconstruction.

The continuation file should summarize:

- repository name and branch
- latest main commit
- latest release tag and tag target
- completed PRs and merged commits
- open/stale PRs and recommended handling
- latest validation commands and results
- current guardrails / non-expansion rules
- recommended next step
- any workflow preferences or active user instructions

The assistant should prefer this checkpoint before the conversation becomes too slow or too difficult to audit.

This is workflow guidance only and does not add runtime behavior or automation.

## 13. Handoff note for next work

End each release by recording the next recommended version in `.ai/PROJECT_STATE.md`.

The next version should remain small and controlled unless the user explicitly approves a larger scope.

Good examples:

```text
v0.2.x — Add README documentation index consistency test
v0.2.x — Add FDA/TFDA mocked query metadata consistency smoke
v0.2.x — Add release/tag/project-state handoff checklist
```

Avoid vague next steps such as:

```text
Improve system
Add more sources
Build dashboard
Add automation
```

Those are too broad for a controlled release increment.

## 14. Stop conditions

Stop and inspect before continuing if:

- Terminal paste appears garbled.
- `git status --short` shows unexpected files.
- PR diff includes unrelated files.
- A tag points to the wrong commit.
- Project state contradicts the actual merged/tagged state.
- A tool or script modifies files outside the intended scope.

Use the smallest safe recovery step first, such as checking status or diff, instead of applying another large script.
