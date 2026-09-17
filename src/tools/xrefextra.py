"""Crossref extras SearchAdapter (citations, abstract, license; no key)."""

from __future__ import annotations

import json
import os
import re
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.crossref import _first_title, _format_authors, _issued_year
from tools.research import USER_AGENT, Hit, _unavailable

XREF_WORKS = "https://api.crossref.org/works"
XREF_SELECT = (
    "DOI,URL,title,author,issued,container-title,abstract,"
    "type,is-referenced-by-count,license,subject"
)
_TAG_RE = re.compile(r"<[^>]+>")


class XrefExtraAdapter:
    """Crossref works search with extra bibliographic fields. No key."""

    name = "xrefextra"
    endpoint = XREF_WORKS

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?query={quote(q)}&rows={limit}&select={quote(XREF_SELECT)}"
        mailto = (os.environ.get("CROSSREF_MAILTO") or "").strip()
        if mailto:
            url += f"&mailto={quote(mailto)}"
        req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_xrefextra_payload(payload, limit=limit)


def _abstract(row: dict) -> str:
    raw = str(row.get("abstract") or "").strip()
    if not raw:
        return ""
    text = _TAG_RE.sub(" ", raw)
    return " ".join(text.split())


def _cites(row: dict) -> str:
    count = row.get("is-referenced-by-count")
    if isinstance(count, (int, float)) and count:
        return f"{int(count)} cites"
    return ""


def _license(row: dict) -> str:
    raw = row.get("license") or []
    if isinstance(raw, dict):
        raw = [raw]
    if not isinstance(raw, list):
        return ""
    for item in raw:
        if not isinstance(item, dict):
            continue
        url = str(item.get("URL") or item.get("url") or "").strip()
        if url:
            return url.rsplit("/", 1)[-1] or url
    return ""


def _subjects(row: dict) -> str:
    raw = row.get("subject") or []
    if isinstance(raw, str):
        return raw.strip()
    if not isinstance(raw, list):
        return ""
    names = [str(item).strip() for item in raw[:2] if str(item).strip()]
    return ", ".join(names)


def parse_xrefextra_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map Crossref extras /works JSON into research Hits."""
    message = payload.get("message") if isinstance(payload.get("message"), dict) else payload
    rows = message.get("items") or message.get("works") or []
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
        kind = str(row.get("type") or "").strip().replace("-", " ")
        cites = _cites(row)
        license_ = _license(row)
        subjects = _subjects(row)
        abstract = _abstract(row)
        bits = [p for p in (authors, year, venue, kind, cites, license_, subjects) if p]
        snippet = " · ".join(bits)
        if abstract:
            snippet = f"{snippet} — {abstract}" if snippet else abstract
        snippet = snippet or (doi and f"DOI {doi}") or "Crossref extras work"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or doi or "Crossref",
                url=url,
                snippet=snippet,
                source="xrefextra",
            )
        )
    return hits[:limit]
