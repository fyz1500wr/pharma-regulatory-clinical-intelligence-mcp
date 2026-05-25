TOPIC_KEYWORDS = {
    "CMC": ["chemistry", "manufacturing", "controls", "cmc"],
    "clinical": ["clinical", "trial", "endpoint"],
    "GMP": ["gmp", "good manufacturing"],
    "safety": ["safety", "adverse"],
    "labeling": ["label", "package insert"],
}


def classify_regulatory_topic(text: str) -> dict:
    content = (text or "").lower()
    hits = [topic for topic, keywords in TOPIC_KEYWORDS.items() if any(k in content for k in keywords)]
    if not hits:
        return {"topics": ["unknown"], "classification_confidence": "low"}
    return {"topics": hits, "classification_confidence": "medium"}
