"""OpenAlex works-by-year extras SearchAdapter (group_by year; no key)."""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

OA_WORKS = "https://api.openalex.org/works"


class OaYearAdapter:
    """OpenAlex works search grouped by publication year. No key."""

    name = "oayear"
    endpoint = OA_WORKS

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?search={quote(q)}&group_by=publication_year&per-page={limit}"
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
        return parse_oayear_payload(payload, limit=limit, query=q)


def _intish(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value or "").strip()
    if text.isdigit():
        return int(text)
    return None


def _year_of(row: dict) -> str:
    raw = row.get("key_display_name") or row.get("key") or row.get("year") or ""
    text = str(raw).strip()
    if text.lower() in {"", "unknown", "null", "none"}:
        return ""
    if text.isdigit() and len(text) == 4:
        return text
    year = _intish(raw)
    if year and 1000 <= year <= 2100:
        return str(year)
    return ""


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
    rows = payload.get("group_by") or payload.get("counts_by_year") or payload.get("years") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def _year_url(year: str, query: str = "") -> str:
    q = query.strip()
    if q:
        return f"https://openalex.org/works?search={quote(q)}&filter=publication_year:{quote(year)}"
    return f"https://openalex.org/works?filter=publication_year:{quote(year)}"


def parse_oayear_payload(payload: dict, limit: int = 5, query: str = "") -> list[Hit]:
    """Map OpenAlex works group_by year JSON into research Hits."""
    rows: list[tuple[int, dict]] = []
    for row in _rows_from_payload(payload):
        year = _year_of(row)
        if not year:
            continue
        rows.append((int(year), row))
    rows.sort(key=lambda item: item[0], reverse=True)
    hits: list[Hit] = []
    for year_n, row in rows:
        year = str(year_n)
        works = _works_count(row)
        cites = _cites_count(row)
        bits = [p for p in (
            f"{works} works" if works else "",
            f"{cites} cites" if cites else "",
        ) if p]
        snippet = " · ".join(bits) or "OpenAlex works by year"
        hits.append(
            Hit(
                title=f"{year} works",
                url=_year_url(year, query),
                snippet=snippet,
                source="oayear",
            )
        )
    return hits[:limit]
