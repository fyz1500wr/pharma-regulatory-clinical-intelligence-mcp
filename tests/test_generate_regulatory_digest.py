from src.mcp_server.server import TOOL_REGISTRY


def _reg_record(title="FDA Digest Guidance", agency="FDA", topics=None, product_modality=None):
    return {
        "title": title,
        "agency": agency,
        "publication_date": "2026-01-01",
        "impact_level": "unknown",
        "official_url": "https://example.gov/regulatory-update",
        "summary": "Regulatory digest record.",
        "topics": topics or ["quality"],
        "product_modality": product_modality or ["unknown"],
    }


def _trial_record(indication="NSCLC"):
    return {
        "trial_id": "NCT00000001",
        "title": "Digest Clinical Trial",
        "sponsor": "Acme Pharma",
        "phase": "PHASE2",
        "status": "RECRUITING",
        "last_update_date": "2026-01-02",
        "official_url": "https://clinicaltrials.gov/study/NCT00000001",
        "indications": [indication],
    }


def _patch_digest_dependencies(monkeypatch, *, regulatory_records=None, trials=None, open_failures=0):
    def fake_search_regulatory_updates(**kwargs):
        return {"records": regulatory_records or [_reg_record()], "known_limitations": []}

    def fake_search_clinical_trials_by_indication(indication, **kwargs):
        return {
            "trials": trials if trials is not None else [_trial_record(indication)],
            "query_metadata": {"known_limitations": []},
        }

    def fake_check_source_health(**kwargs):
        return {"overall_status": "available", "known_limitations": []}

    def fake_list_source_failures(**kwargs):
        return {"summary": {"open_failure_count": open_failures, "known_limitations": []}}

    monkeypatch.setattr("src.mcp_server.tools_digest.search_regulatory_updates", fake_search_regulatory_updates)
    monkeypatch.setattr(
        "src.mcp_server.tools_digest.search_clinical_trials_by_indication",
        fake_search_clinical_trials_by_indication,
    )
    monkeypatch.setattr("src.mcp_server.tools_digest.check_source_health", fake_check_source_health)
    monkeypatch.setattr("src.mcp_server.tools_digest.list_source_failures", fake_list_source_failures)


def test_generate_regulatory_digest_combined_minimal_mvp(monkeypatch):
    _patch_digest_dependencies(monkeypatch)

    result = TOOL_REGISTRY["generate_regulatory_digest"](
        digest_type="combined",
        agencies=["FDA"],
        registries=["ClinicalTrials.gov"],
        indications=["NSCLC"],
        topics=["quality"],
        limit=5,
    )

    assert "error" not in result
    digest = result["digest"]
    assert digest["title"] == "MVP v1 Regulatory and Clinical Intelligence Digest"
    assert digest["sources_searched"] == ["FDA", "ClinicalTrials.gov"]
    assert digest["key_regulatory_updates"][0]["agency"] == "FDA"
    assert digest["key_clinical_trial_updates"][0]["trial_id"] == "NCT00000001"
    assert digest["source_health_summary"]["status"] == "pass"
    assert digest["source_health_summary"]["open_failures"] == 0
    assert digest["impact_matrix"]
    assert result["query_metadata"]["lookup_mode"] == "minimal_mvp_aggregation"


def test_generate_regulatory_digest_regulatory_only(monkeypatch):
    _patch_digest_dependencies(monkeypatch)

    result = TOOL_REGISTRY["generate_regulatory_digest"](
        digest_type="regulatory_update",
        agencies=["FDA"],
        topics=["quality"],
    )

    assert "error" not in result
    assert result["digest"]["key_regulatory_updates"]
    assert result["digest"]["key_clinical_trial_updates"] == []
    assert result["digest"]["sources_searched"] == ["FDA"]


def test_generate_regulatory_digest_clinical_only(monkeypatch):
    _patch_digest_dependencies(monkeypatch)

    result = TOOL_REGISTRY["generate_regulatory_digest"](
        digest_type="clinical_trial_update",
        registries=["ClinicalTrials.gov"],
        indications=["NSCLC"],
    )

    assert "error" not in result
    assert result["digest"]["key_regulatory_updates"] == []
    assert result["digest"]["key_clinical_trial_updates"]
    assert result["digest"]["sources_searched"] == ["ClinicalTrials.gov"]


def test_generate_regulatory_digest_skips_clinical_when_no_indication(monkeypatch):
    _patch_digest_dependencies(monkeypatch)

    result = TOOL_REGISTRY["generate_regulatory_digest"](
        digest_type="combined",
        agencies=["FDA"],
        registries=["ClinicalTrials.gov"],
    )

    assert "error" not in result
    assert result["digest"]["key_regulatory_updates"]
    assert result["digest"]["key_clinical_trial_updates"] == []
    assert "No indications provided; clinical trial search was skipped in MVP v1 digest." in result["digest"]["known_limitations"]


def test_generate_regulatory_digest_rejects_out_of_scope_agency():
    result = TOOL_REGISTRY["generate_regulatory_digest"](agencies=["EMA"])

    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_generate_regulatory_digest_rejects_out_of_scope_registry():
    result = TOOL_REGISTRY["generate_regulatory_digest"](registries=["WHO_ICTRP"])

    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_generate_regulatory_digest_rejects_invalid_boolean():
    result = TOOL_REGISTRY["generate_regulatory_digest"](include_impact_matrix="yes")

    assert result["error"]["code"] == "INVALID_PARAMETER"
