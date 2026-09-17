"""Wikidata SearchAdapter (wbsearchentities JSON, no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

WIKIDATA_API = "https://www.wikidata.org/w/api.php"


class WikidataAdapter:
    """Wikidata entity search. No key required."""

    name = "wikidata"
    endpoint = WIKIDATA_API

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = (
            f"{self.endpoint}?action=wbsearchentities&search={quote(q)}"
            f"&language=en&format=json&limit={limit}"
        )
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_wikidata_payload(payload, limit=limit)


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = payload.get("search") or payload.get("entities") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    if isinstance(rows, dict):
        return [item for item in rows.values() if isinstance(item, dict)]
    return []


def _qid(row: dict) -> str:
    return str(row.get("id") or row.get("title") or "").strip()


def _label(row: dict) -> str:
    label = row.get("label") or row.get("display", {})
    if isinstance(label, dict):
        return str(label.get("value") or label.get("text") or "").strip()
    return str(label or "").strip()


def _description(row: dict) -> str:
    desc = row.get("description") or ""
    if isinstance(desc, dict):
        return str(desc.get("value") or desc.get("text") or "").strip()
    return str(desc or "").strip()


def _url(row: dict, qid: str) -> str:
    raw = str(row.get("concepturi") or row.get("url") or "").strip()
    if raw.startswith("//"):
        raw = "https:" + raw
    if raw.startswith("http"):
        return raw
    if qid:
        return f"https://www.wikidata.org/wiki/{qid}"
    return ""


def parse_wikidata_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map Wikidata wbsearchentities JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        qid = _qid(row)
        title = _label(row)
        url = _url(row, qid)
        desc = _description(row)
        bits = [p for p in (qid, desc) if p]
        snippet = " · ".join(bits) or "Wikidata entity"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or qid or "Wikidata",
                url=url,
                snippet=snippet,
                source="wikidata",
            )
        )
    return hits[:limit]
