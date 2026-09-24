"""OpenAlex works-by-keywords.id extras SearchAdapter (group_by; no key)."""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

OA_WORKS = "https://api.openalex.org/works"
FIELD = "keywords.id"


class OaKwIdAdapter:
    """OpenAlex works search grouped by keywords.id. No key."""

    name = "oakwid"
    endpoint = OA_WORKS

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?search={quote(q)}&group_by={FIELD}&per-page={limit}"
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
        return parse_oakwid_payload(payload, limit=limit, query=q)


def _intish(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value or "").strip()
    if text.isdigit():
        return int(text)
    return None


def _normalize_keyword_id(raw: object) -> str:
    text = str(raw or "").strip()
    if text.lower() in {"", "unknown", "null", "none"}:
        return ""
    if text.startswith("http") and "/" in text:
        text = text.rstrip("/").split("/")[-1]
    if text.lower().startswith("keyword:"):
        text = text.split(":", 1)[1].strip()
    return text.replace("+", " ").replace("%20", " ").strip()


def _keyword_label(row: dict) -> str:
    raw = (
        row.get("key_display_name")
        or row.get("display_name")
        or row.get("keyword")
        or row.get("keywords")
        or row.get(FIELD)
        or row.get("key")
        or ""
    )
    return _normalize_keyword_id(raw)


def _keyword_key(row: dict) -> str:
    raw = (
        row.get("key")
        or row.get("id")
        or row.get("keyword")
        or row.get("keywords")
        or row.get(FIELD)
        or ""
    )
    return _normalize_keyword_id(raw)


def _works_count(row: dict) -> int:
    for key in ("count", "works_count", "works"):
        value = _intish(row.get(key))
        if value is not None:
            return value
    return 0


def _cites_count(row: dict) -> int:
    for key in ("cited_by_count", "cites"):
        value = _intish(row.get(key))
        if value is not None:
            return value
    return 0


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = (
        payload.get("group_by")
        or payload.get("keywords")
        or payload.get("keyword_ids")
        or payload.get(FIELD)
        or []
    )
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def _oa_url(keyword: str, query: str = "") -> str:
    q = query.strip()
    filt = f"{FIELD}:{quote(keyword, safe='')}"
    if q:
        return f"https://openalex.org/works?search={quote(q)}&filter={filt}"
    return f"https://openalex.org/works?filter={filt}"


def parse_oakwid_payload(payload: dict, limit: int = 5, query: str = "") -> list[Hit]:
    """Map OpenAlex works group_by keywords.id JSON into Hits."""
    rows: list[tuple[int, dict]] = []
    for row in _rows_from_payload(payload):
        label = _keyword_label(row)
        key = _keyword_key(row)
        if not label or not key:
            continue
        rows.append((_works_count(row), row))
    rows.sort(key=lambda item: item[0], reverse=True)
    hits: list[Hit] = []
    for works, row in rows:
        label = _keyword_label(row)
        key = _keyword_key(row)
        cites = _cites_count(row)
        bits = [p for p in (
            f"{works} works" if works else "",
            f"{cites} cites" if cites else "",
        ) if p]
        snippet = " · ".join(bits) or "OpenAlex works by keywords.id"
        hits.append(
            Hit(
                title=f"{label} works",
                url=_oa_url(key, query),
                snippet=snippet,
                source="oakwid",
            )
        )
    return hits[:limit]
