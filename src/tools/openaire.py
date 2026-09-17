"""OpenAIRE SearchAdapter (Graph researchProducts JSON, no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

OPENAIRE_PRODUCTS = "https://api.openaire.eu/graph/v2/researchProducts"


class OpenaireAdapter:
    """OpenAIRE Graph research-product search. No key required."""

    name = "openaire"
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
        return parse_openaire_payload(payload, limit=limit)


def _rows_from_payload(payload: dict) -> list[dict]:
    rows = payload.get("results") or payload.get("researchProducts") or payload.get("hits") or []
    if isinstance(rows, list):
        return [item for item in rows if isinstance(item, dict)]
    if isinstance(rows, dict):
        inner = rows.get("result") or rows.get("results") or []
        if isinstance(inner, list):
            return [item for item in inner if isinstance(item, dict)]
        if isinstance(inner, dict):
            return [inner]
    return []


def _title(row: dict) -> str:
    return str(row.get("mainTitle") or row.get("title") or row.get("name") or "").strip()


def _authors(row: dict) -> str:
    raw = row.get("authors") or row.get("author") or []
    if isinstance(raw, str):
        parts = [p.strip() for p in raw.replace(";", ",").split(",") if p.strip()]
        return ", ".join(parts[:3])
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:3]:
        if isinstance(item, dict):
            name = str(item.get("fullName") or item.get("name") or "").strip()
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def _year(row: dict) -> str:
    raw = row.get("publicationDate") or row.get("dateOfCollection") or row.get("year") or ""
    text = str(raw).strip()
    return text[:4] if text[:4].isdigit() else text


def _kind(row: dict) -> str:
    return str(row.get("type") or "").strip()


def _abstract(row: dict) -> str:
    raw = row.get("descriptions") or row.get("description") or ""
    if isinstance(raw, list):
        parts = [str(item).strip() for item in raw if str(item).strip()]
        return parts[0] if parts else ""
    return str(raw or "").strip()


def _doi(row: dict) -> str:
    pids = row.get("pids") or row.get("pid") or []
    if isinstance(pids, dict):
        pids = [pids]
    if isinstance(pids, list):
        for item in pids:
            if not isinstance(item, dict):
                continue
            scheme = str(item.get("scheme") or item.get("type") or "").lower()
            value = str(item.get("value") or item.get("id") or "").strip()
            nested = item.get("id")
            if isinstance(nested, dict) and not value:
                scheme = str(nested.get("scheme") or scheme).lower()
                value = str(nested.get("value") or "").strip()
            if "doi" in scheme and value:
                return value.removeprefix("https://doi.org/")
    return ""


def _url(row: dict, doi: str) -> str:
    instances = row.get("instances") or row.get("instance") or []
    if isinstance(instances, dict):
        instances = [instances]
    if isinstance(instances, list):
        for inst in instances:
            if not isinstance(inst, dict):
                continue
            urls = inst.get("urls") or inst.get("url") or []
            if isinstance(urls, str) and urls.startswith("http"):
                return urls
            if isinstance(urls, list):
                for item in urls:
                    text = str(item or "").strip()
                    if text.startswith("http"):
                        return text
    repo = str(row.get("codeRepositoryUrl") or "").strip()
    if repo.startswith("http"):
        return repo
    if doi:
        return f"https://doi.org/{doi}"
    product_id = str(row.get("id") or "").strip()
    if product_id:
        return f"https://explore.openaire.eu/search/publication?articleId={product_id}"
    return ""


def parse_openaire_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map OpenAIRE Graph researchProducts JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = _title(row)
        doi = _doi(row)
        url = _url(row, doi)
        authors = _authors(row)
        year = _year(row)
        kind = _kind(row)
        abstract = _abstract(row)
        bits = [p for p in (authors, year, kind) if p]
        snippet = " · ".join(bits)
        if abstract:
            snippet = f"{snippet} · {abstract}" if snippet else abstract
        snippet = snippet or "OpenAIRE research product"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "OpenAIRE",
                url=url,
                snippet=snippet,
                source="openaire",
            )
        )
    return hits[:limit]
