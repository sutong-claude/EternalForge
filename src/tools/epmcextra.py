"""Europe PMC extras SearchAdapter (cites, OA, type, keywords; no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.europepmc import (
    EUROPEPMC_SEARCH,
    _article_url,
    _format_authors,
    _rows_from_payload,
)
from tools.research import USER_AGENT, Hit, _unavailable


class EpmcExtraAdapter:
    """Europe PMC core search with cites, OA, type, and keywords. No key."""

    name = "epmcextra"
    endpoint = EUROPEPMC_SEARCH

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = (
            f"{self.endpoint}?query={quote(q)}&format=json"
            f"&pageSize={limit}&resultType=core"
        )
        req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_epmcextra_payload(payload, limit=limit)


def _cites(row: dict) -> str:
    count = row.get("citedByCount") or row.get("citationCount") or row.get("citedBy")
    if isinstance(count, (int, float)) and count:
        return f"{int(count)} cites"
    text = str(count or "").strip()
    if text.isdigit() and int(text):
        return f"{int(text)} cites"
    return ""


def _oa(row: dict) -> str:
    raw = row.get("isOpenAccess") or row.get("openAccess") or row.get("inEPMC")
    if raw is True or str(raw).strip().upper() in {"Y", "YES", "TRUE", "OPEN"}:
        return "OA"
    if raw is False or str(raw).strip().upper() in {"N", "NO", "FALSE", "CLOSED"}:
        return "closed"
    pmcid = str(row.get("pmcid") or "").strip()
    if pmcid:
        return "OA"
    return ""


def _kind(row: dict) -> str:
    raw = row.get("pubType") or row.get("pubTypeList") or row.get("source") or ""
    if isinstance(raw, dict):
        inner = raw.get("pubType") or raw.get("type") or []
        raw = inner
    if isinstance(raw, list):
        names = [str(item).strip() for item in raw[:2] if str(item).strip()]
        return ", ".join(names)
    return str(raw or "").strip()


def _keywords(row: dict) -> str:
    raw = row.get("keywordList") or row.get("keywords") or row.get("meshHeadingList") or []
    if isinstance(raw, dict):
        raw = raw.get("keyword") or raw.get("meshHeading") or raw.get("keywords") or []
    if isinstance(raw, str):
        return raw.strip()
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:2]:
        if isinstance(item, dict):
            name = str(
                item.get("keyword")
                or item.get("descriptorName")
                or item.get("meshHeading")
                or item.get("label")
                or ""
            ).strip()
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def _language(row: dict) -> str:
    raw = row.get("language") or row.get("languages") or ""
    if isinstance(raw, list) and raw:
        return str(raw[0] or "").strip()
    return str(raw or "").strip()


def parse_epmcextra_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map Europe PMC core JSON into extras Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = str(row.get("title") or "").strip().rstrip(".")
        url = _article_url(row)
        authors = _format_authors(row)
        journal = str(row.get("journalTitle") or row.get("journal") or "").strip()
        year = str(row.get("pubYear") or row.get("firstPublicationDate") or row.get("year") or "").strip()
        if len(year) > 4 and year[:4].isdigit():
            year = year[:4]
        kind = _kind(row)
        access = _oa(row)
        cites = _cites(row)
        keywords = _keywords(row)
        lang = _language(row)
        abstract = str(row.get("abstractText") or row.get("abstract") or "").strip()
        bits = [p for p in (authors, journal, year, kind, access, cites, keywords, lang) if p]
        snippet = " · ".join(bits)
        if abstract:
            snippet = f"{snippet} — {abstract}" if snippet else abstract
        snippet = snippet or "Europe PMC extras article"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "Europe PMC",
                url=url,
                snippet=snippet,
                source="epmcextra",
            )
        )
    return hits[:limit]
