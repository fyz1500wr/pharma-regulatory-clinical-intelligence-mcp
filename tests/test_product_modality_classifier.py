from src.classifiers.product_modality_classifier import classify_product_modality, load_keyword_mapping


def test_product_modality_field_only():
    out = classify_product_modality("This is a monoclonal antibody study")
    assert "product_modality" in out
    assert "biologic_type" not in out


def test_load_keyword_mapping_fallback_for_missing_file():
    mapping = load_keyword_mapping("config/taxonomy/not_exists.yaml")
    assert "antibody" in mapping


def test_nce_does_not_match_cancer():
    out = classify_product_modality("advanced cancer cohort with no explicit modality")
    modalities = out["product_modality"]
    assert "small_molecule" not in modalities


def test_small_molecule_still_matches():
    out = classify_product_modality("oral small molecule inhibitor")
    assert "small_molecule" in out["product_modality"]


def test_monoclonal_antibody_still_matches():
    out = classify_product_modality("monoclonal antibody study")
    assert "antibody" in out["product_modality"]

def test_mab_suffix_still_matches_antibody_drug_names():
    out = classify_product_modality("pembrolizumab study")
    assert "antibody" in out["product_modality"]

    out = classify_product_modality("trastuzumab combination therapy")
    assert "antibody" in out["product_modality"]
\n