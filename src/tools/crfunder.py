"""Crossref funder extras SearchAdapter (funders API; no key)."""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

XREF_FUNDERS = "https://api.crossref.org/funders"


class CrFunderAdapter:
    """Crossref funders search with location, alt-names, and work counts. No key."""

    name = "crfunder"
    endpoint = XREF_FUNDERS

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?query={quote(q)}&rows={limit}"
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
        return parse_crfunder_payload(payload, limit=limit)


def _rows_from_payload(payload: dict) -> list[dict]:
    message = payload.get("message") if isinstance(payload.get("message"), dict) else payload
    rows = message.get("items") or message.get("funders") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def _alt_names(row: dict) -> str:
    raw = row.get("alt-names") or row.get("alt_names") or row.get("aliases") or []
    if isinstance(raw, str):
        return raw.strip()
    if not isinstance(raw, list):
        return ""
    names = [str(item).strip() for item in raw[:3] if str(item).strip()]
    return ", ".join(names)


def _works(row: dict) -> str:
    count = row.get("work-count") or row.get("work_count") or row.get("works")
    if isinstance(count, (int, float)) and count:
        return f"{int(count)} works"
    text = str(count or "").strip()
    if text.isdigit() and int(text):
        return f"{text} works"
    return ""


def _descendants(row: dict) -> str:
    count = row.get("descendant-work-count") or row.get("descendant_work_count")
    if isinstance(count, (int, float)) and count:
        return f"{int(count)} descendant works"
    text = str(count or "").strip()
    if text.isdigit() and int(text):
        return f"{text} descendant works"
    return ""


def _funder_url(row: dict) -> str:
    url = str(row.get("uri") or row.get("URL") or row.get("url") or "").strip()
    if url.startswith("http"):
        return url
    funder_id = str(row.get("id") or "").strip()
    if funder_id.startswith("http"):
        return funder_id
    if funder_id:
        return f"https://api.crossref.org/funders/{quote(funder_id)}"
    return ""


def parse_crfunder_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map Crossref /funders JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = str(row.get("name") or row.get("title") or "").strip()
        url = _funder_url(row)
        location = str(row.get("location") or row.get("country") or "").strip()
        bits = [
            p
            for p in (
                location,
                _alt_names(row),
                _works(row),
                _descendants(row),
            )
            if p
        ]
        snippet = " · ".join(bits) or "Crossref funder"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "Crossref funder",
                url=url,
                snippet=snippet,
                source="crfunder",
            )
        )
    return hits[:limit]
