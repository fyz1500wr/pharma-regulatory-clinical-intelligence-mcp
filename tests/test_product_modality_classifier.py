from src.classifiers.product_modality_classifier import classify_product_modality


def test_product_modality_field_only():
    out = classify_product_modality("This is a monoclonal antibody study")
    assert "product_modality" in out
    assert "biologic_type" not in out
