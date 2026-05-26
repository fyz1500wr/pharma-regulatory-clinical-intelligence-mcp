from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

from src.core.errors import ErrorCode, build_error


class _GuidanceHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items: list[dict[str, Any]] = []
        self._current: dict[str, Any] | None = None
        self._field: str | None = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "article" and attrs_dict.get("class") == "guidance-item":
            self._current = {"known_limitations": []}
        if not self._current:
            return
        if tag == "a" and attrs_dict.get("class") == "guidance-link":
            self._field = "title"
            self._current["official_url"] = attrs_dict.get("href", "")
        elif tag == "time":
            self._field = "publication_date"
            if attrs_dict.get("datetime"):
                self._current["publication_date"] = attrs_dict["datetime"]
        elif tag == "p" and attrs_dict.get("class") == "summary":
            self._field = "summary"
        elif tag == "span" and attrs_dict.get("class") == "status":
            self._field = "document_status"

    def handle_data(self, data):
        if self._current is not None and self._field:
            text = data.strip()
            if text:
                self._current[self._field] = f"{self._current.get(self._field, '')} {text}".strip()

    def handle_endtag(self, tag):
        if tag in {"a", "time", "p", "span"}:
            self._field = None
        if tag == "article" and self._current is not None:
            self.items.append(self._current)
            self._current = None


class FDAUpdatesClient:
    def __init__(self, base_url: str = "https://www.fda.gov", timeout: int = 20):
        self.base_url = base_url
        self.timeout = timeout

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _stable_id(self, *parts: str) -> str:
        return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:16]

    def fetch_guidance_documents(self, query: str | None = None, limit: int = 20) -> dict:
        try:
            import requests
        except ImportError:
            return build_error(ErrorCode.SOURCE_UNAVAILABLE, "requests dependency unavailable")
        try:
            resp = requests.get(urljoin(self.base_url, "/drugs/guidance-compliance-regulatory-information"), timeout=self.timeout)
            resp.raise_for_status()
            return {"html": resp.text, "retrieved_at": self._now(), "source_type": "official_html", "limit": limit, "query": query}
        except Exception as exc:
            return build_error(ErrorCode.SOURCE_UNAVAILABLE, f"FDA guidance fetch failed: {exc}")

    def parse_guidance_documents(self, payload_or_html) -> list[dict]:
        try:
            if isinstance(payload_or_html, dict):
                html = payload_or_html.get("html", "")
            else:
                html = payload_or_html or ""
            if not isinstance(html, str) or not html.strip():
                return []
            parser = _GuidanceHTMLParser()
            parser.feed(html)
            records = []
            for item in parser.items:
                url = item.get("official_url", "")
                title = item.get("title", "").strip()
                record = {
                    "id": self._stable_id("guidance", title, url),
                    "title": title,
                    "official_url": urljoin(self.base_url, url),
                    "publication_date": item.get("publication_date"),
                    "last_update_date": None,
                    "source_type": "FDA_GUIDANCE",
                    "document_type": "guidance",
                    "document_status": (item.get("document_status", "unknown") or "unknown").lower(),
                    "summary": item.get("summary", ""),
                    "topics": ["general"],
                    "product_modality": ["unknown"],
                    "known_limitations": item.get("known_limitations", []),
                }
                records.append(record)
            return records
        except Exception:
            return []

    def fetch_rss_feed(self, feed_url: str, limit: int = 20) -> dict:
        try:
            import requests
        except ImportError:
            return build_error(ErrorCode.SOURCE_UNAVAILABLE, "requests dependency unavailable")
        try:
            resp = requests.get(feed_url, timeout=self.timeout)
            resp.raise_for_status()
            return {"xml": resp.text, "retrieved_at": self._now(), "source_type": "RSS", "limit": limit}
        except Exception as exc:
            return build_error(ErrorCode.SOURCE_UNAVAILABLE, f"FDA RSS fetch failed: {exc}")

    def parse_rss_items(self, xml_text: str) -> list[dict]:
        if not xml_text or not isinstance(xml_text, str):
            return []
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return []
        items = []
        for item in root.findall(".//item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            pub_date = (item.findtext("pubDate") or "").strip()
            desc = (item.findtext("description") or "").strip()
            items.append({
                "id": self._stable_id("rss", title, link, pub_date),
                "title": title,
                "official_url": link,
                "publication_date": pub_date or None,
                "last_update_date": None,
                "source_type": "FDA_RSS",
                "document_type": "news_update",
                "document_status": "unknown",
                "summary": desc,
                "topics": ["general"],
                "product_modality": ["unknown"],
                "known_limitations": ["RSS description may be abbreviated."],
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
                urljoin(self.base_url, "/about-fda/contact-fda/stay-informed/rss-feeds/whats-new-drug-rss-feed"),
                limit=limit,
            )
            if isinstance(rss_payload, dict) and "error" in rss_payload:
                source_failures.append(rss_payload["error"])
            elif isinstance(rss_payload, dict):
                records.extend(self.parse_rss_items(rss_payload.get("xml", ""))[:limit])

        if query:
            q = query.lower().strip()
            records = [r for r in records if q in json.dumps(r).lower()]

        if not records and attempted_sources > 0 and len(source_failures) == attempted_sources:
            return build_error(
                ErrorCode.SOURCE_UNAVAILABLE,
                "All requested FDA sources are unavailable",
                details={"source_failures": source_failures},
                suggested_next_action="Check FDA source availability and connector fetch methods.",
            )

        return records[:limit]
