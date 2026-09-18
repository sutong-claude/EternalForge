"""ORCID extras SearchAdapter (names, institutions; no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

ORCID_EXPANDED = "https://pub.orcid.org/v3.0/expanded-search/"
ORCID_PROFILE = "https://orcid.org"


class OrcidExtraAdapter:
    """ORCID public expanded-search with names and institutions. No key."""

    name = "orcidextra"
    endpoint = ORCID_EXPANDED

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?q={quote(q)}&rows={limit}&start=0"
        req = Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
        )
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_orcidextra_payload(payload, limit=limit)


def _rows_from_payload(payload: dict) -> list[dict]:
    if isinstance(payload.get("expanded-result"), list):
        rows = payload["expanded-result"]
    elif isinstance(payload.get("result"), list):
        rows = payload["result"]
    elif isinstance(payload.get("results"), list):
        rows = payload["results"]
    else:
        inner = payload.get("expanded-search") or payload.get("search") or {}
        if isinstance(inner, dict):
            rows = (
                inner.get("expanded-result")
                or inner.get("result")
                or inner.get("results")
                or []
            )
        else:
            rows = []
    return [row for row in rows if isinstance(row, dict)]


def _orcid_id(row: dict) -> str:
    raw = row.get("orcid-id") or row.get("orcid") or ""
    if isinstance(raw, dict):
        raw = raw.get("path") or raw.get("uri") or raw.get("id") or ""
    ident = row.get("orcid-identifier") or row.get("orcidIdentifier") or {}
    if not raw and isinstance(ident, dict):
        raw = ident.get("path") or ident.get("uri") or ident.get("id") or ""
    text = str(raw or "").strip()
    if text.startswith("http"):
        text = text.rstrip("/").split("/")[-1]
    return text


def _display_name(row: dict) -> str:
    credit = str(row.get("credit-name") or row.get("creditName") or "").strip()
    if credit:
        return credit
    given = str(row.get("given-names") or row.get("givenNames") or row.get("given") or "").strip()
    family = str(row.get("family-names") or row.get("familyNames") or row.get("family") or "").strip()
    joined = " ".join(p for p in (given, family) if p)
    if joined:
        return joined
    other = row.get("other-name") or row.get("otherNames") or []
    if isinstance(other, list) and other:
        first = other[0]
        if isinstance(first, dict):
            return str(first.get("content") or first.get("value") or "").strip()
        return str(first or "").strip()
    return ""


def _institutions(row: dict) -> str:
    raw = row.get("institution-name") or row.get("institutionName") or row.get("affiliations") or []
    if isinstance(raw, str):
        return raw.strip()
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:2]:
        if isinstance(item, dict):
            name = str(
                item.get("name")
                or item.get("institution-name")
                or item.get("value")
                or ""
            ).strip()
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def _other_names(row: dict) -> str:
    raw = row.get("other-name") or row.get("otherNames") or []
    if isinstance(raw, str):
        return raw.strip()
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:2]:
        if isinstance(item, dict):
            name = str(item.get("content") or item.get("value") or item.get("name") or "").strip()
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def parse_orcidextra_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map ORCID expanded-search JSON into extras Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        orcid = _orcid_id(row)
        title = _display_name(row) or orcid
        url = f"{ORCID_PROFILE}/{orcid}" if orcid else ""
        inst = _institutions(row)
        aliases = _other_names(row)
        bits = [p for p in (orcid, inst, aliases) if p]
        snippet = " · ".join(bits) or "ORCID extras profile"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "ORCID",
                url=url,
                snippet=snippet,
                source="orcidextra",
            )
        )
    return hits[:limit]
