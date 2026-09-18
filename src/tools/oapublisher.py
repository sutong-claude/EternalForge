"""OpenAlex publishers extras SearchAdapter (publishers API; no key)."""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

OA_PUBLISHERS = "https://api.openalex.org/publishers"
OA_SELECT = (
    "id,display_name,alternate_titles,country_codes,hierarchy_level,"
    "parent_publisher,homepage_url,works_count,cited_by_count,"
    "sources_count,ids"
)


class OaPublisherAdapter:
    """OpenAlex publishers search with country, parent, sources, works, cites. No key."""

    name = "oapublisher"
    endpoint = OA_PUBLISHERS

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
        return parse_oapublisher_payload(payload, limit=limit)


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = payload.get("results") or payload.get("publishers") or []
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


def _countries(row: dict) -> str:
    raw = row.get("country_codes") or row.get("country_code") or row.get("country")
    if isinstance(raw, list):
        codes = [str(item).strip().upper() for item in raw if str(item).strip()]
        return ", ".join(codes[:3])
    return str(raw or "").strip().upper()


def _parent(row: dict) -> str:
    raw = row.get("parent_publisher") or row.get("parent")
    if isinstance(raw, dict):
        name = str(raw.get("display_name") or raw.get("name") or "").strip()
        return f"parent {name}" if name else ""
    text = str(raw or "").strip()
    return f"parent {text}" if text else ""


def _level(row: dict) -> str:
    level = row.get("hierarchy_level")
    if isinstance(level, (int, float)):
        return f"L{int(level)}"
    text = str(level or "").strip()
    if text.isdigit():
        return f"L{text}"
    return ""


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


def _sources(row: dict) -> str:
    count = row.get("sources_count") or row.get("sources")
    if isinstance(count, (int, float)) and count:
        return f"{int(count)} sources"
    text = str(count or "").strip()
    if text.isdigit() and int(text):
        return f"{text} sources"
    return ""


def _publisher_url(row: dict) -> str:
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


def parse_oapublisher_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map OpenAlex /publishers JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = str(row.get("display_name") or row.get("name") or "").strip()
        url = _publisher_url(row)
        bits = [
            p
            for p in (
                _countries(row),
                _alt_names(row),
                _level(row),
                _parent(row),
                _sources(row),
                _works(row),
                _cites(row),
            )
            if p
        ]
        snippet = " · ".join(bits) or "OpenAlex publisher"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "OpenAlex publisher",
                url=url,
                snippet=snippet,
                source="oapublisher",
            )
        )
    return hits[:limit]
