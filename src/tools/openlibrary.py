"""Open Library adapter and multi-backend hit merge."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.arxiv import ArxivAdapter
from tools.core import CoreAdapter
from tools.crfunder import CrFunderAdapter
from tools.crossref import CrossrefAdapter
from tools.datacite import DataCiteAdapter
from tools.dcextra import DataCiteExtraAdapter
from tools.doaj import DoajAdapter
from tools.epmcextra import EpmcExtraAdapter
from tools.europepmc import EuropePMCAdapter
from tools.hackernews import HackerNewsAdapter
from tools.oaauthor import OaAuthorAdapter
from tools.oaconcept import OaConceptAdapter
from tools.oacontinent import OaContinentAdapter
from tools.oacountry import OaCountryAdapter
from tools.oadoi import OaDoiAdapter
from tools.oaextra import OaExtraAdapter
from tools.oafunder import OaFunderAdapter
from tools.oairextra import OaireExtraAdapter
from tools.oainstitution import OaInstitutionAdapter
from tools.oalang import OaLangAdapter
from tools.oaostatus import OaOaStatusAdapter
from tools.oaparatext import OaParatextAdapter
from tools.oapublisher import OaPublisherAdapter
from tools.oaretracted import OaRetractedAdapter
from tools.oasource import OaSourceAdapter
from tools.oasrctype import OaSrcTypeAdapter
from tools.oatopic import OaTopicAdapter
from tools.oatype import OaTypeAdapter
from tools.oayear import OaYearAdapter
from tools.openaire import OpenaireAdapter
from tools.openalex import OpenAlexAdapter
from tools.orcidextra import OrcidExtraAdapter
from tools.orcidworks import OrcidWorksAdapter
from tools.pubmed import PubMedAdapter
from tools.research import (
    USER_AGENT,
    DuckDuckGoAdapter,
    Hit,
    SearchAdapter,
    WikipediaAdapter,
    _unavailable,
)
from tools.s2graph import S2GraphAdapter
from tools.semanticscholar import SemanticScholarAdapter
from tools.unpaywall import UnpaywallAdapter
from tools.wikidata import WikidataAdapter
from tools.xrefextra import XrefExtraAdapter
from tools.zenodo import ZenodoAdapter


def _is_unavailable(hit: Hit) -> bool:
    return hit.title.startswith(f"{hit.source} unavailable for:") and not hit.url


class OpenLibraryAdapter:
    """Open Library Search API. No key required; good for books/authors."""

    name = "openlibrary"
    endpoint = "https://openlibrary.org/search.json"

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?q={quote(q)}&limit={limit}"
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_openlibrary_payload(payload, limit=limit)


def parse_openlibrary_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map Open Library search.json docs into Hits."""
    docs = payload.get("docs") or []
    if not isinstance(docs, list):
        return []
    hits: list[Hit] = []
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        title = str(doc.get("title") or "").strip()
        key = str(doc.get("key") or "").strip()
        authors = doc.get("author_name") or []
        if isinstance(authors, list):
            author = ", ".join(str(a) for a in authors[:3] if a)
        else:
            author = str(authors)
        year = doc.get("first_publish_year")
        bits = [p for p in (author, str(year) if year else "") if p]
        snippet = " · ".join(bits) or str(doc.get("subtitle") or "Open Library work")
        url = f"https://openlibrary.org{key}" if key else ""
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or key or "Open Library",
                url=url,
                snippet=snippet,
                source="openlibrary",
            )
        )
    return hits[:limit]


def _hit_key(hit: Hit) -> str:
    url = hit.url.strip().lower().rstrip("/")
    if url:
        return "url:" + url
    return "title:" + hit.title.strip().lower()


def _dedupe_hits(hits: list[Hit], limit: int) -> list[Hit]:
    seen: set[str] = set()
    unique: list[Hit] = []
    for hit in hits:
        key = _hit_key(hit)
        if key in seen:
            continue
        seen.add(key)
        unique.append(hit)
        if len(unique) >= limit:
            break
    return unique


def merge_hits(*groups: list[Hit], limit: int = 5) -> list[Hit]:
    """Round-robin merge groups, dropping unavailable placeholders when
    any real hit exists, then dedupe by URL (else title).
    """
    real_groups: list[list[Hit]] = []
    fallback: list[Hit] = []
    for group in groups:
        real = [h for h in group if not _is_unavailable(h)]
        if real:
            real_groups.append(real)
        else:
            fallback.extend(group)
    if not real_groups:
        return _dedupe_hits(fallback, limit)

    queues = [list(g) for g in real_groups]
    seen: set[str] = set()
    unique: list[Hit] = []
    while queues and len(unique) < limit:
        next_queues: list[list[Hit]] = []
        for queue in queues:
            while queue:
                hit = queue.pop(0)
                key = _hit_key(hit)
                if key in seen:
                    continue
                seen.add(key)
                unique.append(hit)
                break
            if queue:
                next_queues.append(queue)
            if len(unique) >= limit:
                break
        queues = next_queues
    return unique


class MultiAdapter:
    """Fan-out to several adapters and merge/dedupe their hits."""

    name = "multi"

    def __init__(
        self,
        adapters: list[SearchAdapter] | None = None,
        timeout: float = 8.0,
    ) -> None:
        self.adapters = adapters or [
            WikipediaAdapter(timeout=timeout),
            DuckDuckGoAdapter(timeout=timeout),
            OpenLibraryAdapter(timeout=timeout),
            HackerNewsAdapter(timeout=timeout),
            ArxivAdapter(timeout=timeout),
            CrossrefAdapter(timeout=timeout),
            SemanticScholarAdapter(timeout=timeout),
            PubMedAdapter(timeout=timeout),
            EuropePMCAdapter(timeout=timeout),
            OpenAlexAdapter(timeout=timeout),
            ZenodoAdapter(timeout=timeout),
            DataCiteAdapter(timeout=timeout),
            DoajAdapter(timeout=timeout),
            WikidataAdapter(timeout=timeout),
            OpenaireAdapter(timeout=timeout),
            CoreAdapter(timeout=timeout),
            S2GraphAdapter(timeout=timeout),
            UnpaywallAdapter(timeout=timeout),
            XrefExtraAdapter(timeout=timeout),
            OaExtraAdapter(timeout=timeout),
            OaireExtraAdapter(timeout=timeout),
            EpmcExtraAdapter(timeout=timeout),
            OrcidExtraAdapter(timeout=timeout),
            DataCiteExtraAdapter(timeout=timeout),
            CrFunderAdapter(timeout=timeout),
            OaFunderAdapter(timeout=timeout),
            OrcidWorksAdapter(timeout=timeout),
            OaTopicAdapter(timeout=timeout),
            OaConceptAdapter(timeout=timeout),
            OaSourceAdapter(timeout=timeout),
            OaPublisherAdapter(timeout=timeout),
            OaInstitutionAdapter(timeout=timeout),
            OaAuthorAdapter(timeout=timeout),
            OaYearAdapter(timeout=timeout),
            OaTypeAdapter(timeout=timeout),
            OaLangAdapter(timeout=timeout),
            OaOaStatusAdapter(timeout=timeout),
            OaCountryAdapter(timeout=timeout),
            OaContinentAdapter(timeout=timeout),
            OaSrcTypeAdapter(timeout=timeout),
            OaRetractedAdapter(timeout=timeout),
            OaParatextAdapter(timeout=timeout),
            OaDoiAdapter(timeout=timeout),
        ]

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        groups = [adapter.search(q, max_results=limit) for adapter in self.adapters]
        return merge_hits(*groups, limit=limit)
