# Open-Source Claude/Codex Skill And Tool Survey

## Purpose

This document records a docs/spec-only survey of open-source or openly documented tools, SDKs, plugins, and workflows that could support the original project requirement to evaluate tools for Claude/Codex-based development.

The goal is to help decide future workstreams without immediately installing, integrating, or approving any new tool.

This document is intentionally conservative. It does not approve runtime implementation, source expansion, MCP tool changes, scheduler, alerts, dashboard, persistence, HTTP/SSE transport, `.mcp.json`, GitHub automation, company alias database, corporate-family mapping, product ownership inference, literature/patent/finance/news integration, or CMC weekly management report work.

## Survey Date And Evidence Basis

Survey date: 2026-06-10

Evidence basis:

- Official or primary project repositories and product documentation were preferred.
- The survey focused on tools that may support the current GitHub/Codex/Claude Project workflow, MVP MCP validation, or future MCP server design.
- No package was installed, configured, or added to repository dependencies as part of this document.

## Evaluation Criteria

| Criterion | Description |
|---|---|
| Primary fit | Whether the tool supports GitHub/Codex build work, Claude Project execution, MCP testing, prompt/workflow reuse, or validation. |
| Current repo fit | Whether the tool aligns with the existing MVP v1 boundary and current Python/MCP structure. |
| Adoption risk | Risk from security, credential exposure, local installation requirements, unstable APIs, or company-device restrictions. |
| Scope impact | Whether using the tool would require runtime code, `.mcp.json`, new source connectors, scheduler, persistence, or automation. |
| Recommended disposition | Whether to keep as reference, use manually, evaluate later, or defer. |

## Candidate Matrix

| Candidate | Type | Primary fit | Current repo fit | Key benefit | Main risk / constraint | Recommended disposition |
|---|---|---|---|---|---|---|
| Model Context Protocol Python SDK / FastMCP | MCP SDK | Build and test Python MCP servers and clients. | High; the repo already exposes an MCP stdio server and uses `mcp.server.fastmcp` in tests. | Strongest match for existing MCP architecture and validation. | Any new MCP server/tool implementation would still be scope expansion. | Keep as current dependency basis; do not add new tools without approval. |
| MCP Inspector | MCP testing tool | Visual/manual testing of MCP servers. | Medium to high for future local smoke testing. | Could help test MCP server behavior before Claude Project handoff. | Requires local execution and may not be available on company-managed devices. | Reference only; consider manual validation if local execution is permitted. |
| OpenAI Codex CLI | Coding agent CLI | Supports Codex-based code editing and validation from a terminal. | Medium; useful for development workflow, not for runtime. | Could support repo maintenance, docs edits, and test-driven changes. | Requires local/terminal install; company devices may restrict installation. | Reference only; use Codex Web first under current constraints. |
| Claude Code MCP configuration and plugin workflow | Claude Code / MCP integration pattern | Shows how Claude Code can connect to MCP servers and plugin-provided MCP tools. | Medium; useful for future handoff design. | Helps evaluate whether MCP servers should be local, project-scoped, or user-scoped. | `.mcp.json` and plugin installation are explicitly not approved in this repo. | Reference only; do not add `.mcp.json` or plugins without approval. |
| pytest | Test framework | Validates repository behavior, docs index, state file consistency, and MCP wrappers. | High; already used in the repository. | Provides low-cost validation for docs/spec and code changes. | Requires dependencies such as `mcp` to be installed in fresh environments. | Continue using for validation; no new dependency change needed. |
| GitHub CLI | Developer workflow helper | Could assist branch, PR, and status checks from a terminal. | Low to medium; connector and web UI already cover most current needs. | Useful outside ChatGPT connector workflows. | Requires local installation and authentication; unnecessary for current browser-first workflow. | Defer; not needed while GitHub connector/Codex Web are sufficient. |
| markdownlint / markdownlint-cli | Documentation quality tool | Could enforce Markdown formatting. | Low to medium. | May reduce docs drift and formatting inconsistencies. | Would add new dependency/config and possibly noisy style churn. | Defer unless repeated Markdown-quality issues appear. |
| pre-commit | Local quality gate | Could run formatting/lint/test hooks before commits. | Low to medium. | Useful for developer discipline in larger code changes. | Adds local workflow complexity and may conflict with browser-only constraints. | Defer; do not add unless dependency/tooling governance is approved. |
| Playwright | Browser automation/testing | Could test official HTML pages if source expansion reaches controlled browser validation. | Low for current MVP; potentially relevant later. | Could support controlled webpage behavior checks. | High scope risk: may be mistaken for scraping or source connector implementation. | Defer; do not adopt before source-expansion and scraping-policy decisions. |
| OpenAI Agents SDK / agent workflow tools | Agent SDK | Could support future agent workflow evaluation. | Low for current MVP. | May be useful if the project later designs agentic workflow automation. | Would be runtime/architecture expansion, not needed for current docs/spec workflow. | Defer; reference only. |

## Near-Term Recommendation

Recommended near-term action:

```text
Do not install or integrate a new tool yet.
```

The current best-supported tools for this repository are:

1. `pytest` for validation.
2. Existing Python MCP SDK / FastMCP dependency path for current MCP server tests.
3. Claude Code Web / Codex Web for browser-first repo work while Codespaces quota is limited.
4. MCP Inspector only as an optional manual validation aid if a local development environment is available and explicitly permitted.

## Adoption Gates

Before any surveyed tool is adopted into the repository, confirm all of the following:

- The user explicitly approves adoption.
- The adoption does not require source expansion unless source expansion is separately approved.
- The adoption does not add new MCP tools unless the MCP tool contract is updated first.
- The adoption does not introduce `.mcp.json`, scheduler, alerts, dashboard, persistence, HTTP/SSE transport, or GitHub automation without explicit approval.
- Any new dependency or developer tool is documented with its purpose, validation command, security consideration, and rollback path.
- Company-device restrictions and browser-only workflow constraints are considered.

## Tool-Specific Notes

### Model Context Protocol Python SDK / FastMCP

This is the most relevant candidate because the current repository already exposes a local MCP stdio server and includes tests that import `mcp.server.fastmcp`. The SDK is useful for maintaining current MCP wrappers and future approved MCP server work.

No new MCP tools should be added just because the SDK exists.

### MCP Inspector

MCP Inspector may be useful for manual MCP server testing, especially when validating whether a server exposes expected tools/resources/prompts. It should remain optional and local-only unless explicitly approved.

Do not add MCP Inspector configuration, scripts, or dependency records to the repository in this workstream.

### OpenAI Codex CLI

Codex CLI may be useful for developers who can install and run local command-line tools. Under current project constraints, the preferred workflow remains Codex Web or Claude Code Web because the user's company computer may restrict software installation.

Do not add Codex CLI configuration, automation, or dependency files to this repository.

### Claude Code MCP / Plugin Workflows

Claude Code documentation describes multiple MCP server connection options and plugin-provided MCP server workflows. These are useful references for future handoff design.

However, this repository should not add `.mcp.json`, plugin files, or project-scoped MCP configuration unless explicitly approved.

## Recommended Next Follow-Up

After this survey, the next decision should be one of:

1. Keep this as reference only and return to MVP validation/handoff cleanup.
2. Create a source expansion feasibility matrix for EMA/NMPA/PMDA.
3. Create a narrow MCP validation runbook using only existing tools and no new dependencies.
4. Defer all tool adoption until a concrete blocked workflow appears.

Preferred next step after this document:

```text
Do not adopt a new tool. Use the survey to decide whether the next mainline workstream should be source expansion feasibility or MVP validation cleanup.
```

## Explicit Non-Goals

This survey does not authorize:

- Installing any new package.
- Adding any dependency file or lockfile.
- Adding or changing `.mcp.json`.
- Adding runtime code.
- Adding MCP tools.
- Adding source connectors.
- Adding scheduler, alerts, dashboard, persistence, HTTP/SSE transport, or GitHub automation.
- Adding literature, patent, finance, news, company alias, corporate-family, or product ownership integrations.
- Creating a CMC weekly management report template.
