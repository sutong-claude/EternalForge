"""OpenAlex concepts extras SearchAdapter (concepts API; no key)."""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

OA_CONCEPTS = "https://api.openalex.org/concepts"
OA_SELECT = (
    "id,display_name,description,level,works_count,cited_by_count,"
    "ancestors,related_concepts,ids"
)


class OaConceptAdapter:
    """OpenAlex concepts search with level, ancestors, related, works, cites. No key."""

    name = "oaconcept"
    endpoint = OA_CONCEPTS

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
        return parse_oaconcept_payload(payload, limit=limit)


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = payload.get("results") or payload.get("concepts") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def _display(value: object) -> str:
    if isinstance(value, dict):
        return str(value.get("display_name") or value.get("name") or "").strip()
    return str(value or "").strip()


def _level(row: dict) -> str:
    level = row.get("level")
    if isinstance(level, (int, float)):
        return f"L{int(level)}"
    text = str(level or "").strip()
    if text.isdigit():
        return f"L{text}"
    return ""


def _names(raw: object, key: str = "display_name", limit: int = 3) -> str:
    if isinstance(raw, str):
        return raw.strip()
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:limit]:
        text = _display(item) if not isinstance(item, dict) else str(
            item.get(key) or item.get("display_name") or item.get("name") or ""
        ).strip()
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


def _concept_url(row: dict) -> str:
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


def parse_oaconcept_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map OpenAlex /concepts JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = str(row.get("display_name") or row.get("name") or "").strip()
        url = _concept_url(row)
        desc = str(row.get("description") or "").strip()
        ancestors = _names(row.get("ancestors"))
        related = _names(row.get("related_concepts"))
        bits = [
            p
            for p in (
                _level(row),
                ancestors,
                related,
                _works(row),
                _cites(row),
            )
            if p
        ]
        snippet = " · ".join(bits)
        if desc:
            snippet = f"{snippet} — {desc}" if snippet else desc
        snippet = snippet or "OpenAlex concept"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "OpenAlex concept",
                url=url,
                snippet=snippet,
                source="oaconcept",
            )
        )
    return hits[:limit]
