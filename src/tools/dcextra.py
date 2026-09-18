"""DataCite extras SearchAdapter (subjects, publisher, rights, cites; no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

DATACITE_DOIS = "https://api.datacite.org/dois"


class DataCiteExtraAdapter:
    """DataCite DOI search with subjects, publisher, rights, and cites. No key."""

    name = "dcextra"
    endpoint = DATACITE_DOIS

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?query={quote(q)}&page[size]={limit}"
        req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.api+json"})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_dcextra_payload(payload, limit=limit)


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


def _publisher(attrs: dict) -> str:
    raw = attrs.get("publisher") or attrs.get("publisherName") or ""
    if isinstance(raw, dict):
        return str(raw.get("name") or raw.get("publisher") or "").strip()
    return str(raw or "").strip()


def _subjects(attrs: dict) -> str:
    raw = attrs.get("subjects") or attrs.get("subject") or []
    if isinstance(raw, str):
        return raw.strip()
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:3]:
        if isinstance(item, dict):
            name = str(item.get("subject") or item.get("name") or item.get("term") or "").strip()
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def _rights(attrs: dict) -> str:
    raw = attrs.get("rightsList") or attrs.get("rights") or []
    if isinstance(raw, str):
        return raw.strip()
    if isinstance(raw, dict):
        return str(raw.get("rights") or raw.get("rightsIdentifier") or raw.get("name") or "").strip()
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:2]:
        if isinstance(item, dict):
            name = str(
                item.get("rights")
                or item.get("rightsIdentifier")
                or item.get("name")
                or ""
            ).strip()
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def _cites(attrs: dict) -> str:
    raw = attrs.get("citationCount") or attrs.get("viewCount") or attrs.get("citations") or ""
    if raw in (None, ""):
        return ""
    text = str(raw).strip()
    if not text:
        return ""
    if text.isdigit():
        return f"{text} cites"
    return text


def _language(attrs: dict) -> str:
    raw = attrs.get("language") or attrs.get("lang") or ""
    if isinstance(raw, list):
        raw = raw[0] if raw else ""
    return str(raw or "").strip()


def _container(attrs: dict) -> str:
    raw = attrs.get("container") or attrs.get("containerTitle") or {}
    if isinstance(raw, dict):
        return str(raw.get("title") or raw.get("name") or "").strip()
    return str(raw or "").strip()


def parse_dcextra_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map DataCite DOI extras JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        attrs = _attrs(row)
        title = _first_title(attrs, row)
        url = _doi_url(row, attrs)
        bits = [
            p
            for p in (
                _publisher(attrs),
                _subjects(attrs),
                _rights(attrs),
                _cites(attrs),
                _language(attrs),
                _container(attrs),
            )
            if p
        ]
        snippet = " · ".join(bits) or "DataCite extras DOI"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "DataCite",
                url=url,
                snippet=snippet,
                source="dcextra",
            )
        )
    return hits[:limit]
