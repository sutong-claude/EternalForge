"""OpenAlex works-by-has_oa_bronze extras SearchAdapter (group_by; no key)."""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

OA_WORKS = "https://api.openalex.org/works"
FIELD = "has_oa_bronze"


class OaHasOaBronzeAdapter:
    """OpenAlex works search grouped by has_oa_bronze. No key."""

    name = "oahasobrnz"
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
        return parse_oahasobrnz_payload(payload, limit=limit, query=q)


def _intish(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value or "").strip()
    if text.isdigit():
        return int(text)
    return None


def _flag(row: dict) -> bool | None:
    raw = row.get("key")
    if raw is None:
        raw = row.get(FIELD)
    if raw is None:
        raw = row.get("has_bronze")
    if raw is None:
        raw = row.get("key_display_name")
    if isinstance(raw, bool):
        return raw
    text = str(raw or "").strip().lower().replace("_", " ").replace("-", " ")
    if text in {
        "true",
        "yes",
        "1",
        "has oa bronze",
        "bronze",
        "bronze oa",
        "with bronze oa",
        "oa bronze",
    }:
        return True
    if text in {
        "false",
        "no",
        "0",
        "no oa bronze",
        "without bronze oa",
        "missing bronze oa",
        "not bronze",
    }:
        return False
    return None


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
        or payload.get(FIELD)
        or payload.get("has_bronze")
        or []
    )
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def _oabronze_url(flag: bool, query: str = "") -> str:
    q = query.strip()
    filt = f"{FIELD}:{str(flag).lower()}"
    if q:
        return f"https://openalex.org/works?search={quote(q)}&filter={filt}"
    return f"https://openalex.org/works?filter={filt}"


def parse_oahasobrnz_payload(payload: dict, limit: int = 5, query: str = "") -> list[Hit]:
    """Map OpenAlex works group_by has_oa_bronze JSON into Hits."""
    rows: list[tuple[int, dict]] = []
    for row in _rows_from_payload(payload):
        flag = _flag(row)
        if flag is None:
            continue
        rows.append((_works_count(row), row))
    rows.sort(key=lambda item: item[0], reverse=True)
    hits: list[Hit] = []
    for works, row in rows:
        flag = _flag(row)
        if flag is None:
            continue
        cites = _cites_count(row)
        bits = [p for p in (
            f"{works} works" if works else "",
            f"{cites} cites" if cites else "",
        ) if p]
        snippet = " · ".join(bits) or "OpenAlex works by has_oa_bronze"
        title = (
            "Works with bronze OA"
            if flag
            else "Works without bronze OA"
        )
        hits.append(
            Hit(
                title=title,
                url=_oabronze_url(flag, query),
                snippet=snippet,
                source="oahasobrnz",
            )
        )
    return hits[:limit]
