from src.core.errors import ErrorCode, build_error


class ClinicalTrialsGovClient:
    def __init__(self, base_url: str = "https://clinicaltrials.gov/api/v2", timeout: int = 20):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def build_studies_query(
        self,
        *,
        indication: str,
        page_size: int = 20,
        sponsor: str | None = None,
        phase: list[str] | None = None,
        status: list[str] | None = None,
        page_token: str | None = None,
        fields: list[str] | None = None,
    ) -> dict:
        query = {"query.cond": indication, "pageSize": page_size}
        if sponsor:
            query["query.spons"] = sponsor
        # Conservative mapping for API v2 filters; keep explicit until stricter syntax is finalized.
        if phase:
            query["query.term"] = " AND ".join([f"AREA[Phase]{p}" for p in phase])
        if status:
            status_filter = " OR ".join(status)
            query["filter.overallStatus"] = status_filter
        if page_token:
            query["pageToken"] = page_token
        if fields:
            query["fields"] = ",".join(fields)
        return query

    def search_studies(
        self,
        *,
        indication: str,
        page_size: int = 20,
        sponsor: str | None = None,
        phase: list[str] | None = None,
        status: list[str] | None = None,
        page_token: str | None = None,
    ) -> dict:
        endpoint = f"{self.base_url}/studies"
        params = self.build_studies_query(
            indication=indication,
            page_size=page_size,
            sponsor=sponsor,
            phase=phase,
            status=status,
            page_token=page_token,
        )
        try:
            import requests
        except ModuleNotFoundError as exc:
            return build_error(
                ErrorCode.SOURCE_UNAVAILABLE,
                "requests dependency is not available for ClinicalTrials.gov client",
                details=str(exc),
                suggested_next_action="Install project dependencies before running live ClinicalTrials.gov queries.",
            )

        try:
            response = requests.get(endpoint, params=params, timeout=self.timeout)
        except requests.RequestException as exc:
            return build_error(
                ErrorCode.SOURCE_UNAVAILABLE,
                "ClinicalTrials.gov request failed",
                details=str(exc),
                suggested_next_action="Retry later or verify ClinicalTrials.gov API availability.",
            )

        if response.status_code >= 400:
            return build_error(
                ErrorCode.SOURCE_UNAVAILABLE,
                "ClinicalTrials.gov returned non-success status",
                details=f"HTTP {response.status_code}",
                suggested_next_action="Retry later or verify API endpoint/query parameters.",
            )

        try:
            payload = response.json()
        except ValueError as exc:
            return build_error(
                ErrorCode.INTERNAL_ERROR,
                "ClinicalTrials.gov response JSON decoding failed",
                details=str(exc),
                suggested_next_action="Validate upstream response format before processing.",
            )

        return payload

    def iter_studies(
        self,
        *,
        indication: str,
        max_pages: int = 1,
        page_size: int = 20,
        sponsor: str | None = None,
        phase: list[str] | None = None,
        status: list[str] | None = None,
    ) -> list[dict]:
        studies: list[dict] = []
        page_token: str | None = None

        for _ in range(max_pages):
            result = self.search_studies(
                indication=indication,
                page_size=page_size,
                sponsor=sponsor,
                phase=phase,
                status=status,
                page_token=page_token,
            )
            if "error" in result:
                break
            page_studies = result.get("studies", [])
            if not isinstance(page_studies, list):
                break
            studies.extend(page_studies)
            page_token = result.get("nextPageToken")
            if not page_token:
                break

        return studies
