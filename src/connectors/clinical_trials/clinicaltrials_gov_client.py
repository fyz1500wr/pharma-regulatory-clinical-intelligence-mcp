

class ClinicalTrialsGovClient:
    def __init__(self, base_url: str = "https://clinicaltrials.gov/api/v2", timeout: int = 20):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def build_studies_query(self, *, indication: str, page_size: int = 20, sponsor: str | None = None) -> dict:
        query = {"query.cond": indication, "pageSize": page_size}
        if sponsor:
            query["query.spons"] = sponsor
        return query

    def search_studies(self, *, indication: str, page_size: int = 20, sponsor: str | None = None) -> dict:
        params = self.build_studies_query(indication=indication, page_size=page_size, sponsor=sponsor)
        return {"endpoint": f"{self.base_url}/studies", "params": params, "timeout": self.timeout}
