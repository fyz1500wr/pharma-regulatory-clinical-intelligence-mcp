from src.core.errors import ErrorCode, build_error


def search_regulatory_updates(**kwargs):
    return {"records": [], "no_result_reason": "DATA_NOT_INGESTED", "suggested_next_action": "Ingest MVP v1 FDA/TFDA data."}


def get_regulatory_document_detail(document_id: str, **kwargs):
    if not document_id:
        return build_error(ErrorCode.INVALID_PARAMETER, "document_id is required")
    return build_error(ErrorCode.DATA_NOT_INGESTED, "Document detail is not available in skeleton")


def compare_regulatory_updates(**kwargs):
    raise NotImplementedError("compare_regulatory_updates is planned after MVP v1 stabilization")
