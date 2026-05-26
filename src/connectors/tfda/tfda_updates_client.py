from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urljoin

from src.classifiers.product_modality_classifier import classify_product_modality
from src.core.errors import ErrorCode, build_error


def _clean(value: object) -> str:
    return " ".join(str(value or "").split())


def _normalize_tfda_date(value: object) -> tuple[str | None, list[str]]:
    text = _clean(value)
    limitations: list[str] = []
    if not text:
        return None, limitations

    normalized = (
        text.replace("民國", "")
        .replace("年", "/")
        .replace("月", "/")
        .replace("日", "")
        .replace(".", "/")
        .replace("-", "/")
    )

    match = re.search(r"(\d{2,4})/(\d{1,2})/(\d{1,2})", normalized)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        if year < 1911:
            year += 1911
        try:
            return datetime(year, month, day).date().isoformat(), limitations
        except ValueError:
            limitations.append(f"Unable to normalize TFDA date: {text}")
            return None, limitations

    for fmt in ("%Y%m%d", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).date().isoformat(), limitations
        except ValueError:
            pass

    limitations.append(f"Unable to normalize TFDA date: {text}")
    return None, limitations


def _normalize_status(value: object) -> str:
    text = _clean(value).lower()
    if not text:
        return "published"
    if "草案" in text or "draft" in text:
        return "draft"
    if any(token in text for token in ["公告", "發布", "published", "final", "生效"]):
        return "published"
    return "unknown"


class _TFDATableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows: list[dict[str, Any]] = []
        self._headers: list[str] = []
        self._in_tr = False
        self._current_cells: list[dict[str, str]] = []
        self._current_cell: dict[str, str] | None = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "tr":
            self._in_tr = True
            self._current_cells = []
        elif self._in_tr and tag in {"th", "td"}:
            self._current_cell = {"tag": tag, "text": "", "href": ""}
        elif self._current_cell is not None and tag == "a":
            self._current_cell["href"] = attrs_dict.get("href", "")

    def handle_data(self, data):
        if self._current_cell is not None:
            text = _clean(data)
            if text:
                self._current_cell["text"] = _clean(f"{self._current_cell['text']} {text}")

    def handle_endtag(self, tag):
        if self._in_tr and tag in {"th", "td"} and self._current_cell is not None:
            self._current_cells.append(self._current_cell)
            self._current_cell = None

        if tag == "tr" and self._in_tr:
            if self._current_cells:
                if all(cell["tag"] == "th" for cell in self._current_cells):
                    self._headers = [_clean(cell["text"]).lower() for cell in self._current_cells]
                elif self._headers:
                    row = {}
                    for idx, header in enumerate(self._headers):
                        if idx < len(self._current_cells):
                            row[header] = self._current_cells[idx]
                    self.rows.append(row)
            self._in_tr = False
            self._current_cells = []


class TFDAUpdatesClient:
    def __init__(self, base_url: str = "https://www.fda.gov.tw", timeout: int = 20):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _stable_id(self, *parts: object) -> str:
        joined = "|".join(str(part or "") for part in parts)
        return hashlib.sha1(joined.encode("utf-8")).hexdigest()[:16]

    def _canonicalize_tfda_url(self, url: object) -> str:
        text = _clean(url)
        if not text:
            return ""
        return urljoin(self.base_url + "/", text)

    def _build_record(
        self,
        *,
        title: str,
        official_url: str,
        publication_date: str | None,
        document_status: str = "published",
        source_type: str = "TFDA_HTML",
        document_type: str = "regulatory_update",
        summary: str = "",
        topics: list[str] | None = None,
        known_limitations: list[str] | None = None,
    ) -> dict:
        title = _clean(title)
        official_url = self._canonicalize_tfda_url(official_url)
        topics = [topic for topic in (topics or []) if topic]
        known_limitations = list(known_limitations or [])

        if not title:
            known_limitations.append("TFDA title missing.")
        if not official_url:
            known_limitations.append("TFDA official_url missing.")
        if not publication_date:
            known_limitations.append("TFDA publication_date missing or unparseable.")

        modality_text = " ".join([title, summary, " ".join(topics)])
        modality = classify_product_modality(modality_text).get("product_modality", ["unknown"])

        return {
            "id": self._stable_id("tfda", title, official_url, publication_date or ""),
            "title": title,
            "official_url": official_url,
            "publication_date": publication_date,
            "last_update_date": None,
            "source_type": source_type,
            "document_type": document_type,
            "document_status": document_status,
            "summary": _clean(summary),
            "topics": topics or ["general"],
            "product_modality": modality or ["unknown"],
            "known_limitations": known_limitations,
        }

    def fetch_updates(self, query: str | None = None, limit: int = 20) -> dict:
        try:
            import requests
        except ImportError:
            return build_error(ErrorCode.SOURCE_UNAVAILABLE, "requests dependency unavailable")
        try:
            response = requests.get(urljoin(self.base_url + "/", "/TC/news.aspx"), timeout=self.timeout)
            response.raise_for_status()
            return {"html": response.text, "source_type": "TFDA_HTML", "query": query, "limit": limit}
        except Exception as exc:
            return build_error(ErrorCode.SOURCE_UNAVAILABLE, f"TFDA fetch failed: {exc}")

    def parse_html_updates(self, payload_or_html) -> list[dict]:
        html = payload_or_html.get("html", "") if isinstance(payload_or_html, dict) else payload_or_html or ""
        if not isinstance(html, str) or not html.strip():
            return []

        parser = _TFDATableParser()
        parser.feed(html)
        records: list[dict] = []

        for row in parser.rows:
            def cell_text(*names: str) -> str:
                for name in names:
                    for key, cell in row.items():
                        if name in key:
                            return _clean(cell.get("text", ""))
                return ""

            def cell_href(*names: str) -> str:
                for name in names:
                    for key, cell in row.items():
                        if name in key and cell.get("href"):
                            return _clean(cell.get("href", ""))
                return ""

            title = cell_text("標題", "主旨", "title", "subject")
            official_url = cell_href("標題", "主旨", "title", "subject") or cell_text("連結", "link", "url")
            date_text = cell_text("日期", "發布", "公告", "date")
            category = cell_text("分類", "類別", "category", "topic")
            status_text = cell_text("狀態", "status")
            summary = cell_text("摘要", "說明", "summary", "description")

            publication_date, limitations = _normalize_tfda_date(date_text)
            records.append(
                self._build_record(
                    title=title,
                    official_url=official_url,
                    publication_date=publication_date,
                    document_status=_normalize_status(status_text),
                    summary=summary,
                    topics=[category] if category else ["general"],
                    known_limitations=limitations,
                )
            )

        return records

    def parse_json_updates(self, payload) -> list[dict]:
        if isinstance(payload, str):
            payload = json.loads(payload)

        if isinstance(payload, dict):
            items = payload.get("items") or payload.get("data") or payload.get("results") or []
        elif isinstance(payload, list):
            items = payload
        else:
            return []

        records = []
        for item in items:
            if not isinstance(item, dict):
                continue

            title = item.get("title") or item.get("subject") or item.get("name") or ""
            official_url = item.get("official_url") or item.get("url") or item.get("link") or ""
            date_text = item.get("publication_date") or item.get("date") or item.get("publishDate") or ""
            publication_date, limitations = _normalize_tfda_date(date_text)
            topics = item.get("topics") if isinstance(item.get("topics"), list) else [item.get("category") or "general"]

            records.append(
                self._build_record(
                    title=title,
                    official_url=official_url,
                    publication_date=publication_date,
                    document_status=_normalize_status(item.get("document_status") or item.get("status")),
                    source_type="TFDA_JSON",
                    document_type=item.get("document_type", "regulatory_update"),
                    summary=item.get("summary", ""),
                    topics=topics,
                    known_limitations=limitations + item.get("known_limitations", []),
                )
            )

        return records

    def search_updates(self, query: str | None = None, source_types: list[str] | None = None, limit: int = 20) -> list[dict] | dict:
        source_types = source_types or ["TFDA_HTML"]
        records: list[dict] = []
        source_failures: list[dict] = []
        attempted_sources = 0

        if "TFDA_HTML" in source_types:
            attempted_sources += 1
            payload = self.fetch_updates(query=query, limit=limit)
            if isinstance(payload, dict) and "error" in payload:
                source_failures.append(payload["error"])
            elif isinstance(payload, dict):
                records.extend(self.parse_html_updates(payload)[:limit])

        if "TFDA_JSON" in source_types:
            attempted_sources += 1
            payload = self.fetch_updates(query=query, limit=limit)
            if isinstance(payload, dict) and "error" in payload:
                source_failures.append(payload["error"])
            else:
                records.extend(self.parse_json_updates(payload)[:limit])

        if query:
            q = query.lower().strip()
            records = [record for record in records if q in json.dumps(record, ensure_ascii=False).lower()]

        if not records and attempted_sources > 0 and len(source_failures) == attempted_sources:
            return build_error(
                ErrorCode.SOURCE_UNAVAILABLE,
                "All requested TFDA sources are unavailable",
                details={"source_failures": source_failures},
                suggested_next_action="Check TFDA source availability and connector fetch methods.",
            )

        return records[:limit]
