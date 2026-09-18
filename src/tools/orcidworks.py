"""ORCID works extras SearchAdapter (public works list; no key)."""

from __future__ import annotations

import json
import re
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

ORCID_WORKS = "https://pub.orcid.org/v3.0"
ORCID_EXPANDED = "https://pub.orcid.org/v3.0/expanded-search/"
ORCID_PROFILE = "https://orcid.org"
ORCID_RE = re.compile(r"(?:orcid\.org/)?(\d{4}-\d{4}-\d{4}-\d{3}[\dXx])\b")


class OrcidWorksAdapter:
    """ORCID public works list with type, year, journal, and DOI. No key."""

    name = "orcidworks"
    endpoint = ORCID_WORKS

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        orcid = extract_orcid_id(q)
        if not orcid:
            orcid = _lookup_orcid(q, self.timeout)
        if not orcid:
            return []
        url = f"{self.endpoint}/{quote(orcid)}/works"
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
        return parse_orcidworks_payload(payload, limit=limit, orcid=orcid)


def extract_orcid_id(text: str) -> str:
    """Return a normalized ORCID iD if one appears in text."""
    match = ORCID_RE.search(text or "")
    if not match:
        return ""
    return match.group(1).upper()


def _lookup_orcid(query: str, timeout: float) -> str:
    url = f"{ORCID_EXPANDED}?q={quote(query)}&rows=1&start=0"
    req = Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (URLError, TimeoutError, json.JSONDecodeError, OSError):
        return ""
    if not isinstance(payload, dict):
        return ""
    rows = payload.get("expanded-result") or payload.get("result") or []
    if not isinstance(rows, list):
        return ""
    for row in rows:
        if not isinstance(row, dict):
            continue
        raw = row.get("orcid-id") or row.get("orcid") or ""
        ident = row.get("orcid-identifier") or {}
        if not raw and isinstance(ident, dict):
            raw = ident.get("path") or ident.get("uri") or ""
        found = extract_orcid_id(str(raw or ""))
        if found:
            return found
    return ""


def _as_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        return str(
            value.get("value")
            or value.get("content")
            or value.get("title")
            or ""
        ).strip()
    return str(value).strip()


def _rows_from_payload(payload: dict) -> list[dict]:
    groups = payload.get("group") or payload.get("groups") or payload.get("works") or []
    if isinstance(payload.get("work-summary"), list):
        return [row for row in payload["work-summary"] if isinstance(row, dict)]
    rows: list[dict] = []
    if not isinstance(groups, list):
        return rows
    for group in groups:
        if not isinstance(group, dict):
            continue
        summaries = group.get("work-summary") or group.get("workSummary") or []
        if isinstance(summaries, dict):
            summaries = [summaries]
        if isinstance(summaries, list) and summaries:
            first = summaries[0]
            if isinstance(first, dict):
                rows.append(first)
        elif group.get("title") or group.get("put-code"):
            rows.append(group)
    return rows


def _title(row: dict) -> str:
    raw = row.get("title") or {}
    if isinstance(raw, dict):
        inner = raw.get("title") or raw.get("value") or raw
        return _as_text(inner)
    return _as_text(raw)


def _year(row: dict) -> str:
    pub = row.get("publication-date") or row.get("publicationDate") or {}
    if isinstance(pub, dict):
        year = pub.get("year") or {}
        text = _as_text(year) or str(pub.get("value") or "").strip()
        return text
    return ""


def _work_type(row: dict) -> str:
    return str(row.get("type") or row.get("work-type") or "").replace("-", " ").strip()


def _journal(row: dict) -> str:
    raw = row.get("journal-title") or row.get("journalTitle") or row.get("journal") or {}
    return _as_text(raw)


def _doi(row: dict) -> str:
    ids = row.get("external-ids") or row.get("externalIds") or {}
    items = []
    if isinstance(ids, dict):
        items = ids.get("external-id") or ids.get("externalId") or []
    elif isinstance(ids, list):
        items = ids
    if not isinstance(items, list):
        return ""
    for item in items:
        if not isinstance(item, dict):
            continue
        kind = str(item.get("external-id-type") or item.get("type") or "").lower()
        value = str(
            item.get("external-id-value")
            or item.get("value")
            or ""
        ).strip()
        if kind == "doi" and value:
            return value
    return ""


def _work_url(row: dict, doi: str, orcid: str) -> str:
    raw = row.get("url") or {}
    href = _as_text(raw)
    if href.startswith("http"):
        return href
    if doi:
        clean = doi.lower().removeprefix("https://doi.org/").removeprefix("doi:")
        return f"https://doi.org/{clean}"
    if orcid:
        return f"{ORCID_PROFILE}/{orcid}"
    return ""


def parse_orcidworks_payload(
    payload: dict,
    limit: int = 5,
    orcid: str = "",
) -> list[Hit]:
    """Map ORCID /works JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = _title(row)
        doi = _doi(row)
        url = _work_url(row, doi, orcid)
        bits = [p for p in (_work_type(row), _year(row), _journal(row), doi) if p]
        snippet = " · ".join(bits) or "ORCID work"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "ORCID work",
                url=url,
                snippet=snippet,
                source="orcidworks",
            )
        )
    return hits[:limit]
