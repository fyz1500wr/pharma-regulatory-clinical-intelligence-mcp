
def check_source_health(**kwargs):
    return {"source_health": [], "known_limitations": ["MVP v1 skeleton: no live checks executed"]}


def list_source_failures(**kwargs):
    return {"failures": [], "summary": {"open_failure_count": 0, "critical_failure_count": 0, "known_limitations": ["No persisted events in skeleton"]}}
