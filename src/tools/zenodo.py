"""Zenodo SearchAdapter (records search JSON, no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

ZENODO_RECORDS = "https://zenodo.org/api/records"


class ZenodoAdapter:
    """Zenodo records search. No key required."""

    name = "zenodo"
    endpoint = ZENODO_RECORDS

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?q={quote(q)}&size={limit}"
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_zenodo_payload(payload, limit=limit)


def _metadata(row: dict) -> dict:
    meta = row.get("metadata")
    return meta if isinstance(meta, dict) else {}


def _format_creators(meta: dict) -> str:
    raw = meta.get("creators") or meta.get("authors") or []
    if isinstance(raw, str):
        parts = [p.strip() for p in raw.replace(";", ",").split(",") if p.strip()]
        return ", ".join(parts[:3])
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:3]:
        if isinstance(item, dict):
            name = str(item.get("name") or item.get("display_name") or "").strip()
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def _record_url(row: dict, meta: dict) -> str:
    links = row.get("links") if isinstance(row.get("links"), dict) else {}
    html = str(links.get("html") or links.get("self_html") or "").strip()
    if html.startswith("http"):
        return html
    doi = str(row.get("doi") or meta.get("doi") or "").strip()
    if doi.startswith("http"):
        return doi
    if doi:
        return f"https://doi.org/{doi.removeprefix('https://doi.org/')}"
    ident = str(row.get("id") or row.get("recid") or "").strip()
    if ident.startswith("http"):
        return ident
    if ident:
        return f"https://zenodo.org/records/{ident}"
    return ""


def _resource_type(meta: dict) -> str:
    raw = meta.get("resource_type") or meta.get("type") or ""
    if isinstance(raw, dict):
        return str(raw.get("title") or raw.get("type") or "").strip()
    return str(raw or "").strip()


def _rows_from_payload(payload: dict) -> list[dict]:
    hits = payload.get("hits")
    if isinstance(hits, dict):
        rows = hits.get("hits") or hits.get("records") or []
    else:
        rows = payload.get("records") or payload.get("hits") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def parse_zenodo_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map Zenodo records search JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        meta = _metadata(row)
        title = str(meta.get("title") or row.get("title") or "").strip()
        url = _record_url(row, meta)
        authors = _format_creators(meta)
        date = str(meta.get("publication_date") or row.get("created") or "").strip()
        year = date[:4] if date[:4].isdigit() else date
        kind = _resource_type(meta)
        abstract = str(meta.get("description") or row.get("description") or "").strip()
        bits = [p for p in (authors, year, kind) if p]
        snippet = " · ".join(bits)
        if abstract:
            snippet = f"{snippet} · {abstract}" if snippet else abstract
        snippet = snippet or "Zenodo record"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "Zenodo",
                url=url,
                snippet=snippet,
                source="zenodo",
            )
        )
    return hits[:limit]
