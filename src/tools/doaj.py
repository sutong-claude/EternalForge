"""DOAJ SearchAdapter (open-access articles JSON, no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

DOAJ_ARTICLES = "https://doaj.org/api/search/articles"


class DoajAdapter:
    """Directory of Open Access Journals article search. No key required."""

    name = "doaj"
    endpoint = DOAJ_ARTICLES

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}/{quote(q)}?pageSize={limit}"
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_doaj_payload(payload, limit=limit)


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = payload.get("results") or payload.get("articles") or payload.get("hits") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def _bibjson(row: dict) -> dict:
    raw = row.get("bibjson") or row.get("bib") or {}
    return raw if isinstance(raw, dict) else {}


def _title(bib: dict, row: dict) -> str:
    return str(bib.get("title") or row.get("title") or "").strip()


def _authors(bib: dict) -> str:
    raw = bib.get("author") or bib.get("authors") or []
    if isinstance(raw, str):
        parts = [p.strip() for p in raw.replace(";", ",").split(",") if p.strip()]
        return ", ".join(parts[:3])
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:3]:
        if isinstance(item, dict):
            name = str(item.get("name") or item.get("full_name") or "").strip()
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def _year(bib: dict) -> str:
    year = bib.get("year") or bib.get("publication_year") or ""
    text = str(year).strip()
    return text[:4] if text[:4].isdigit() else text


def _journal(bib: dict) -> str:
    raw = bib.get("journal") or {}
    if isinstance(raw, dict):
        return str(raw.get("title") or raw.get("name") or "").strip()
    return str(raw or "").strip()


def _abstract(bib: dict) -> str:
    return str(bib.get("abstract") or bib.get("description") or "").strip()


def _doi(bib: dict, row: dict) -> str:
    identifiers = bib.get("identifier") or bib.get("identifiers") or row.get("id") or []
    if isinstance(identifiers, str):
        text = identifiers.strip()
        if text.lower().startswith("10."):
            return text
        return ""
    if isinstance(identifiers, list):
        for item in identifiers:
            if isinstance(item, dict):
                kind = str(item.get("type") or item.get("id_type") or "").lower()
                value = str(item.get("id") or item.get("value") or "").strip()
                if kind == "doi" and value:
                    return value.removeprefix("https://doi.org/")
            else:
                value = str(item or "").strip()
                if value.lower().startswith("10."):
                    return value
    return ""


def _url(bib: dict, row: dict, doi: str) -> str:
    links = bib.get("link") or bib.get("links") or []
    if isinstance(links, list):
        for item in links:
            if isinstance(item, dict):
                url = str(item.get("url") or item.get("href") or "").strip()
            else:
                url = str(item or "").strip()
            if url.startswith("http"):
                return url
    elif isinstance(links, str) and links.startswith("http"):
        return links
    url = str(row.get("url") or bib.get("url") or "").strip()
    if url.startswith("http"):
        return url
    if doi:
        return f"https://doi.org/{doi}"
    article_id = str(row.get("id") or "").strip()
    if article_id:
        return f"https://doaj.org/article/{article_id}"
    return ""


def parse_doaj_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map DOAJ article search JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        bib = _bibjson(row)
        title = _title(bib, row)
        doi = _doi(bib, row)
        url = _url(bib, row, doi)
        authors = _authors(bib)
        year = _year(bib)
        journal = _journal(bib)
        abstract = _abstract(bib)
        bits = [p for p in (authors, year, journal) if p]
        snippet = " · ".join(bits)
        if abstract:
            snippet = f"{snippet} · {abstract}" if snippet else abstract
        snippet = snippet or "DOAJ article"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "DOAJ",
                url=url,
                snippet=snippet,
                source="doaj",
            )
        )
    return hits[:limit]
