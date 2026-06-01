from src.mcp_server.server import TOOL_REGISTRY


def _raw_health(source, *, available=True, error_code="", message="OK"):
    source_type = "clinical_trials_registry" if source == "ClinicalTrials.gov" else "regulatory"
    return {
        "overall_status": "available" if available else "degraded",
        "sources": [
            {
                "source": source,
                "source_type": source_type,
                "available": available,
                "retrieved_at": "2026-01-01T00:00:00+00:00",
                "error_code": error_code,
                "message": message,
                "suggested_next_action": f"Check {source} connector.",
                "known_limitations": [],
            }
        ],
        "query_metadata": {
            "known_limitations": [],
        },
    }


def test_list_source_failures_returns_empty_when_all_sources_healthy(monkeypatch):
    def fake_health_impl(source, mode):
        return _raw_health(source, available=True)

    monkeypatch.setattr("src.mcp_server.tools_healthcheck._check_source_health_impl", fake_health_impl)

    result = TOOL_REGISTRY["list_source_failures"]()

    assert result["failures"] == []
    assert result["summary"]["open_failure_count"] == 0
    assert result["summary"]["critical_failure_count"] == 0
    assert result["query_metadata"]["lookup_mode"] == "current_health_snapshot"


def test_list_source_failures_returns_failed_source_snapshot(monkeypatch):
    def fake_health_impl(source, mode):
        if source == "FDA":
            return _raw_health(source, available=False, error_code="SOURCE_UNAVAILABLE", message="FDA timeout")
        return _raw_health(source, available=True)

    monkeypatch.setattr("src.mcp_server.tools_healthcheck._check_source_health_impl", fake_health_impl)

    result = TOOL_REGISTRY["list_source_failures"]()

    assert len(result["failures"]) == 1
    failure = result["failures"][0]
    assert failure["source_id"] == "FDA_openFDA"
    assert failure["agency_or_registry"] == "FDA"
    assert failure["status"] == "open"
    assert failure["failure_type"] == "api_status"
    assert failure["severity"] == "high"
    assert "FDA timeout" in failure["error_message"]
    assert failure["suggested_connector_file"] == "src/connectors/fda/fda_updates_client.py"
    assert result["summary"]["open_failure_count"] == 1
    assert result["summary"]["high_failure_count"] == 1


def test_list_source_failures_filters_by_sources(monkeypatch):
    calls = []

    def fake_health_impl(source, mode):
        calls.append(source)
        return _raw_health(source, available=False, error_code="SOURCE_UNAVAILABLE", message=f"{source} failed")

    monkeypatch.setattr("src.mcp_server.tools_healthcheck._check_source_health_impl", fake_health_impl)

    result = TOOL_REGISTRY["list_source_failures"](sources=["TFDA_DataAction"])

    assert calls == ["TFDA"]
    assert len(result["failures"]) == 1
    assert result["failures"][0]["source_id"] == "TFDA_DataAction"
    assert result["query_metadata"]["sources_checked"] == ["TFDA_DataAction"]


def test_list_source_failures_filters_by_agencies_or_registries(monkeypatch):
    def fake_health_impl(source, mode):
        return _raw_health(source, available=False, error_code="SOURCE_UNAVAILABLE", message=f"{source} failed")

    monkeypatch.setattr("src.mcp_server.tools_healthcheck._check_source_health_impl", fake_health_impl)

    result = TOOL_REGISTRY["list_source_failures"](agencies_or_registries=["ClinicalTrials.gov"])

    assert len(result["failures"]) == 1
    assert result["failures"][0]["source_id"] == "ClinicalTrialsGov_API"
    assert result["failures"][0]["agency_or_registry"] == "ClinicalTrials.gov"


def test_list_source_failures_filters_by_failure_type(monkeypatch):
    def fake_health_impl(source, mode):
        return _raw_health(source, available=False, error_code="SOURCE_UNAVAILABLE", message=f"{source} failed")

    monkeypatch.setattr("src.mcp_server.tools_healthcheck._check_source_health_impl", fake_health_impl)

    result = TOOL_REGISTRY["list_source_failures"](failure_types=["schema_validation"])

    assert result["failures"] == []
    assert result["summary"]["open_failure_count"] == 0


def test_list_source_failures_filters_by_severity(monkeypatch):
    def fake_health_impl(source, mode):
        if source == "FDA":
            return _raw_health(source, available=False, error_code="SOURCE_UNAVAILABLE", message="FDA failed")
        return _raw_health(source, available=True)

    monkeypatch.setattr("src.mcp_server.tools_healthcheck._check_source_health_impl", fake_health_impl)

    result = TOOL_REGISTRY["list_source_failures"](severity=["critical"])

    assert result["failures"] == []
    assert result["summary"]["open_failure_count"] == 0


def test_list_source_failures_rejects_unsupported_source():
    result = TOOL_REGISTRY["list_source_failures"](sources=["EMA"])

    assert result["error"]["code"] == "INVALID_PARAMETER"
    assert "EMA" in result["error"]["message"]


def test_list_source_failures_rejects_unsupported_failure_type():
    result = TOOL_REGISTRY["list_source_failures"](failure_types=["database_down"])

    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_list_source_failures_rejects_non_boolean_include_resolved():
    result = TOOL_REGISTRY["list_source_failures"](include_resolved="yes")

    assert result["error"]["code"] == "INVALID_PARAMETER"



# --- egress policy source failure tests ---
def _egress_policy_health_result():
    return {
        "source_health": [
            {
                "source_id": "TFDA_DataAction",
                "agency_or_registry": "TFDA",
                "source_type": "API",
                "endpoint_url": "https://www.fda.gov.tw",
                "status": "failed",
                "last_successful_check": None,
                "last_checked_at": "2026-06-01T00:00:00+00:00",
                "failure_type": "egress_policy",
                "severity": "high",
                "error_message": "403 Host not in allowlist",
                "error_details": {"reason": "Host not in allowlist"},
                "suggested_fix": "Check the runtime/network egress allowlist, including Claude Code Web environment settings if applicable, and add the source host; otherwise rerun live-source validation in Codespaces/local.",
                "suggested_connector_file": "src/connectors/tfda/tfda_updates_client.py",
                "known_limitations": [
                    "Runtime network policy / egress allowlist failure means the source could not be reached from this runtime; it MUST NOT be interpreted as no matching records, no clinical trials, or no regulatory updates."
                ],
            },
            {
                "source_id": "ClinicalTrialsGov_API",
                "agency_or_registry": "ClinicalTrials.gov",
                "source_type": "API",
                "endpoint_url": "https://clinicaltrials.gov",
                "status": "failed",
                "last_successful_check": None,
                "last_checked_at": "2026-06-01T00:00:00+00:00",
                "failure_type": "api_status",
                "severity": "high",
                "error_message": "ClinicalTrials.gov timeout",
                "error_details": {"reason": "timeout"},
                "suggested_fix": "Check ClinicalTrials.gov connector runtime dependencies and API v2 availability.",
                "suggested_connector_file": "src/connectors/clinical_trials/clinicaltrials_gov_client.py",
                "known_limitations": [],
            },
        ],
        "overall_status": "degraded",
        "known_limitations": [],
        "query_metadata": {
            "sources_checked": ["TFDA_DataAction", "ClinicalTrialsGov_API"],
            "internal_sources_checked": ["TFDA", "ClinicalTrials.gov"],
        },
    }


def test_list_source_failures_filters_by_egress_policy(monkeypatch):
    from src.mcp_server import tools_healthcheck

    monkeypatch.setattr(tools_healthcheck, "check_source_health", lambda **kwargs: _egress_policy_health_result())

    result = tools_healthcheck.list_source_failures(failure_types=["egress_policy"])

    assert result["summary"]["open_failure_count"] == 1
    assert len(result["failures"]) == 1
    assert result["failures"][0]["source_id"] == "TFDA_DataAction"
    assert result["failures"][0]["failure_type"] == "egress_policy"


def test_list_source_failures_egress_policy_suspected_cause(monkeypatch):
    from src.mcp_server import tools_healthcheck

    monkeypatch.setattr(tools_healthcheck, "check_source_health", lambda **kwargs: _egress_policy_health_result())

    result = tools_healthcheck.list_source_failures(failure_types=["egress_policy"])
    suspected_cause = result["failures"][0]["suspected_cause"]

    assert "runtime network policy" in suspected_cause
    assert "NOT" in suspected_cause
    assert "no matching records" in suspected_cause


def test_list_source_failures_preserves_egress_policy_error_details(monkeypatch):
    from src.mcp_server import tools_healthcheck

    monkeypatch.setattr(tools_healthcheck, "check_source_health", lambda **kwargs: _egress_policy_health_result())

    result = tools_healthcheck.list_source_failures(failure_types=["egress_policy"])

    assert result["failures"][0]["error_details"]["reason"] == "Host not in allowlist"


def test_list_source_failures_keeps_api_status_for_generic_unavailable(monkeypatch):
    from src.mcp_server import tools_healthcheck

    monkeypatch.setattr(tools_healthcheck, "check_source_health", lambda **kwargs: _egress_policy_health_result())

    result = tools_healthcheck.list_source_failures(failure_types=["api_status"])

    assert result["summary"]["open_failure_count"] == 1
    assert result["failures"][0]["source_id"] == "ClinicalTrialsGov_API"
    assert result["failures"][0]["failure_type"] == "api_status"


def test_list_source_failures_accepts_egress_policy_failure_type_filter():
    from src.mcp_server import tools_healthcheck

    assert tools_healthcheck._validate_failure_types(["egress_policy"]) is None
