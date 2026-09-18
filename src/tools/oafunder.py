"""OpenAlex funder extras SearchAdapter (funders API; no key)."""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

OA_FUNDERS = "https://api.openalex.org/funders"
OA_SELECT = (
    "id,display_name,country_code,description,homepage_url,works_count,"
    "cited_by_count,ids,alternate_titles,grants_count,roles"
)


class OaFunderAdapter:
    """OpenAlex funders search with country, alt names, works, and cites. No key."""

    name = "oafunder"
    endpoint = OA_FUNDERS

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
        return parse_oafunder_payload(payload, limit=limit)


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = payload.get("results") or payload.get("funders") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def _alt_names(row: dict) -> str:
    raw = row.get("alternate_titles") or row.get("alternate_names") or []
    if isinstance(raw, str):
        return raw.strip()
    if not isinstance(raw, list):
        return ""
    names = [str(item).strip() for item in raw[:3] if str(item).strip()]
    return ", ".join(names)


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


def _grants(row: dict) -> str:
    count = row.get("grants_count") or row.get("grants")
    if isinstance(count, (int, float)) and count:
        return f"{int(count)} grants"
    text = str(count or "").strip()
    if text.isdigit() and int(text):
        return f"{text} grants"
    return ""


def _funder_url(row: dict) -> str:
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


def parse_oafunder_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map OpenAlex /funders JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = str(row.get("display_name") or row.get("name") or "").strip()
        url = _funder_url(row)
        country = str(row.get("country_code") or row.get("country") or "").strip()
        desc = str(row.get("description") or "").strip()
        bits = [
            p
            for p in (
                country,
                _alt_names(row),
                _works(row),
                _cites(row),
                _grants(row),
            )
            if p
        ]
        snippet = " · ".join(bits)
        if desc:
            snippet = f"{snippet} — {desc}" if snippet else desc
        snippet = snippet or "OpenAlex funder"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "OpenAlex funder",
                url=url,
                snippet=snippet,
                source="oafunder",
            )
        )
    return hits[:limit]
