"""OpenAlex sources extras SearchAdapter (sources API; no key)."""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

OA_SOURCES = "https://api.openalex.org/sources"
OA_SELECT = (
    "id,display_name,type,issn_l,issn,publisher,host_organization_name,"
    "country_code,is_oa,is_in_doaj,works_count,cited_by_count,"
    "homepage_url,ids"
)


class OaSourceAdapter:
    """OpenAlex sources search with type, publisher, ISSN, OA, works, cites. No key."""

    name = "oasource"
    endpoint = OA_SOURCES

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
        return parse_oasource_payload(payload, limit=limit)


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = payload.get("results") or payload.get("sources") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def _issn(row: dict) -> str:
    issn_l = str(row.get("issn_l") or "").strip()
    if issn_l:
        return issn_l
    raw = row.get("issn")
    if isinstance(raw, list):
        for item in raw:
            text = str(item or "").strip()
            if text:
                return text
    return str(raw or "").strip()


def _publisher(row: dict) -> str:
    for key in ("host_organization_name", "publisher"):
        text = str(row.get(key) or "").strip()
        if text:
            return text
    return ""


def _oa_flags(row: dict) -> str:
    bits: list[str] = []
    if row.get("is_oa") is True:
        bits.append("OA")
    if row.get("is_in_doaj") is True:
        bits.append("DOAJ")
    return " ".join(bits)


def _works(row: dict) -> str:
    count = row.get("works_count") or row.get("works")
    if isinstance(count, (int, float)) and count:
        return f"{int(count)} works"
    text = str(count or "").strip()
    if text.isdigit() and int(text):
        return f"{text} works"
    return ""


def _cites(row: dict) -> str:
    count = row.get("cited_by_count")
    if isinstance(count, (int, float)) and count:
        return f"{int(count)} cites"
    text = str(count or "").strip()
    if text.isdigit() and int(text):
        return f"{text} cites"
    return ""


def _source_url(row: dict) -> str:
    home = str(row.get("homepage_url") or "").strip()
    if home.startswith("http"):
        return home
    raw_id = str(row.get("id") or "").strip()
    if raw_id.startswith("http"):
        return raw_id
    ids = row.get("ids") if isinstance(row.get("ids"), dict) else {}
    openalex = str(ids.get("openalex") or "").strip()
    if openalex.startswith("http"):
        return openalex
    if raw_id:
        short = raw_id.split("/")[-1]
        return f"https://openalex.org/{quote(short)}"
    return ""


def parse_oasource_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map OpenAlex /sources JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = str(row.get("display_name") or row.get("name") or "").strip()
        url = _source_url(row)
        kind = str(row.get("type") or "").strip()
        country = str(row.get("country_code") or "").strip().upper()
        bits = [
            p
            for p in (
                kind,
                _publisher(row),
                _issn(row),
                country,
                _oa_flags(row),
                _works(row),
                _cites(row),
            )
            if p
        ]
        snippet = " · ".join(bits) or "OpenAlex source"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "OpenAlex source",
                url=url,
                snippet=snippet,
                source="oasource",
            )
        )
    return hits[:limit]
