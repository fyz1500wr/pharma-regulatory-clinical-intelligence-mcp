

class TFDAClient:
    def __init__(self, endpoint_url: str = "https://data.fda.gov.tw", timeout: int = 20):
        self.endpoint_url = endpoint_url
        self.timeout = timeout

    def fetch(self, path: str, params: dict | None = None) -> dict:
        return {"endpoint": f"{self.endpoint_url.rstrip('/')}/{path.lstrip('/')}", "params": params or {}, "timeout": self.timeout}
