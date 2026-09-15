"""Crossref SearchAdapter (works API, no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable


class CrossrefAdapter:
    """Crossref works search. No key required; good for published papers."""

    name = "crossref"
    endpoint = "https://api.crossref.org/works"

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?query={quote(q)}&rows={limit}"
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_crossref_payload(payload, limit=limit)


def _first_title(value: object) -> str:
    if isinstance(value, list):
        for item in value:
            text = str(item or "").strip()
            if text:
                return text
        return ""
    return str(value or "").strip()


def _format_authors(authors: object) -> str:
    if not isinstance(authors, list):
        return ""
    names: list[str] = []
    for author in authors[:3]:
        if not isinstance(author, dict):
            continue
        family = str(author.get("family") or "").strip()
        given = str(author.get("given") or "").strip()
        if family and given:
            names.append(f"{given} {family}")
        elif family or given:
            names.append(family or given)
    return ", ".join(names)


def _issued_year(issued: object) -> str:
    if not isinstance(issued, dict):
        return ""
    parts = issued.get("date-parts") or issued.get("date_parts")
    if not isinstance(parts, list) or not parts:
        return ""
    first = parts[0]
    if isinstance(first, list) and first:
        year = first[0]
        return str(year) if year else ""
    return ""


def parse_crossref_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map Crossref /works JSON into research Hits."""
    message = payload.get("message") if isinstance(payload.get("message"), dict) else payload
    rows = message.get("items") or []
    if not isinstance(rows, list):
        return []
    hits: list[Hit] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        title = _first_title(row.get("title"))
        doi = str(row.get("DOI") or row.get("doi") or "").strip()
        url = str(row.get("URL") or row.get("url") or "").strip()
        if not url and doi:
            url = f"https://doi.org/{doi}"
        authors = _format_authors(row.get("author"))
        year = _issued_year(row.get("issued"))
        venue = _first_title(row.get("container-title") or row.get("container_title"))
        bits = [p for p in (authors, year, venue) if p]
        snippet = " · ".join(bits) or (doi and f"DOI {doi}") or "Crossref work"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or doi or "Crossref",
                url=url,
                snippet=snippet,
                source="crossref",
            )
        )
    return hits[:limit]
