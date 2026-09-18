"""OpenAIRE extras SearchAdapter (access right, subjects, cites; no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.openaire import (
    OPENAIRE_PRODUCTS,
    _abstract,
    _authors,
    _doi,
    _kind,
    _rows_from_payload,
    _title,
    _url,
    _year,
)
from tools.research import USER_AGENT, Hit, _unavailable


class OaireExtraAdapter:
    """OpenAIRE Graph search with extra access, subject, and cite fields. No key."""

    name = "oairextra"
    endpoint = OPENAIRE_PRODUCTS

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?search={quote(q)}&pageSize={limit}"
        req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_oairextra_payload(payload, limit=limit)


def _label(raw: object) -> str:
    if isinstance(raw, dict):
        return str(raw.get("label") or raw.get("name") or raw.get("code") or "").strip()
    return str(raw or "").strip()


def _access(row: dict) -> str:
    raw = row.get("bestAccessRight") or row.get("accessRight") or row.get("access_right") or ""
    text = _label(raw).replace("_", " ").replace("-", " ")
    if text:
        return text
    instances = row.get("instances") or []
    if isinstance(instances, dict):
        instances = [instances]
    if isinstance(instances, list):
        for inst in instances:
            if not isinstance(inst, dict):
                continue
            text = _label(inst.get("accessRight") or inst.get("license") or "")
            if text:
                return text.replace("_", " ")
    return ""


def _subjects(row: dict) -> str:
    raw = row.get("subjects") or row.get("subject") or []
    if isinstance(raw, str):
        return raw.strip()
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:2]:
        if isinstance(item, dict):
            inner = item.get("subject") or item.get("label") or item.get("value") or item
            name = _label(inner) if not isinstance(inner, str) else inner.strip()
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def _language(row: dict) -> str:
    raw = row.get("language") or row.get("languages") or ""
    if isinstance(raw, list) and raw:
        return _label(raw[0])
    return _label(raw)


def _cites(row: dict) -> str:
    indicators = row.get("indicators") or {}
    if not isinstance(indicators, dict):
        indicators = {}
    impact = indicators.get("citationImpact") or indicators.get("citation_impact") or {}
    if not isinstance(impact, dict):
        impact = {}
    count = (
        impact.get("citationCount")
        or impact.get("citation_count")
        or row.get("citationCount")
        or row.get("cited_by_count")
    )
    if isinstance(count, (int, float)) and count:
        return f"{int(count)} cites"
    return ""


def _publisher(row: dict) -> str:
    raw = row.get("publishers") or row.get("publisher") or []
    if isinstance(raw, str):
        return raw.strip()
    if isinstance(raw, list):
        names = [_label(item) for item in raw[:1]]
        return next((n for n in names if n), "")
    return _label(raw)


def parse_oairextra_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map OpenAIRE extras researchProducts JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = _title(row)
        doi = _doi(row)
        url = _url(row, doi)
        authors = _authors(row)
        year = _year(row)
        kind = _kind(row)
        access = _access(row)
        subjects = _subjects(row)
        cites = _cites(row)
        lang = _language(row)
        publisher = _publisher(row)
        abstract = _abstract(row)
        bits = [p for p in (authors, year, kind, access, subjects, cites, publisher, lang) if p]
        snippet = " · ".join(bits)
        if abstract:
            snippet = f"{snippet} — {abstract}" if snippet else abstract
        snippet = snippet or "OpenAIRE extras product"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "OpenAIRE",
                url=url,
                snippet=snippet,
                source="oairextra",
            )
        )
    return hits[:limit]
