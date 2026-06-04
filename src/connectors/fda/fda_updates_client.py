from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

from src.classifiers.product_modality_classifier import classify_product_modality
from src.core.errors import ErrorCode, build_error


def _clean(value: object) -> str:
    return " ".join(str(value or "").split())


def _looks_like_fda_abuse_detection(*values: object) -> bool:
    text = " ".join(_clean(value).lower() for value in values if value is not None)
    return any(
        pattern in text
        for pattern in (
            "apology_objects",
            "abuse-detection-apology",
            "abuse detection",
        )
    )


def _normalize_status(value: object) -> str:
    text = _clean(value).lower()
    if "draft" in text:
        return "draft"
    if "final" in text:
        return "final"
    return "unknown"


def _normalize_date(value: object) -> tuple[str | None, list[str]]:
    text = _clean(value)
    limitations: list[str] = []
    if not text:
        return None, limitations

    formats = ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y", "%m/%d/%Y", "%d %b %Y")
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).date().isoformat(), limitations
        except ValueError:
            pass

    try:
        return parsedate_to_datetime(text).date().isoformat(), limitations
    except Exception:
        limitations.append(f"Unable to normalize FDA date: {text}")
        return None, limitations


class _GuidanceHTMLParser(HTMLParser):
    """Small stdlib parser for fixture-first FDA guidance pages.

    Supports:
    - simplified article fixtures from MVP v1
    - table-like guidance search fixtures closer to FDA Guidance Search pages
    """

    def __init__(self):
        super().__init__()
        self.article_items: list[dict[str, Any]] = []
        self.table_rows: list[dict[str, Any]] = []
        self._current_article: dict[str, Any] | None = None
        self._article_field: str | None = None

        self._in_tr = False
        self._current_cells: list[dict[str, str]] = []
        self._current_cell: dict[str, str] | None = None
        self._current_cell_tag: str | None = None
        self._headers: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = set(str(attrs_dict.get("class", "")).split())

        if tag == "article" and "guidance-item" in classes:
            self._current_article = {"known_limitations": []}

        if self._current_article is not None:
            if tag == "a" and "guidance-link" in classes:
                self._article_field = "title"
                self._current_article["official_url"] = attrs_dict.get("href", "")
            elif tag == "time":
                if attrs_dict.get("datetime"):
                    self._current_article["publication_date"] = attrs_dict["datetime"]
                    self._article_field = None
                else:
                    self._article_field = "publication_date"
            elif tag == "p" and "summary" in classes:
                self._article_field = "summary"
            elif tag == "span" and "status" in classes:
                self._article_field = "document_status"

        if tag == "tr":
            self._in_tr = True
            self._current_cells = []
        elif self._in_tr and tag in {"td", "th"}:
            self._current_cell = {"text": "", "href": "", "tag": tag}
            self._current_cell_tag = tag
        elif self._current_cell is not None and tag == "a":
            self._current_cell["href"] = attrs_dict.get("href", "")

    def handle_data(self, data):
        text = _clean(data)
        if not text:
            return

        if self._current_article is not None and self._article_field:
            self._current_article[self._article_field] = _clean(
                f"{self._current_article.get(self._article_field, '')} {text}"
            )

        if self._current_cell is not None:
            self._current_cell["text"] = _clean(f"{self._current_cell.get('text', '')} {text}")

    def handle_endtag(self, tag):
        if tag in {"a", "time", "p", "span"}:
            self._article_field = None

        if tag == "article" and self._current_article is not None:
            self.article_items.append(self._current_article)
            self._current_article = None

        if self._in_tr and tag in {"td", "th"} and self._current_cell is not None:
            self._current_cells.append(self._current_cell)
            self._current_cell = None
            self._current_cell_tag = None

        if tag == "tr" and self._in_tr:
            if self._current_cells:
                if all(cell.get("tag") == "th" for cell in self._current_cells):
                    self._headers = [_clean(cell.get("text")).lower() for cell in self._current_cells]
                elif self._headers:
                    row = {}
                    for idx, header in enumerate(self._headers):
                        if idx < len(self._current_cells):
                            row[header] = self._current_cells[idx]
                    self.table_rows.append(row)
            self._in_tr = False
            self._current_cells = []


class FDAUpdatesClient:
    def __init__(self, base_url: str = "https://www.fda.gov", timeout: int = 20):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _stable_id(self, *parts: str) -> str:
        return hashlib.sha1("|".join(str(p or "") for p in parts).encode("utf-8")).hexdigest()[:16]

    def _canonicalize_fda_url(self, url: object) -> str:
        text = _clean(url)
        if not text:
            return ""
        return urljoin(self.base_url + "/", text)

    def _status_and_date(self, status_value: object, date_value: object) -> tuple[str, str | None, list[str]]:
        status = _normalize_status(status_value)
        date, limitations = _normalize_date(date_value)
        return status, date, limitations

    def _request_failure_details(
        self,
        *,
        requested_url: str,
        response: Any | None = None,
        exception: Exception | None = None,
    ) -> dict[str, Any]:
        response = response or getattr(exception, "response", None)
        final_url = getattr(response, "url", None)
        status_code = getattr(response, "status_code", None)
        body = getattr(response, "text", "") if response is not None else ""
        detected_source_block = _looks_like_fda_abuse_detection(final_url, body, exception)

        details: dict[str, Any] = {"requested_url": requested_url}
        if final_url:
            details["final_url"] = final_url
        if status_code is not None:
            details["status_code"] = status_code
        if detected_source_block:
            details["detected_source_block"] = True
            details["redirected_to_abuse_detection"] = True
            details["source_block_reason"] = "FDA abuse-detection/apology path indicated by final URL or response body."
        if exception is not None:
            details["exception_type"] = type(exception).__name__
            details["exception_message"] = str(exception)
        return details

    def _build_abuse_detection_error(self, *, source_name: str, requested_url: str, response: Any) -> dict:
        return build_error(
            ErrorCode.SOURCE_UNAVAILABLE,
            f"FDA {source_name} fetch blocked by FDA abuse-detection/apology response",
            details=self._request_failure_details(requested_url=requested_url, response=response),
            suggested_next_action="Retry later from an allowed network or verify FDA source access before treating this as no matching records.",
        )

    def _build_guidance_record(
        self,
        *,
        title: str,
        official_url: str,
        publication_date: str | None,
        document_status: str,
        summary: str = "",
        topics: list[str] | None = None,
        known_limitations: list[str] | None = None,
    ) -> dict:
        title = _clean(title)
        official_url = self._canonicalize_fda_url(official_url)
        topics = [topic for topic in (topics or []) if topic]
        known_limitations = list(known_limitations or [])

        if not title:
            known_limitations.append("FDA guidance title missing.")
        if not official_url:
            known_limitations.append("FDA guidance official_url missing.")
        if not publication_date:
            known_limitations.append("FDA guidance publication_date missing or unparseable.")

        modality_text = " ".join([title, summary, " ".join(topics)])
        modality = classify_product_modality(modality_text).get("product_modality", ["unknown"])

        return {
            "id": self._stable_id("guidance", title, official_url, publication_date or ""),
            "title": title,
            "official_url": official_url,
            "publication_date": publication_date,
            "last_update_date": None,
            "source_type": "FDA_GUIDANCE",
            "document_type": "guidance",
            "document_status": document_status or "unknown",
            "summary": _clean(summary),
            "topics": topics or ["general"],
            "product_modality": modality or ["unknown"],
            "known_limitations": known_limitations,
        }

    def fetch_guidance_documents(self, query: str | None = None, limit: int = 20) -> dict:
        try:
            import requests
        except ImportError:
            return build_error(ErrorCode.SOURCE_UNAVAILABLE, "requests dependency unavailable")

        requested_url = urljoin(self.base_url + "/", "/drugs/guidance-compliance-regulatory-information")
        resp = None
        try:
            resp = requests.get(
                requested_url,
                timeout=self.timeout,
            )
            resp.raise_for_status()
            if _looks_like_fda_abuse_detection(getattr(resp, "url", None), getattr(resp, "text", "")):
                return self._build_abuse_detection_error(
                    source_name="guidance",
                    requested_url=requested_url,
                    response=resp,
                )
            return {"html": resp.text, "retrieved_at": self._now(), "source_type": "official_html", "limit": limit, "query": query}
        except Exception as exc:
            return build_error(
                ErrorCode.SOURCE_UNAVAILABLE,
                f"FDA guidance fetch failed: {exc}",
                details=self._request_failure_details(
                    requested_url=requested_url,
                    response=resp,
                    exception=exc,
                ),
            )

    def parse_guidance_documents(self, payload_or_html) -> list[dict]:
        try:
            html = payload_or_html.get("html", "") if isinstance(payload_or_html, dict) else payload_or_html or ""
            if not isinstance(html, str) or not html.strip():
                return []

            parser = _GuidanceHTMLParser()
            parser.feed(html)
            records: list[dict] = []

            for item in parser.article_items:
                status, date, limitations = self._status_and_date(item.get("document_status"), item.get("publication_date"))
                limitations.extend(item.get("known_limitations", []))
                records.append(
                    self._build_guidance_record(
                        title=item.get("title", ""),
                        official_url=item.get("official_url", ""),
                        publication_date=date,
                        document_status=status,
                        summary=item.get("summary", ""),
                        topics=["general"],
                        known_limitations=limitations,
                    )
                )

            for row in parser.table_rows:
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

                title = cell_text("title")
                url = cell_href("title") or cell_text("url", "link")
                status_text = cell_text("status")
                date_text = cell_text("issue date", "issued date", "date")
                org = cell_text("organization")
                product = cell_text("product")
                topic = cell_text("topic")
                doc_type = cell_text("document type")
                summary = cell_text("summary", "description")

                status, date, limitations = self._status_and_date(status_text, date_text)
                topics = [value for value in [org, product, topic, doc_type] if value]

                records.append(
                    self._build_guidance_record(
                        title=title,
                        official_url=url,
                        publication_date=date,
                        document_status=status,
                        summary=summary,
                        topics=topics,
                        known_limitations=limitations,
                    )
                )

            return records
        except Exception:
            return []

    def fetch_rss_feed(self, feed_url: str, limit: int = 20) -> dict:
        try:
            import requests
        except ImportError:
            return build_error(ErrorCode.SOURCE_UNAVAILABLE, "requests dependency unavailable")

        resp = None
        try:
            resp = requests.get(feed_url, timeout=self.timeout)
            resp.raise_for_status()
            if _looks_like_fda_abuse_detection(getattr(resp, "url", None), getattr(resp, "text", "")):
                return self._build_abuse_detection_error(
                    source_name="RSS",
                    requested_url=feed_url,
                    response=resp,
                )
            return {"xml": resp.text, "retrieved_at": self._now(), "source_type": "RSS", "limit": limit}
        except Exception as exc:
            return build_error(
                ErrorCode.SOURCE_UNAVAILABLE,
                f"FDA RSS fetch failed: {exc}",
                details=self._request_failure_details(
                    requested_url=feed_url,
                    response=resp,
                    exception=exc,
                ),
            )

    def parse_rss_items(self, xml_text: str) -> list[dict]:
        if not xml_text or not isinstance(xml_text, str):
            return []
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return []

        items = []
        for item in root.findall(".//item"):
            title = _clean(item.findtext("title"))
            link = self._canonicalize_fda_url(item.findtext("link"))
            pub_date_raw = _clean(item.findtext("pubDate"))
            pub_date, limitations = _normalize_date(pub_date_raw)
            desc = _clean(item.findtext("description"))
            if not desc:
                limitations.append("RSS description missing or empty.")

            modality = classify_product_modality(" ".join([title, desc])).get("product_modality", ["unknown"])

            items.append({
                "id": self._stable_id("rss", title, link, pub_date or pub_date_raw),
                "title": title,
                "official_url": link,
                "publication_date": pub_date,
                "last_update_date": None,
                "source_type": "FDA_RSS",
                "document_type": "news_update",
                "document_status": "unknown",
                "summary": desc,
                "topics": ["general"],
                "product_modality": modality or ["unknown"],
                "known_limitations": limitations + ["RSS description may be abbreviated."],
            })
        return items

    def search_updates(self, query: str | None = None, source_types: list[str] | None = None, limit: int = 20) -> list[dict] | dict:
        source_types = source_types or ["FDA_GUIDANCE", "FDA_RSS"]
        records: list[dict] = []
        source_failures: list[dict] = []
        attempted_sources = 0

        if "FDA_GUIDANCE" in source_types:
            attempted_sources += 1
            guidance_payload = self.fetch_guidance_documents(query=query, limit=limit)
            if isinstance(guidance_payload, dict) and "error" in guidance_payload:
                source_failures.append(guidance_payload["error"])
            elif isinstance(guidance_payload, dict):
                records.extend(self.parse_guidance_documents(guidance_payload)[:limit])

        if "FDA_RSS" in source_types:
            attempted_sources += 1
            rss_payload = self.fetch_rss_feed(
                urljoin(self.base_url + "/", "/about-fda/contact-fda/stay-informed/rss-feeds/whats-new-drug-rss-feed"),
                limit=limit,
            )
            if isinstance(rss_payload, dict) and "error" in rss_payload:
                source_failures.append(rss_payload["error"])
            elif isinstance(rss_payload, dict):
                records.extend(self.parse_rss_items(rss_payload.get("xml", ""))[:limit])

        if query:
            q = query.lower().strip()
            records = [record for record in records if q in json.dumps(record).lower()]

        if source_failures and records:
            messages = [str(err.get("message", err)) for err in source_failures]
            for record in records:
                record.setdefault("known_limitations", []).append("Partial FDA source failure: " + " | ".join(messages))

        if not records and attempted_sources > 0 and len(source_failures) == attempted_sources:
            return build_error(
                ErrorCode.SOURCE_UNAVAILABLE,
                "All requested FDA sources are unavailable",
                details={"source_failures": source_failures},
                suggested_next_action="Check FDA source availability and connector fetch methods.",
            )

        return records[:limit]
