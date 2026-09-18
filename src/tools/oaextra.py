"""OpenAlex extras SearchAdapter (OA status, concepts, type; no key)."""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.openalex import (
    _abstract_from_inverted,
    _format_authors,
    _venue,
    _work_url,
)
from tools.research import USER_AGENT, Hit, _unavailable

OA_WORKS = "https://api.openalex.org/works"
OA_SELECT = (
    "id,doi,display_name,title,authorships,publication_year,publication_date,"
    "primary_location,best_oa_location,host_venue,cited_by_count,type,"
    "open_access,concepts,language,abstract_inverted_index,abstract"
)


class OaExtraAdapter:
    """OpenAlex works search with extra bibliographic fields. No key."""

    name = "oaextra"
    endpoint = OA_WORKS

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?search={quote(q)}&per-page={limit}&select={quote(OA_SELECT)}"
        mailto = (os.environ.get("OPENALEX_MAILTO") or "").strip()
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
        return parse_oaextra_payload(payload, limit=limit)


def _oa_status(row: dict) -> str:
    raw = row.get("open_access") or {}
    if isinstance(raw, dict):
        status = str(raw.get("oa_status") or raw.get("status") or "").strip()
        if raw.get("is_oa") is True and not status:
            status = "oa"
        return status.replace("-", " ")
    if raw is True:
        return "oa"
    return ""


def _concepts(row: dict) -> str:
    raw = row.get("concepts") or row.get("topics") or []
    if isinstance(raw, str):
        return raw.strip()
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:2]:
        if isinstance(item, dict):
            name = str(item.get("display_name") or item.get("name") or "").strip()
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def _kind(row: dict) -> str:
    return str(row.get("type") or row.get("type_crossref") or "").strip().replace("-", " ")


def _cites(row: dict) -> str:
    count = row.get("cited_by_count")
    if isinstance(count, (int, float)) and count:
        return f"{int(count)} cites"
    return ""


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = payload.get("results") or payload.get("works") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def parse_oaextra_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map OpenAlex extras works JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = str(row.get("display_name") or row.get("title") or "").strip()
        url = _work_url(row)
        authors = _format_authors(row)
        year = str(row.get("publication_year") or row.get("year") or "").strip()
        date = str(row.get("publication_date") or "").strip()
        when = date or year
        venue = _venue(row)
        kind = _kind(row)
        cites = _cites(row)
        oa = _oa_status(row)
        concepts = _concepts(row)
        lang = str(row.get("language") or "").strip()
        abstract = str(row.get("abstract") or "").strip()
        if not abstract:
            abstract = _abstract_from_inverted(row.get("abstract_inverted_index"))
        bits = [p for p in (authors, when, venue, kind, cites, oa, concepts, lang) if p]
        snippet = " · ".join(bits)
        if abstract:
            snippet = f"{snippet} — {abstract}" if snippet else abstract
        snippet = snippet or "OpenAlex extras work"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "OpenAlex",
                url=url,
                snippet=snippet,
                source="oaextra",
            )
        )
    return hits[:limit]
