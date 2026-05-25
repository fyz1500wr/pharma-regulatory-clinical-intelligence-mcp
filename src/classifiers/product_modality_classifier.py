import re
from pathlib import Path
try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

DEFAULT = "unknown"
FALLBACK_MAPPING = {
    "antibody": ["monoclonal antibody", "mab"],
    "adc": ["adc", "antibody-drug conjugate"],
    "small_molecule": ["small molecule"],
}


def load_keyword_mapping(path: str = "config/taxonomy/product_modality_keywords.yaml") -> dict[str, list[str]]:
    try:
        p = Path(path)
        if p.exists() and yaml is not None:
            loaded = yaml.safe_load(p.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                return {str(k): list(v or []) for k, v in loaded.items()}
    except Exception:
        pass
    return FALLBACK_MAPPING


def _keyword_matches(content: str, keyword: str) -> bool:
    keyword = str(keyword or "").strip().lower()
    if not keyword:
        return False
    # Match complete keyword terms. This avoids false positives for short tokens,
    # such as "nce" matching the middle of "cancer".
    pattern = rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])"
    return re.search(pattern, content) is not None


def classify_product_modality(text: str, mapping: dict[str, list[str]] | None = None) -> dict:
    content = (text or "").lower()
    mapping = mapping or load_keyword_mapping()
    for label, keywords in mapping.items():
        if label in {"unknown", "requires_manual_review"}:
            continue
        if any(_keyword_matches(content, str(k)) for k in keywords):
            return {"product_modality": [label], "classification_confidence": "medium"}
    if content.strip():
        return {"product_modality": ["requires_manual_review"], "classification_confidence": "requires_manual_review"}
    return {"product_modality": [DEFAULT], "classification_confidence": "low"}
