"""OpenAlex topics extras SearchAdapter (topics API; no key)."""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

OA_TOPICS = "https://api.openalex.org/topics"
OA_SELECT = (
    "id,display_name,description,keywords,works_count,cited_by_count,"
    "domain,field,subfield,ids"
)


class OaTopicAdapter:
    """OpenAlex topics search with hierarchy, keywords, works, and cites. No key."""

    name = "oatopic"
    endpoint = OA_TOPICS

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
        return parse_oatopic_payload(payload, limit=limit)


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = payload.get("results") or payload.get("topics") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def _display(value: object) -> str:
    if isinstance(value, dict):
        return str(value.get("display_name") or value.get("name") or "").strip()
    return str(value or "").strip()


def _keywords(row: dict) -> str:
    raw = row.get("keywords") or []
    if isinstance(raw, str):
        return raw.strip()
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:3]:
        if isinstance(item, dict):
            text = str(item.get("keyword") or item.get("display_name") or "").strip()
        else:
            text = str(item).strip()
        if text:
            names.append(text)
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


def _hierarchy(row: dict) -> str:
    parts = [
        p
        for p in (
            _display(row.get("domain")),
            _display(row.get("field")),
            _display(row.get("subfield")),
        )
        if p
    ]
    return " / ".join(parts)


def _topic_url(row: dict) -> str:
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


def parse_oatopic_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map OpenAlex /topics JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = str(row.get("display_name") or row.get("name") or "").strip()
        url = _topic_url(row)
        desc = str(row.get("description") or "").strip()
        bits = [
            p
            for p in (
                _hierarchy(row),
                _keywords(row),
                _works(row),
                _cites(row),
            )
            if p
        ]
        snippet = " · ".join(bits)
        if desc:
            snippet = f"{snippet} — {desc}" if snippet else desc
        snippet = snippet or "OpenAlex topic"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "OpenAlex topic",
                url=url,
                snippet=snippet,
                source="oatopic",
            )
        )
    return hits[:limit]
