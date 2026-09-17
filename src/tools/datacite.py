"""DataCite SearchAdapter (DOI REST search JSON, no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

DATACITE_DOIS = "https://api.datacite.org/dois"


class DataCiteAdapter:
    """DataCite DOI search. No key required."""

    name = "datacite"
    endpoint = DATACITE_DOIS

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?query={quote(q)}&page[size]={limit}"
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_datacite_payload(payload, limit=limit)


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = payload.get("data") or payload.get("dois") or payload.get("hits") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def _attrs(row: dict) -> dict:
    raw = row.get("attributes") or row.get("attr") or {}
    return raw if isinstance(raw, dict) else {}


def _first_title(attrs: dict, row: dict) -> str:
    titles = attrs.get("titles") or row.get("titles") or []
    if isinstance(titles, list):
        for item in titles:
            if isinstance(item, dict):
                title = str(item.get("title") or "").strip()
            else:
                title = str(item or "").strip()
            if title:
                return title
    elif isinstance(titles, str) and titles.strip():
        return titles.strip()
    return str(attrs.get("title") or row.get("title") or "").strip()


def _format_creators(attrs: dict) -> str:
    raw = attrs.get("creators") or attrs.get("authors") or []
    if isinstance(raw, str):
        parts = [p.strip() for p in raw.replace(";", ",").split(",") if p.strip()]
        return ", ".join(parts[:3])
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:3]:
        if isinstance(item, dict):
            name = str(item.get("name") or item.get("familyName") or "").strip()
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def _doi_url(row: dict, attrs: dict) -> str:
    url = str(attrs.get("url") or row.get("url") or "").strip()
    if url.startswith("http"):
        return url
    doi = str(row.get("id") or attrs.get("doi") or row.get("doi") or "").strip()
    if doi.startswith("http"):
        return doi
    if doi:
        return f"https://doi.org/{doi.removeprefix('https://doi.org/')}"
    return ""


def _year(attrs: dict) -> str:
    year = attrs.get("publicationYear") or attrs.get("published") or attrs.get("year") or ""
    text = str(year).strip()
    return text[:4] if text[:4].isdigit() else text


def _resource_type(attrs: dict) -> str:
    raw = attrs.get("types") or attrs.get("resourceType") or ""
    if isinstance(raw, dict):
        return str(
            raw.get("resourceTypeGeneral") or raw.get("resourceType") or raw.get("title") or ""
        ).strip()
    return str(raw or "").strip()


def _description(attrs: dict) -> str:
    raw = attrs.get("descriptions") or attrs.get("description") or ""
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                text = str(item.get("description") or "").strip()
            else:
                text = str(item or "").strip()
            if text:
                return text
        return ""
    return str(raw or "").strip()


def parse_datacite_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map DataCite DOI search JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        attrs = _attrs(row)
        title = _first_title(attrs, row)
        url = _doi_url(row, attrs)
        authors = _format_creators(attrs)
        year = _year(attrs)
        kind = _resource_type(attrs)
        abstract = _description(attrs)
        bits = [p for p in (authors, year, kind) if p]
        snippet = " · ".join(bits)
        if abstract:
            snippet = f"{snippet} · {abstract}" if snippet else abstract
        snippet = snippet or "DataCite DOI"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "DataCite",
                url=url,
                snippet=snippet,
                source="datacite",
            )
        )
    return hits[:limit]
