from datetime import datetime, timezone


def generate_regulatory_digest(**kwargs):
    return {
        "digest": {
            "title": "MVP v1 Skeleton Digest",
            "date_range": kwargs.get("date_range", "1m"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "sources_searched": kwargs.get("agencies", []) + kwargs.get("registries", []),
            "search_criteria": kwargs,
            "executive_summary": "No ingested data yet.",
            "key_regulatory_updates": [],
            "key_clinical_trial_updates": [],
            "source_health_summary": {"status": "unknown", "open_failures": 0, "notes": ["Skeleton mode"]},
            "known_limitations": ["DATA_NOT_INGESTED"]
        }
    }
