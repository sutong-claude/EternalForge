"""arXiv SearchAdapter (export Atom API, no key)."""

from __future__ import annotations

from xml.etree import ElementTree as ET
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable

ATOM_NS = "{http://www.w3.org/2005/Atom}"


class ArxivAdapter:
    """arXiv API search. No key required; good for papers/preprints."""

    name = "arxiv"
    endpoint = "https://export.arxiv.org/api/query"

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = (
            f"{self.endpoint}?search_query={quote('all:' + q)}"
            f"&start=0&max_results={limit}"
        )
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
        except (URLError, TimeoutError, OSError):
            return _unavailable(self.name, q)
        try:
            payload = parse_arxiv_xml(raw)
        except ET.ParseError:
            return _unavailable(self.name, q)
        return parse_arxiv_payload(payload, limit=limit)


def parse_arxiv_xml(raw: str) -> dict:
    """Turn an Atom feed string into {entries: [...]}."""
    root = ET.fromstring(raw)
    entries: list[dict] = []
    for node in root.findall(f"{ATOM_NS}entry"):
        entry_id = (node.findtext(f"{ATOM_NS}id") or "").strip()
        title = " ".join((node.findtext(f"{ATOM_NS}title") or "").split())
        summary = " ".join((node.findtext(f"{ATOM_NS}summary") or "").split())
        published = (node.findtext(f"{ATOM_NS}published") or "")[:10]
        authors = [
            (a.findtext(f"{ATOM_NS}name") or "").strip()
            for a in node.findall(f"{ATOM_NS}author")
        ]
        authors = [a for a in authors if a]
        html_url = ""
        for link in node.findall(f"{ATOM_NS}link"):
            href = (link.get("href") or "").strip()
            rel = link.get("rel") or ""
            typ = link.get("type") or ""
            if rel == "alternate" or typ == "text/html":
                html_url = href
                break
        if not html_url:
            html_url = entry_id
        entries.append(
            {
                "id": entry_id,
                "title": title,
                "summary": summary,
                "published": published,
                "authors": authors,
                "url": html_url,
            }
        )
    return {"entries": entries}


def parse_arxiv_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map simplified arXiv entries into research Hits."""
    rows = payload.get("entries") or []
    if not isinstance(rows, list):
        return []
    hits: list[Hit] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        title = str(row.get("title") or "").strip()
        url = str(row.get("url") or row.get("id") or "").strip()
        authors = row.get("authors") or []
        if isinstance(authors, list):
            author = ", ".join(str(a) for a in authors[:3] if a)
        else:
            author = str(authors)
        published = str(row.get("published") or "").strip()
        summary = str(row.get("summary") or "").strip()
        bits = [p for p in (author, published) if p]
        snippet = " · ".join(bits)
        if summary:
            snippet = f"{snippet} · {summary}" if snippet else summary
        snippet = snippet or "arXiv preprint"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or url or "arXiv",
                url=url,
                snippet=snippet,
                source="arxiv",
            )
        )
    return hits[:limit]
