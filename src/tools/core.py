"""CORE SearchAdapter (v3 works search JSON, optional key)."""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

CORE_WORKS = "https://api.core.ac.uk/v3/search/works"


class CoreAdapter:
    """CORE works search. No key required; CORE_API_KEY used if set."""

    name = "core"
    endpoint = CORE_WORKS

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?q={quote(q)}&limit={limit}"
        headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
        key = (os.environ.get("CORE_API_KEY") or "").strip()
        if key:
            headers["Authorization"] = f"Bearer {key}"
        req = Request(url, headers=headers)
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_core_payload(payload, limit=limit)


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = payload.get("results") or payload.get("data") or payload.get("hits") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    if isinstance(rows, dict):
        inner = rows.get("hits") or rows.get("results") or []
        if isinstance(inner, list):
            return [item for item in inner if isinstance(item, dict)]
    return []


def _title(row: dict) -> str:
    return str(row.get("title") or row.get("name") or "").strip()


def _authors(row: dict) -> str:
    raw = row.get("authors") or row.get("author") or []
    if isinstance(raw, str):
        parts = [p.strip() for p in raw.replace(";", ",").split(",") if p.strip()]
        return ", ".join(parts[:3])
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:3]:
        if isinstance(item, dict):
            name = str(item.get("name") or item.get("fullName") or "").strip()
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def _year(row: dict) -> str:
    raw = row.get("yearPublished") or row.get("year") or row.get("publishedDate") or ""
    text = str(raw).strip()
    return text[:4] if text[:4].isdigit() else text


def _doi(row: dict) -> str:
    doi = str(row.get("doi") or row.get("DOI") or "").strip()
    if doi:
        return doi.removeprefix("https://doi.org/")
    identifiers = row.get("identifiers") or []
    if isinstance(identifiers, list):
        for item in identifiers:
            if not isinstance(item, dict):
                continue
            kind = str(item.get("type") or item.get("scheme") or "").lower()
            value = str(item.get("identifier") or item.get("value") or "").strip()
            if "doi" in kind and value:
                return value.removeprefix("https://doi.org/")
    return ""


def _url(row: dict, doi: str) -> str:
    download = str(row.get("downloadUrl") or row.get("download_url") or "").strip()
    if download.startswith("http"):
        return download
    source_urls = row.get("sourceFulltextUrls") or row.get("links") or []
    if isinstance(source_urls, str) and source_urls.startswith("http"):
        return source_urls
    if isinstance(source_urls, list):
        for item in source_urls:
            if isinstance(item, str) and item.startswith("http"):
                return item
            if isinstance(item, dict):
                href = str(item.get("url") or item.get("href") or "").strip()
                if href.startswith("http"):
                    return href
    if doi:
        return f"https://doi.org/{doi}"
    ident = str(row.get("id") or row.get("coreId") or "").strip()
    if ident.startswith("http"):
        return ident
    if ident:
        return f"https://core.ac.uk/works/{ident}"
    return ""


def _abstract(row: dict) -> str:
    raw = row.get("abstract") or row.get("description") or ""
    if isinstance(raw, list):
        parts = [str(item).strip() for item in raw if str(item).strip()]
        return parts[0] if parts else ""
    return str(raw or "").strip()


def parse_core_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map CORE v3 works search JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = _title(row)
        doi = _doi(row)
        url = _url(row, doi)
        authors = _authors(row)
        year = _year(row)
        abstract = _abstract(row)
        bits = [p for p in (authors, year) if p]
        snippet = " · ".join(bits)
        if abstract:
            snippet = f"{snippet} · {abstract}" if snippet else abstract
        snippet = snippet or "CORE work"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "CORE",
                url=url,
                snippet=snippet,
                source="core",
            )
        )
    return hits[:limit]
