from src.mcp_server.tools_regulatory import search_regulatory_updates, get_regulatory_document_detail, compare_regulatory_updates
from src.mcp_server.tools_clinical_trials import search_clinical_trials_by_indication, compare_companies_by_indication
from src.mcp_server.tools_healthcheck import check_source_health, list_source_failures
from src.mcp_server.tools_digest import generate_regulatory_digest


TOOL_REGISTRY = {
    "search_regulatory_updates": search_regulatory_updates,
    "get_regulatory_document_detail": get_regulatory_document_detail,
    "compare_regulatory_updates": compare_regulatory_updates,
    "search_clinical_trials_by_indication": search_clinical_trials_by_indication,
    "compare_companies_by_indication": compare_companies_by_indication,
    "check_source_health": check_source_health,
    "list_source_failures": list_source_failures,
    "generate_regulatory_digest": generate_regulatory_digest,
}
