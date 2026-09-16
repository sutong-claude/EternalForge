"""Semantic Scholar SearchAdapter (graph paper search, no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable


class SemanticScholarAdapter:
    """Semantic Scholar graph paper search. No key required for light use."""

    name = "semanticscholar"
    endpoint = "https://api.semanticscholar.org/graph/v1/paper/search"

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        fields = "title,url,abstract,year,authors,venue,externalIds"
        url = f"{self.endpoint}?query={quote(q)}&limit={limit}&fields={fields}"
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_semanticscholar_payload(payload, limit=limit)


def _format_authors(authors: object) -> str:
    if not isinstance(authors, list):
        return ""
    names: list[str] = []
    for author in authors[:3]:
        if isinstance(author, dict):
            name = str(author.get("name") or "").strip()
        else:
            name = str(author or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def _paper_url(row: dict) -> str:
    url = str(row.get("url") or "").strip()
    if url:
        return url
    paper_id = str(row.get("paperId") or row.get("paper_id") or "").strip()
    if paper_id:
        return f"https://www.semanticscholar.org/paper/{paper_id}"
    ids = row.get("externalIds") or row.get("external_ids") or {}
    if isinstance(ids, dict):
        doi = str(ids.get("DOI") or ids.get("doi") or "").strip()
        if doi:
            return f"https://doi.org/{doi}"
        arxiv = str(ids.get("ArXiv") or ids.get("arxiv") or "").strip()
        if arxiv:
            return f"https://arxiv.org/abs/{arxiv}"
    return ""


def parse_semanticscholar_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map Semantic Scholar paper/search JSON into research Hits."""
    rows = payload.get("data") or payload.get("papers") or []
    if not isinstance(rows, list):
        return []
    hits: list[Hit] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        title = str(row.get("title") or "").strip()
        url = _paper_url(row)
        authors = _format_authors(row.get("authors"))
        year = row.get("year")
        year_s = str(year) if year else ""
        venue = str(row.get("venue") or "").strip()
        abstract = str(row.get("abstract") or "").strip()
        bits = [p for p in (authors, year_s, venue) if p]
        snippet = " · ".join(bits)
        if abstract:
            snippet = f"{snippet} — {abstract}" if snippet else abstract
        snippet = snippet or "Semantic Scholar paper"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "Semantic Scholar",
                url=url,
                snippet=snippet,
                source="semanticscholar",
            )
        )
    return hits[:limit]
