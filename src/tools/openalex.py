"""OpenAlex SearchAdapter (works search JSON, no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

OPENALEX_WORKS = "https://api.openalex.org/works"


class OpenAlexAdapter:
    """OpenAlex works search. No key required."""

    name = "openalex"
    endpoint = OPENALEX_WORKS

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?search={quote(q)}&per-page={limit}"
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_openalex_payload(payload, limit=limit)


def _format_authors(row: dict) -> str:
    raw = row.get("authorships") or row.get("authors") or []
    if isinstance(raw, str):
        parts = [p.strip() for p in raw.replace(";", ",").split(",") if p.strip()]
        return ", ".join(parts[:3])
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:3]:
        if isinstance(item, dict):
            author = item.get("author") if isinstance(item.get("author"), dict) else item
            name = str(
                author.get("display_name") or author.get("name") or ""
            ).strip()
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def _work_url(row: dict) -> str:
    loc = row.get("primary_location") or row.get("best_oa_location") or {}
    if isinstance(loc, dict):
        landing = str(loc.get("landing_page_url") or loc.get("pdf_url") or "").strip()
        if landing.startswith("http"):
            return landing
    doi = str(row.get("doi") or "").strip()
    if doi.startswith("http"):
        return doi
    if doi:
        return f"https://doi.org/{doi.removeprefix('https://doi.org/')}"
    ident = str(row.get("id") or row.get("openalex_id") or "").strip()
    if ident.startswith("http"):
        return ident
    if ident:
        return f"https://openalex.org/{ident}"
    return ""


def _venue(row: dict) -> str:
    loc = row.get("primary_location") or {}
    if isinstance(loc, dict):
        source = loc.get("source") or {}
        if isinstance(source, dict):
            name = str(source.get("display_name") or source.get("name") or "").strip()
            if name:
                return name
    host = row.get("host_venue") or {}
    if isinstance(host, dict):
        return str(host.get("display_name") or host.get("name") or "").strip()
    return str(row.get("venue") or "").strip()


def _abstract_from_inverted(index: object) -> str:
    if not isinstance(index, dict) or not index:
        return ""
    positions: list[tuple[int, str]] = []
    for word, spots in index.items():
        if not isinstance(spots, list):
            continue
        for spot in spots:
            try:
                positions.append((int(spot), str(word)))
            except (TypeError, ValueError):
                continue
    if not positions:
        return ""
    positions.sort()
    return " ".join(word for _, word in positions)


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = payload.get("results") or payload.get("works") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def parse_openalex_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map OpenAlex works search JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = str(row.get("display_name") or row.get("title") or "").strip()
        url = _work_url(row)
        authors = _format_authors(row)
        year = str(row.get("publication_year") or row.get("year") or "").strip()
        venue = _venue(row)
        cited = row.get("cited_by_count")
        cited_s = f"{cited} cites" if isinstance(cited, int) and cited else ""
        abstract = str(row.get("abstract") or "").strip()
        if not abstract:
            abstract = _abstract_from_inverted(row.get("abstract_inverted_index"))
        bits = [p for p in (authors, year, venue, cited_s) if p]
        snippet = " · ".join(bits)
        if abstract:
            snippet = f"{snippet} · {abstract}" if snippet else abstract
        snippet = snippet or "OpenAlex work"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "OpenAlex",
                url=url,
                snippet=snippet,
                source="openalex",
            )
        )
    return hits[:limit]
