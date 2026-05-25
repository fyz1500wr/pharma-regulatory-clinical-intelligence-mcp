from src.connectors.clinical_trials.clinicaltrials_gov_client import ClinicalTrialsGovClient


def test_build_query_no_network_needed():
    client = ClinicalTrialsGovClient()
    q = client.build_studies_query(indication="NSCLC", page_size=10, sponsor="Roche")
    assert q["query.cond"] == "NSCLC"
    assert q["pageSize"] == 10
    assert q["query.spons"] == "Roche"
