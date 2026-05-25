import os


class OpenFDAClient:
    def __init__(self, base_url: str = "https://api.fda.gov", timeout: int | None = None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout or int(os.getenv("HTTP_TIMEOUT_SECONDS", "20"))
        self.api_key = os.getenv("OPENFDA_API_KEY", "")

    def build_url(self, dataset: str) -> str:
        return f"{self.base_url}/{dataset}.json"

    def fetch(self, dataset: str, params: dict | None = None) -> dict:
        query = dict(params or {})
        if self.api_key:
            query["api_key"] = self.api_key
        return {"endpoint": self.build_url(dataset), "params": query, "timeout": self.timeout}
