"""Semantic Scholar Graph extras SearchAdapter (tldr + citations, no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable
from tools.semanticscholar import _format_authors, _paper_url

S2_GRAPH_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"
S2_FIELDS = (
    "title,url,abstract,year,authors,venue,externalIds,"
    "citationCount,influentialCitationCount,tldr,publicationDate"
)


class S2GraphAdapter:
    """Semantic Scholar Graph paper search with extra fields. No key."""

    name = "s2graph"
    endpoint = S2_GRAPH_SEARCH

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?query={quote(q)}&limit={limit}&fields={S2_FIELDS}"
        req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_s2graph_payload(payload, limit=limit)


def _tldr(row: dict) -> str:
    raw = row.get("tldr")
    if isinstance(raw, dict):
        return str(raw.get("text") or raw.get("tldr") or "").strip()
    return str(raw or "").strip()


def _citations(row: dict) -> str:
    count = row.get("citationCount")
    infl = row.get("influentialCitationCount")
    bits: list[str] = []
    if isinstance(count, (int, float)) and count:
        bits.append(f"{int(count)} cites")
    if isinstance(infl, (int, float)) and infl:
        bits.append(f"{int(infl)} infl")
    return ", ".join(bits)


def _year(row: dict) -> str:
    year = row.get("year")
    if year:
        return str(year)
    date = str(row.get("publicationDate") or "").strip()
    return date[:4] if date[:4].isdigit() else date


def parse_s2graph_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map Semantic Scholar Graph extras JSON into research Hits."""
    rows = payload.get("data") or payload.get("papers") or payload.get("results") or []
    if not isinstance(rows, list):
        return []
    hits: list[Hit] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        title = str(row.get("title") or "").strip()
        url = _paper_url(row)
        authors = _format_authors(row.get("authors"))
        year = _year(row)
        venue = str(row.get("venue") or "").strip()
        cites = _citations(row)
        abstract = str(row.get("abstract") or "").strip()
        tldr = _tldr(row)
        summary = tldr or abstract
        bits = [p for p in (authors, year, venue, cites) if p]
        snippet = " · ".join(bits)
        if summary:
            snippet = f"{snippet} — {summary}" if snippet else summary
        snippet = snippet or "Semantic Scholar graph paper"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "Semantic Scholar",
                url=url,
                snippet=snippet,
                source="s2graph",
            )
        )
    return hits[:limit]
