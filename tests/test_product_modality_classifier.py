from src.classifiers.product_modality_classifier import classify_product_modality, load_keyword_mapping


def test_product_modality_field_only():
    out = classify_product_modality("This is a monoclonal antibody study")
    assert "product_modality" in out
    assert "biologic_type" not in out


def test_load_keyword_mapping_fallback_for_missing_file():
    mapping = load_keyword_mapping("config/taxonomy/not_exists.yaml")
    assert "antibody" in mapping
