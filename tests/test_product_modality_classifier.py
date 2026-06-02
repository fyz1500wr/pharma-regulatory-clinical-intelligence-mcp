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


def test_bilingual_product_modality_keywords_cover_mvp_labels():
    cases = [
        ("小分子藥物為 EGFR inhibitor", "small_molecule"),
        ("GLP-1 胜肽藥物開發計畫", "peptide"),
        ("反義寡核苷酸 ASO 核酸藥物", "oligonucleotide"),
        ("mRNA疫苗與信使RNA平台", "mrna_rna"),
        ("單株抗體與雙特異性抗體產品", "antibody"),
        ("抗體藥物複合體 ADC 藥物", "adc"),
        ("重組蛋白與干擾素產品", "recombinant_protein"),
        ("生物相似性藥品品質審查", "biosimilar"),
        ("治療性疫苗臨床試驗", "vaccine"),
        ("CAR-T細胞治療產品", "cell_therapy"),
        ("AAV載體基因治療產品", "gene_therapy"),
        ("放射性藥品 Lu-177 radioligand", "radiopharmaceutical"),
        ("藥械組合與預充填注射器", "combination_product"),
    ]

    for text, expected in cases:
        out = classify_product_modality(text)
        assert expected in out["product_modality"], (text, out)


def test_bilingual_adc_phrase_is_not_classified_as_plain_antibody():
    out = classify_product_modality("抗體藥物複合體 ADC")
    assert out["product_modality"] == ["adc"]


def test_bilingual_mrna_vaccine_prioritizes_mrna_rna_over_general_vaccine():
    out = classify_product_modality("mRNA疫苗")
    assert out["product_modality"] == ["mrna_rna"]


def test_bilingual_unknown_content_still_requires_manual_review():
    out = classify_product_modality("未明確說明產品類型的公告")
    assert out["product_modality"] == ["requires_manual_review"]
