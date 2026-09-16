"""Europe PMC SearchAdapter (REST search JSON, no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

EUROPEPMC_SEARCH = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
EUROPEPMC_PAGE = "https://europepmc.org/article"


class EuropePMCAdapter:
    """Europe PMC literature search. No key required."""

    name = "europepmc"
    endpoint = EUROPEPMC_SEARCH

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = (
            f"{self.endpoint}?query={quote(q)}&format=json"
            f"&pageSize={limit}&resultType=lite"
        )
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_europepmc_payload(payload, limit=limit)


def _article_url(row: dict) -> str:
    explicit = str(row.get("url") or row.get("fullTextUrl") or "").strip()
    if explicit.startswith("http"):
        return explicit
    source = str(row.get("source") or "").strip().upper()
    ident = str(
        row.get("id") or row.get("pmid") or row.get("pmcid") or row.get("doi") or ""
    ).strip()
    if source and ident:
        return f"{EUROPEPMC_PAGE}/{source}/{ident}"
    pmid = str(row.get("pmid") or "").strip()
    if pmid:
        return f"{EUROPEPMC_PAGE}/MED/{pmid}"
    pmcid = str(row.get("pmcid") or "").strip()
    if pmcid:
        return f"{EUROPEPMC_PAGE}/PMC/{pmcid}"
    doi = str(row.get("doi") or "").strip()
    if doi:
        return f"https://doi.org/{doi}"
    return ""


def _format_authors(row: dict) -> str:
    raw = row.get("authorString") or row.get("authorList") or row.get("authors")
    if isinstance(raw, str):
        parts = [p.strip() for p in raw.replace(";", ",").split(",") if p.strip()]
        return ", ".join(parts[:3])
    if isinstance(raw, dict):
        authors = raw.get("author") or raw.get("authors") or []
        raw = authors
    if isinstance(raw, list):
        names: list[str] = []
        for author in raw[:3]:
            if isinstance(author, dict):
                full = str(author.get("fullName") or author.get("name") or "").strip()
                if not full:
                    given = str(author.get("firstName") or author.get("given") or "").strip()
                    family = str(author.get("lastName") or author.get("family") or "").strip()
                    full = " ".join(p for p in (given, family) if p)
            else:
                full = str(author or "").strip()
            if full:
                names.append(full)
        return ", ".join(names)
    return ""


def _rows_from_payload(payload: dict) -> list[dict]:
    articles = payload.get("articles") or payload.get("results") or []
    if isinstance(articles, list) and articles:
        return [item for item in articles if isinstance(item, dict)]
    result_list = payload.get("resultList") or payload.get("resultlist") or {}
    if isinstance(result_list, dict):
        rows = result_list.get("result") or result_list.get("results") or []
        if isinstance(rows, list):
            return [item for item in rows if isinstance(item, dict)]
    if isinstance(result_list, list):
        return [item for item in result_list if isinstance(item, dict)]
    return []


def parse_europepmc_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map Europe PMC search JSON (or a simple articles list) into Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = str(row.get("title") or "").strip().rstrip(".")
        url = _article_url(row)
        authors = _format_authors(row)
        journal = str(row.get("journalTitle") or row.get("journal") or "").strip()
        year = str(row.get("pubYear") or row.get("year") or "").strip()
        snippet_src = str(row.get("abstractText") or row.get("abstract") or "").strip()
        bits = [p for p in (authors, journal, year) if p]
        snippet = " · ".join(bits)
        if snippet_src:
            snippet = f"{snippet} · {snippet_src}" if snippet else snippet_src
        snippet = snippet or "Europe PMC article"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "Europe PMC",
                url=url,
                snippet=snippet,
                source="europepmc",
            )
        )
    return hits[:limit]
