"""Unpaywall SearchAdapter (v2 title search + DOI lookup, email only)."""

from __future__ import annotations

import json
import os
import re
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

UNPAYWALL_SEARCH = "https://api.unpaywall.org/v2/search"
UNPAYWALL_DOI = "https://api.unpaywall.org/v2"
DEFAULT_EMAIL = "eternalforge@users.noreply.github.com"
_DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)


class UnpaywallAdapter:
    """Unpaywall title search / DOI lookup. Email via UNPAYWALL_EMAIL."""

    name = "unpaywall"
    endpoint = UNPAYWALL_SEARCH

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        email = (os.environ.get("UNPAYWALL_EMAIL") or DEFAULT_EMAIL).strip()
        doi = _as_doi(q)
        if doi:
            url = f"{UNPAYWALL_DOI}/{quote(doi)}?email={quote(email)}"
        else:
            url = f"{self.endpoint}?query={quote(q)}&email={quote(email)}"
        req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_unpaywall_payload(payload, limit=limit)


def _as_doi(query: str) -> str:
    text = query.strip()
    lower = text.lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if lower.startswith(prefix):
            text = text[len(prefix) :].strip()
            break
    return text if _DOI_RE.match(text) else ""


def _unwrap(row: dict) -> dict:
    inner = row.get("response")
    return inner if isinstance(inner, dict) else row


def _rows_from_payload(payload: dict) -> list[dict]:
    if payload.get("doi") or payload.get("title") or payload.get("best_oa_location"):
        if "results" not in payload:
            return [payload]
    rows = payload.get("results") or payload.get("docs") or payload.get("data") or []
    if not isinstance(rows, list):
        return []
    out: list[dict] = []
    for item in rows:
        if isinstance(item, dict):
            out.append(_unwrap(item))
    return out


def _authors(row: dict) -> str:
    raw = row.get("z_authors") or row.get("authors") or []
    if not isinstance(raw, list):
        return ""
    names: list[str] = []
    for item in raw[:3]:
        if isinstance(item, dict):
            given = str(item.get("given") or "").strip()
            family = str(item.get("family") or item.get("name") or "").strip()
            name = " ".join(p for p in (given, family) if p) or family
        else:
            name = str(item or "").strip()
        if name:
            names.append(name)
    return ", ".join(names)


def _oa_bits(row: dict) -> str:
    bits: list[str] = []
    if row.get("is_oa") is True:
        bits.append("OA")
    elif row.get("is_oa") is False:
        bits.append("closed")
    status = str(row.get("oa_status") or "").strip()
    if status:
        bits.append(status)
    loc = row.get("best_oa_location")
    if isinstance(loc, dict):
        version = str(loc.get("version") or "").strip()
        license_ = str(loc.get("license") or "").strip()
        if version:
            bits.append(version)
        if license_:
            bits.append(license_)
    return " · ".join(bits)


def _url(row: dict) -> str:
    loc = row.get("best_oa_location")
    if isinstance(loc, dict):
        for key in ("url_for_pdf", "url_for_landing_page", "url"):
            href = str(loc.get(key) or "").strip()
            if href.startswith("http"):
                return href
    doi = str(row.get("doi") or row.get("DOI") or "").strip()
    if doi:
        return f"https://doi.org/{doi.removeprefix('https://doi.org/')}"
    landing = str(row.get("oa_location_url") or row.get("url") or "").strip()
    return landing if landing.startswith("http") else ""


def parse_unpaywall_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map Unpaywall v2 search or DOI JSON into research Hits."""
    hits: list[Hit] = []
    for row in _rows_from_payload(payload):
        title = str(row.get("title") or row.get("genre") or "").strip()
        url = _url(row)
        authors = _authors(row)
        year = str(row.get("year") or "").strip()
        journal = str(row.get("journal_name") or row.get("publisher") or "").strip()
        oa = _oa_bits(row)
        bits = [p for p in (authors, year, journal, oa) if p]
        snippet = " · ".join(bits) or "Unpaywall record"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or "Unpaywall",
                url=url,
                snippet=snippet,
                source="unpaywall",
            )
        )
    return hits[:limit]
