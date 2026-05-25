from src.classifiers.product_modality_classifier import classify_product_modality, load_keyword_mapping


def test_product_modality_field_only():
    out = classify_product_modality("This is a monoclonal antibody study")
    assert "product_modality" in out
    assert "biologic_type" not in out


def test_load_keyword_mapping_fallback_for_missing_file():
    mapping = load_keyword_mapping("config/taxonomy/not_exists.yaml")
    assert "antibody" in mapping


def test_keyword_nce_does_not_match_cancer():
    out = classify_product_modality("advanced cancer population", mapping={"small_molecule": ["nce"]})
    assert out["product_modality"] != ["small_molecule"]


def test_small_molecule_keyword_still_matches():
    out = classify_product_modality("small molecule inhibitor", mapping={"small_molecule": ["small molecule"]})
    assert out["product_modality"] == ["small_molecule"]


def test_monoclonal_antibody_keyword_still_matches():
    out = classify_product_modality("monoclonal antibody therapy", mapping={"antibody": ["monoclonal antibody"]})
    assert out["product_modality"] == ["antibody"]
