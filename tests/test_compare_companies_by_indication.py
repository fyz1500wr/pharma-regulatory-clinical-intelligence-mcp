from src.mcp_server.server import TOOL_REGISTRY


def _trial(
    trial_id,
    *,
    sponsor="Acme Pharma",
    phase="PHASE2",
    status="RECRUITING",
    product_modality=None,
    results_available=False,
):
    return {
        "trial_id": trial_id,
        "title": f"{sponsor} {trial_id}",
        "sponsor": sponsor,
        "phase": phase,
        "status": status,
        "last_update_date": "2026-01-02",
        "official_url": f"https://clinicaltrials.gov/study/{trial_id}",
        "intervention_names": ["test intervention"],
        "product_modality": product_modality or ["small_molecule"],
        "results_available": results_available,
    }


def _patch_company_search(monkeypatch, company_to_trials):
    def fake_search_clinical_trials_by_indication(indication, **kwargs):
        sponsor = kwargs.get("sponsor")
        return {
            "trials": company_to_trials.get(sponsor, []),
            "query_metadata": {"known_limitations": []},
        }

    monkeypatch.setattr(
        "src.mcp_server.tools_clinical_trials.search_clinical_trials_by_indication",
        fake_search_clinical_trials_by_indication,
    )


def test_compare_companies_by_indication_minimal_mvp(monkeypatch):
    _patch_company_search(
        monkeypatch,
        {
            "Acme Pharma": [
                _trial("NCT00000001", sponsor="Acme Pharma", phase="PHASE3", status="RECRUITING"),
                _trial("NCT00000002", sponsor="Acme Pharma", phase="PHASE2", status="COMPLETED"),
            ],
            "Beta Bio": [
                _trial("NCT00000003", sponsor="Beta Bio", phase="PHASE1", status="ACTIVE_NOT_RECRUITING"),
            ],
        },
    )

    result = TOOL_REGISTRY["compare_companies_by_indication"](
        indication="NSCLC",
        companies=["Acme Pharma", "Beta Bio"],
        registries=["ClinicalTrials.gov"],
    )

    assert "error" not in result
    assert result["landscape_summary"]["indication"] == "NSCLC"
    assert result["landscape_summary"]["companies_compared"] == ["Acme Pharma", "Beta Bio"]
    assert result["company_comparison"][0]["company"] == "Acme Pharma"
    assert result["company_comparison"][0]["trial_count"] == 2
    assert result["company_comparison"][0]["active_trial_count"] == 1
    assert result["company_comparison"][0]["completed_trial_count"] == 1
    assert result["company_comparison"][0]["highest_phase"] == "PHASE3"
    assert result["query_metadata"]["lookup_mode"] == "clinicaltrials_gov_sponsor_activity_mvp"


def test_compare_companies_by_indication_filters_phase_and_completed_trials(monkeypatch):
    _patch_company_search(
        monkeypatch,
        {
            "Acme Pharma": [
                _trial("NCT00000001", sponsor="Acme Pharma", phase="PHASE3", status="RECRUITING"),
                _trial("NCT00000002", sponsor="Acme Pharma", phase="PHASE2", status="COMPLETED"),
            ],
        },
    )

    result = TOOL_REGISTRY["compare_companies_by_indication"](
        indication="NSCLC",
        companies=["Acme Pharma"],
        phase=["PHASE3"],
        include_completed_trials=False,
    )

    assert "error" not in result
    comparison = result["company_comparison"][0]
    assert comparison["trial_count"] == 1
    assert comparison["key_trials"][0]["trial_id"] == "NCT00000001"


def test_compare_companies_by_indication_filters_product_modality(monkeypatch):
    _patch_company_search(
        monkeypatch,
        {
            "Acme Pharma": [
                _trial("NCT00000001", sponsor="Acme Pharma", product_modality=["small_molecule"]),
                _trial("NCT00000002", sponsor="Acme Pharma", product_modality=["antibody"]),
            ],
        },
    )

    result = TOOL_REGISTRY["compare_companies_by_indication"](
        indication="NSCLC",
        companies=["Acme Pharma"],
        product_modality=["antibody"],
    )

    assert "error" not in result
    comparison = result["company_comparison"][0]
    assert comparison["trial_count"] == 1
    assert comparison["modalities"] == ["antibody"]


def test_compare_companies_by_indication_requires_company_list():
    result = TOOL_REGISTRY["compare_companies_by_indication"](indication="NSCLC")

    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_compare_companies_by_indication_rejects_out_of_scope_registry():
    result = TOOL_REGISTRY["compare_companies_by_indication"](
        indication="NSCLC",
        companies=["Acme Pharma"],
        registries=["WHO_ICTRP"],
    )

    assert result["error"]["code"] == "INVALID_PARAMETER"


def test_compare_companies_by_indication_rejects_superiority_inference_by_design(monkeypatch):
    _patch_company_search(
        monkeypatch,
        {
            "Acme Pharma": [_trial("NCT00000001", sponsor="Acme Pharma")],
        },
    )

    result = TOOL_REGISTRY["compare_companies_by_indication"](
        indication="NSCLC",
        companies=["Acme Pharma"],
    )

    assert "error" not in result
    assert "does not rank company superiority" in " ".join(result["landscape_summary"]["data_gaps"])
    assert "should not be interpreted as clinical superiority" in result["company_comparison"][0]["summary"]
