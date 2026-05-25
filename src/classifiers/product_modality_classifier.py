DEFAULT = "unknown"


def load_keyword_mapping(path: str = "config/taxonomy/product_modality_keywords.yaml") -> dict[str, list[str]]:
    # MVP v1 skeleton default mapping; file loading can be added later.
    return {"antibody": ["monoclonal antibody", "mab"], "adc": ["adc", "antibody-drug conjugate"], "small_molecule": ["small molecule"]}


def classify_product_modality(text: str, mapping: dict[str, list[str]] | None = None) -> dict:
    content = (text or "").lower()
    mapping = mapping or load_keyword_mapping()
    for label, keywords in mapping.items():
        if label in {"unknown", "requires_manual_review"}:
            continue
        if any(k.lower() in content for k in keywords):
            return {"product_modality": [label], "classification_confidence": "medium"}
    if content.strip():
        return {"product_modality": ["requires_manual_review"], "classification_confidence": "requires_manual_review"}
    return {"product_modality": [DEFAULT], "classification_confidence": "low"}
