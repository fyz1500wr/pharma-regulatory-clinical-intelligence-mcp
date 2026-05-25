from enum import Enum


class ErrorCode(str, Enum):
    SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
    INVALID_PARAMETER = "INVALID_PARAMETER"
    NO_RESULTS = "NO_RESULTS"
    PARTIAL_RESULTS = "PARTIAL_RESULTS"
    DATA_NOT_INGESTED = "DATA_NOT_INGESTED"
    CLASSIFICATION_UNCERTAIN = "CLASSIFICATION_UNCERTAIN"
    INTERNAL_ERROR = "INTERNAL_ERROR"


def build_error(code: ErrorCode, message: str, details: str = "", suggested_next_action: str = "") -> dict:
    return {"error": {"code": code.value, "message": message, "details": details, "suggested_next_action": suggested_next_action}}
