"""OpenAlex authors extras SearchAdapter (authors API; no key)."""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

OA_AUTHORS = "https://api.openalex.org/authors"
OA_SELECT = (
    "id,display_name,display_name_alternatives,orcid,"
    "last_known_institutions,affiliations,works_count,cited_by_count,"
    "summary_stats,ids"
)


class OaAuthorAdapter:
    """OpenAlex authors search with ORCID, institution, works, cites. No key."""

    name = "oaauthor"
    endpoint = OA_AUTHORS

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
        return parse_oaauthor_payload(payload, limit=limit)


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = payload.get("results") or payload.get("authors") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def _alts(row: dict) -> str:
    raw = row.get("display_name_alternatives") or row.get("alternate_names") or []
    parts: list[str] = []
    if isinstance(raw, str) and raw.strip():
        parts.append(raw.strip())
    elif isinstance(raw, list):
        parts.extend(str(item).strip() for item in raw if str(item).strip())
    seen: set[str] = set()
    unique: list[str] = []
    for name in parts:
        low = name.lower()
        if low in seen:
            continue
        seen.add(low)
        unique.append(name)
        if len(unique) >= 2:
            break
    return ", ".join(unique)


def _orcid(row: dict) -> str:
    raw = str(row.get("orcid") or "").strip()
    if not raw:
        ids = row.get("ids") if isinstance(row.get("ids"), dict) else {}
        raw = str(ids.get("orcid") or "").strip()
    if not raw:
        return ""
    short = raw.rstrip("/").split("/")[-1]
    return f"orcid:{short}" if short else ""


def _institution(row: dict) -> str:
    raw = row.get("last_known_institutions") or row.get("last_known_institution") or []
    if isinstance(raw, dict):
        raw = [raw]
    if not isinstance(raw, list):
        raw = []
    if not raw:
        aff = row.get("affiliations") or []
        if isinstance(aff, list):
            for item in aff:
                if isinstance(item, dict):
                    inst = item.get("institution") if isinstance(item.get("institution"), dict) else item
                    if isinstance(inst, dict):
                        raw = [inst]
                        break
    for item in raw:
        if not isinstance(item, dict):
            continue
        name = str(item.get("display_name") or item.get("name") or "").strip()
        if not name:
            continue
        country = str(item.get("country_code") or "").strip().upper()
        return f"{name} ({country})" if country else name
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


def _hindex(row: dict) -> str:
    stats = row.get("summary_stats") if isinstance(row.get("summary_stats"), dict) else {}
    value = stats.get("h_index") if stats else row.get("h_index")
    if isinstance(value, (int, float)) and value:
        return f"h={int(value)}"
    text = str(value or "").strip()
    if text.isdigit() and int(text):
        return f"h={text}"
    return ""


def _author_url(row: dict) -> str:
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
    orcid = str(row.get("orcid") or "").strip()
    if orcid.startswith("http"):
        return orcid
    return ""


def parse_oaauthor_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map OpenAlex /authors JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = str(row.get("display_name") or row.get("name") or "").strip()
        url = _author_url(row)
        bits = [
            p
            for p in (
                _orcid(row),
                _institution(row),
                _alts(row),
                _hindex(row),
                _works(row),
                _cites(row),
            )
            if p
        ]
        snippet = " · ".join(bits) or "OpenAlex author"
        if not title:
            continue
        hits.append(
            Hit(
                title=title,
                url=url,
                snippet=snippet,
                source="oaauthor",
            )
        )
    return hits[:limit]
