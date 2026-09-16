"""PubMed SearchAdapter (NCBI E-utilities esearch + esummary, no key)."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
PUBMED_PAGE = "https://pubmed.ncbi.nlm.nih.gov"


class PubMedAdapter:
    """PubMed via NCBI E-utilities. No key required for light use."""

    name = "pubmed"
    search_endpoint = f"{EUTILS}/esearch.fcgi"
    summary_endpoint = f"{EUTILS}/esummary.fcgi"

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def _get_json(self, url: str) -> object:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        search_url = (
            f"{self.search_endpoint}?db=pubmed&retmode=json"
            f"&retmax={limit}&term={quote(q)}"
        )
        try:
            raw = self._get_json(search_url)
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        ids = _esearch_ids(raw)[:limit]
        if not ids:
            return []
        summary_url = (
            f"{self.summary_endpoint}?db=pubmed&retmode=json"
            f"&id={','.join(ids)}"
        )
        try:
            payload = self._get_json(summary_url)
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_pubmed_payload(payload, limit=limit)


def _esearch_ids(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return []
    result = payload.get("esearchresult") or payload.get("esearchResult") or {}
    if not isinstance(result, dict):
        return []
    raw_ids = result.get("idlist") or result.get("idList") or []
    if not isinstance(raw_ids, list):
        return []
    ids: list[str] = []
    for item in raw_ids:
        pmid = str(item or "").strip()
        if pmid:
            ids.append(pmid)
    return ids


def _format_authors(authors: object) -> str:
    if not isinstance(authors, list):
        return ""
    names: list[str] = []
    for author in authors[:3]:
        if isinstance(author, dict):
            name = str(author.get("name") or author.get("authtype") or "").strip()
        else:
            name = str(author or "").strip()
        if name and name.lower() not in {"author", "collectivename"}:
            names.append(name)
    return ", ".join(names)


def _article_url(row: dict, pmid: str) -> str:
    if pmid:
        return f"{PUBMED_PAGE}/{pmid}/"
    ids = row.get("articleids") or row.get("articleIds") or []
    if isinstance(ids, list):
        for item in ids:
            if not isinstance(item, dict):
                continue
            kind = str(item.get("idtype") or item.get("idType") or "").lower()
            value = str(item.get("value") or "").strip()
            if kind in {"pubmed", "pmid"} and value:
                return f"{PUBMED_PAGE}/{value}/"
            if kind == "doi" and value:
                return f"https://doi.org/{value}"
    doi = str(row.get("elocationid") or row.get("elocationId") or "").strip()
    if doi.lower().startswith("doi:"):
        return f"https://doi.org/{doi.split(':', 1)[1].strip()}"
    return ""


def _row_pmid(uid: str, row: dict) -> str:
    pmid = str(uid or row.get("uid") or row.get("pmid") or "").strip()
    if pmid:
        return pmid
    ids = row.get("articleids") or row.get("articleIds") or []
    if isinstance(ids, list):
        for item in ids:
            if not isinstance(item, dict):
                continue
            kind = str(item.get("idtype") or item.get("idType") or "").lower()
            value = str(item.get("value") or "").strip()
            if kind in {"pubmed", "pmid"} and value:
                return value
    return ""


def parse_pubmed_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map NCBI esummary JSON (or a simple articles list) into Hits."""
    articles = payload.get("articles") or payload.get("resultlist") or []
    if isinstance(articles, list) and articles:
        rows: list[tuple[str, dict]] = []
        for item in articles:
            if isinstance(item, dict):
                rows.append((str(item.get("uid") or item.get("pmid") or ""), item))
        return _hits_from_rows(rows, limit)

    result = payload.get("result") or payload
    if not isinstance(result, dict):
        return []
    uids = result.get("uids") or result.get("uidsList") or []
    if not isinstance(uids, list):
        uids = []
    rows = []
    if uids:
        for uid in uids:
            key = str(uid)
            row = result.get(key)
            if isinstance(row, dict):
                rows.append((key, row))
    else:
        for key, row in result.items():
            if key in {"uids", "uidsList"}:
                continue
            if isinstance(row, dict) and (
                row.get("title") or row.get("uid") or row.get("pmid")
            ):
                rows.append((str(key), row))
    return _hits_from_rows(rows, limit)


def _hits_from_rows(rows: list[tuple[str, dict]], limit: int) -> list[Hit]:
    hits: list[Hit] = []
    for uid, row in rows:
        pmid = _row_pmid(uid, row)
        title = str(row.get("title") or "").strip().rstrip(".")
        url = _article_url(row, pmid)
        authors = _format_authors(row.get("authors") or row.get("authorlist"))
        journal = str(row.get("source") or row.get("fulljournalname") or "").strip()
        pubdate = str(row.get("pubdate") or row.get("sortpubdate") or "").strip()
        bits = [p for p in (authors, journal, pubdate) if p]
        snippet = " · ".join(bits) or "PubMed article"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or f"PMID {pmid}" or "PubMed",
                url=url,
                snippet=snippet,
                source="pubmed",
            )
        )
    return hits[:limit]
