"""OpenAlex institutions extras SearchAdapter (institutions API; no key)."""

from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

OA_INSTITUTIONS = "https://api.openalex.org/institutions"
OA_SELECT = (
    "id,display_name,display_name_acronyms,display_name_alternatives,"
    "country_code,type,homepage_url,works_count,cited_by_count,"
    "associated_institutions,ids"
)


class OaInstitutionAdapter:
    """OpenAlex institutions search with type, country, alts, works, cites. No key."""

    name = "oainstitution"
    endpoint = OA_INSTITUTIONS

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
        return parse_oainstitution_payload(payload, limit=limit)


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = payload.get("results") or payload.get("institutions") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    return []


def _type(row: dict) -> str:
    return str(row.get("type") or "").strip().lower()


def _country(row: dict) -> str:
    raw = row.get("country_code") or row.get("country_codes") or row.get("country")
    if isinstance(raw, list):
        codes = [str(item).strip().upper() for item in raw if str(item).strip()]
        return ", ".join(codes[:3])
    return str(raw or "").strip().upper()


def _alts(row: dict) -> str:
    parts: list[str] = []
    for key in ("display_name_acronyms", "display_name_alternatives", "alternate_titles"):
        raw = row.get(key) or []
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
        if len(unique) >= 3:
            break
    return ", ".join(unique)


def _associated(row: dict) -> str:
    raw = row.get("associated_institutions") or row.get("lineage") or []
    if isinstance(raw, dict):
        name = str(raw.get("display_name") or raw.get("name") or "").strip()
        rel = str(raw.get("relationship") or "").strip()
        if name and rel:
            return f"{rel} {name}"
        return f"assoc {name}" if name else ""
    if not isinstance(raw, list):
        return ""
    for item in raw:
        if not isinstance(item, dict):
            continue
        name = str(item.get("display_name") or item.get("name") or "").strip()
        if not name:
            continue
        rel = str(item.get("relationship") or "").strip()
        return f"{rel} {name}" if rel else f"assoc {name}"
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


def _ror(row: dict) -> str:
    ids = row.get("ids") if isinstance(row.get("ids"), dict) else {}
    ror = str(ids.get("ror") or row.get("ror") or "").strip()
    if not ror:
        return ""
    short = ror.rstrip("/").split("/")[-1]
    return f"ror:{short}" if short else ""


def _institution_url(row: dict) -> str:
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


def parse_oainstitution_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map OpenAlex /institutions JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = str(row.get("display_name") or row.get("name") or "").strip()
        url = _institution_url(row)
        bits = [
            p
            for p in (
                _type(row),
                _country(row),
                _alts(row),
                _associated(row),
                _ror(row),
                _works(row),
                _cites(row),
            )
            if p
        ]
        snippet = " · ".join(bits) or "OpenAlex institution"
        if not title:
            continue
        hits.append(
            Hit(
                title=title,
                url=url,
                snippet=snippet,
                source="oainstitution",
            )
        )
    return hits[:limit]
