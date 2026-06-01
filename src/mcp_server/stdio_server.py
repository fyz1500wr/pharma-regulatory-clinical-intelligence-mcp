"""MCP stdio transport wrapper for MVP v1 tools.

This module exposes the existing TOOL_REGISTRY functions through the official
MCP Python SDK FastMCP server.

It intentionally does not implement new business logic, new sources, HTTP/SSE
deployment, persistence, scheduling, alerting, or source expansion.
"""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from src.mcp_server.server import TOOL_REGISTRY


MCP_SERVER_NAME = "pharma-regulatory-clinical-intelligence-mcp"
MCP_TOOL_NAMES = tuple(sorted(TOOL_REGISTRY.keys()))
MCP_SERVER = FastMCP(MCP_SERVER_NAME)


def _call_tool(tool_name: str, **kwargs: Any) -> dict[str, Any]:
    """Delegate an MCP tool call to the existing Python TOOL_REGISTRY."""
    return TOOL_REGISTRY[tool_name](**kwargs)


@MCP_SERVER.tool()
def search_regulatory_updates(
    agency: str = "FDA",
    query: str | None = None,
    product_modality: list[str] | str | None = None,
    date_range: str | None = None,
    custom_date_range: dict[str, str] | None = None,
    limit: int = 20,
    source_types: list[str] | None = None,
    document_status: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> dict[str, Any]:
    """Search FDA or TFDA regulatory updates within MVP v1 scope."""
    return _call_tool(
        "search_regulatory_updates",
        agency=agency,
        query=query,
        product_modality=product_modality,
        date_range=date_range,
        custom_date_range=custom_date_range,
        limit=limit,
        source_types=source_types,
        document_status=document_status,
        date_from=date_from,
        date_to=date_to,
    )


@MCP_SERVER.tool()
def get_regulatory_document_detail(
    document_id: str,
    agency: str | None = None,
    source_types: list[str] | None = None,
    limit: int = 100,
) -> dict[str, Any]:
    """Return structured detail for a regulatory document found by search."""
    return _call_tool(
        "get_regulatory_document_detail",
        document_id=document_id,
        agency=agency,
        source_types=source_types,
        limit=limit,
    )


@MCP_SERVER.tool()
def compare_regulatory_updates(
    agencies: list[str] | None = None,
    comparison_axis: str = "agency",
    query: str | None = None,
    keywords: list[str] | str | None = None,
    topics: list[str] | None = None,
    product_modality: list[str] | None = None,
    document_status: str | None = None,
    source_types: list[str] | None = None,
    limit: int = 20,
    date_range: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    custom_date_range: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Compare FDA and TFDA regulatory update activity within MVP v1 scope."""
    return _call_tool(
        "compare_regulatory_updates",
        agencies=agencies,
        comparison_axis=comparison_axis,
        query=query,
        keywords=keywords,
        topics=topics,
        product_modality=product_modality,
        document_status=document_status,
        source_types=source_types,
        limit=limit,
        date_range=date_range,
        date_from=date_from,
        date_to=date_to,
        start_date=start_date,
        end_date=end_date,
        custom_date_range=custom_date_range,
    )


@MCP_SERVER.tool()
def search_clinical_trials_by_indication(
    indication: str,
    page_size: int = 20,
    sponsor: str | None = None,
    phase: str | None = None,
    status: str | None = None,
    page_token: str | None = None,
) -> dict[str, Any]:
    """Search ClinicalTrials.gov trial activity for an indication."""
    return _call_tool(
        "search_clinical_trials_by_indication",
        indication=indication,
        page_size=page_size,
        sponsor=sponsor,
        phase=phase,
        status=status,
        page_token=page_token,
    )


@MCP_SERVER.tool()
def compare_companies_by_indication(
    indication: str,
    companies: list[str],
    registries: list[str] | None = None,
    date_range: str = "3y",
    product_modality: list[str] | None = None,
    phase: list[str] | None = None,
    include_completed_trials: bool = True,
    include_results: bool = True,
    page_size: int = 20,
) -> dict[str, Any]:
    """Compare sponsor-name-based ClinicalTrials.gov activity only."""
    return _call_tool(
        "compare_companies_by_indication",
        indication=indication,
        companies=companies,
        registries=registries,
        date_range=date_range,
        product_modality=product_modality,
        phase=phase,
        include_completed_trials=include_completed_trials,
        include_results=include_results,
        page_size=page_size,
    )


@MCP_SERVER.tool()
def check_source_health(
    source: str | None = None,
    sources: list[str] | None = None,
    mode: str = "limited_live_connector_check",
) -> dict[str, Any]:
    """Check current source or connector health for MVP v1 sources."""
    return _call_tool(
        "check_source_health",
        source=source,
        sources=sources,
        mode=mode,
    )


@MCP_SERVER.tool()
def list_source_failures(
    source: str | None = None,
    sources: list[str] | None = None,
    agencies_or_registries: list[str] | None = None,
    failure_types: list[str] | None = None,
    severity: list[str] | None = None,
    include_resolved: bool = False,
    date_range: str | None = None,
    mode: str = "limited_live_connector_check",
) -> dict[str, Any]:
    """List current source failures derived from source health checks."""
    return _call_tool(
        "list_source_failures",
        source=source,
        sources=sources,
        agencies_or_registries=agencies_or_registries,
        failure_types=failure_types,
        severity=severity,
        include_resolved=include_resolved,
        date_range=date_range,
        mode=mode,
    )


@MCP_SERVER.tool()
def generate_regulatory_digest(
    digest_type: str = "combined",
    agencies: list[str] | None = None,
    registries: list[str] | None = None,
    topics: list[str] | None = None,
    indications: list[str] | None = None,
    companies: list[str] | None = None,
    product_modality: list[str] | None = None,
    limit: int = 5,
    date_range: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    include_impact_matrix: bool = True,
    include_source_health_summary: bool = True,
) -> dict[str, Any]:
    """Generate a rule-based MVP v1 regulatory-clinical digest."""
    return _call_tool(
        "generate_regulatory_digest",
        digest_type=digest_type,
        agencies=agencies,
        registries=registries,
        topics=topics,
        indications=indications,
        companies=companies,
        product_modality=product_modality,
        limit=limit,
        date_range=date_range,
        date_from=date_from,
        date_to=date_to,
        start_date=start_date,
        end_date=end_date,
        include_impact_matrix=include_impact_matrix,
        include_source_health_summary=include_source_health_summary,
    )


def main() -> None:
    """Run the MCP server using stdio transport."""
    MCP_SERVER.run(transport="stdio")


if __name__ == "__main__":
    main()
