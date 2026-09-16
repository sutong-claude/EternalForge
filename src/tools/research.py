"""Research tool with a pluggable SearchAdapter interface.

Live backends: Wikipedia OpenSearch, DuckDuckGo Instant Answer,
Open Library, Hacker News Algolia, arXiv, Crossref, Semantic Scholar,
PubMed, and Europe PMC (stdlib urllib, no API key). Tests inject
FixtureAdapter or call parse_*_payload helpers so they never hit the
network. Backend ``multi`` merges the live adapters.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable, Protocol
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from core.memory import Journal, MemoryEntry, normalize_tags

USER_AGENT = "EternalForge/0.1 (research tool)"


@dataclass(frozen=True)
class Hit:
    title: str
    url: str
    snippet: str
    source: str = ""

    def as_dict(self) -> dict[str, str]:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source,
        }


class SearchAdapter(Protocol):
    name: str

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        ...


class FixtureAdapter:
    """Deterministic in-memory adapter for tests and offline demos."""

    name = "fixture"

    def __init__(self, catalog: dict[str, list[Hit]] | None = None) -> None:
        self.catalog = catalog or {
            "eternalforge": [
                Hit(
                    title="EternalForge",
                    url="https://github.com/sutong-claude/EternalForge",
                    snippet="Personal AI research and development platform.",
                    source="fixture",
                )
            ]
        }

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip().lower()
        if not q:
            return []
        hits: list[Hit] = []
        for key, items in self.catalog.items():
            if q in key or key in q:
                hits.extend(items)
        if not hits:
            hits = [
                Hit(
                    title=f"No catalog match for {query}",
                    url="",
                    snippet="FixtureAdapter only returns seeded topics.",
                    source="fixture",
                )
            ]
        return hits[: max(0, max_results)]


def _unavailable(name: str, query: str) -> list[Hit]:
    return [
        Hit(
            title=f"{name} unavailable for: {query}",
            url="",
            snippet="Network or parse error; use FixtureAdapter offline.",
            source=name,
        )
    ]


class WikipediaAdapter:
    """Wikipedia OpenSearch over HTTPS. Safe to call without credentials."""

    name = "wikipedia"
    endpoint = "https://en.wikipedia.org/w/api.php"

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = (
            f"{self.endpoint}?action=opensearch&format=json"
            f"&limit={limit}&namespace=0&search={quote(q)}"
        )
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        return parse_wikipedia_payload(payload, limit=limit)


def parse_wikipedia_payload(payload: object, limit: int = 5) -> list[Hit]:
    if not isinstance(payload, list) or len(payload) < 4:
        return []
    titles, snippets, urls = payload[1], payload[2], payload[3]
    hits: list[Hit] = []
    for title, snippet, link in zip(titles, snippets, urls):
        hits.append(
            Hit(
                title=str(title),
                url=str(link),
                snippet=str(snippet) or f"Wikipedia article: {title}",
                source="wikipedia",
            )
        )
    return hits[:limit]


class DuckDuckGoAdapter:
    """DuckDuckGo Instant Answer API. No key required."""

    name = "duckduckgo"
    endpoint = "https://api.duckduckgo.com/"

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = (
            f"{self.endpoint}?q={quote(q)}&format=json"
            f"&no_html=1&skip_disambig=1"
        )
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_duckduckgo_payload(payload, limit=limit)


def parse_duckduckgo_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map Instant Answer JSON into Hits (abstract + related topics)."""
    hits: list[Hit] = []
    heading = str(payload.get("Heading") or payload.get("AnswerType") or "DuckDuckGo")
    abstract = str(payload.get("AbstractText") or payload.get("Abstract") or "").strip()
    abstract_url = str(payload.get("AbstractURL") or "").strip()
    answer = str(payload.get("Answer") or "").strip()
    if abstract or answer:
        hits.append(
            Hit(
                title=heading,
                url=abstract_url,
                snippet=abstract or answer,
                source="duckduckgo",
            )
        )
    related = payload.get("RelatedTopics") or []
    if isinstance(related, list):
        for item in related:
            if not isinstance(item, dict):
                continue
            if "Topics" in item and isinstance(item["Topics"], list):
                for nested in item["Topics"]:
                    hit = _ddg_topic_hit(nested)
                    if hit:
                        hits.append(hit)
                continue
            hit = _ddg_topic_hit(item)
            if hit:
                hits.append(hit)
    seen: set[tuple[str, str]] = set()
    unique: list[Hit] = []
    for hit in hits:
        key = (hit.title, hit.url)
        if key in seen:
            continue
        seen.add(key)
        unique.append(hit)
    return unique[:limit]


def _ddg_topic_hit(item: object) -> Hit | None:
    if not isinstance(item, dict):
        return None
    text = str(item.get("Text") or "").strip()
    url = str(item.get("FirstURL") or "").strip()
    if not text and not url:
        return None
    title = text.split(" -", 1)[0].strip() or text[:80] or url
    return Hit(title=title, url=url, snippet=text, source="duckduckgo")


ADAPTERS: dict[str, type] = {
    "wikipedia": WikipediaAdapter,
    "duckduckgo": DuckDuckGoAdapter,
    "ddg": DuckDuckGoAdapter,
    "fixture": FixtureAdapter,
}

_LIVE_EXTRA = {
    "openlibrary",
    "ol",
    "books",
    "hackernews",
    "hn",
    "algolia",
    "arxiv",
    "papers",
    "preprint",
    "crossref",
    "doi",
    "works",
    "semanticscholar",
    "s2",
    "scholar",
    "pubmed",
    "ncbi",
    "medline",
    "europepmc",
    "epmc",
    "europe",
    "multi",
    "all",
}


def get_adapter(name: str | None = None) -> SearchAdapter:
    key = (name or "wikipedia").strip().lower()
    if key in _LIVE_EXTRA:
        from tools import arxiv as axmod
        from tools import crossref as xrmod
        from tools import europepmc as epmcmod
        from tools import hackernews as hnmod
        from tools import openlibrary as olmod
        from tools import pubmed as pmmod
        from tools import semanticscholar as s2mod

        if key in {"multi", "all"}:
            return olmod.MultiAdapter()
        if key in {"hackernews", "hn", "algolia"}:
            return hnmod.HackerNewsAdapter()
        if key in {"arxiv", "papers", "preprint"}:
            return axmod.ArxivAdapter()
        if key in {"crossref", "doi", "works"}:
            return xrmod.CrossrefAdapter()
        if key in {"semanticscholar", "s2", "scholar"}:
            return s2mod.SemanticScholarAdapter()
        if key in {"pubmed", "ncbi", "medline"}:
            return pmmod.PubMedAdapter()
        if key in {"europepmc", "epmc", "europe"}:
            return epmcmod.EuropePMCAdapter()
        return olmod.OpenLibraryAdapter()
    cls = ADAPTERS.get(key)
    if cls is None:
        known = ", ".join(sorted(set(ADAPTERS) | _LIVE_EXTRA))
        raise ValueError(f"Unknown search backend {name!r}. Known: {known}")
    return cls()


def default_adapter() -> SearchAdapter:
    return WikipediaAdapter()


def search(
    query: str,
    max_results: int = 5,
    adapter: SearchAdapter | None = None,
) -> list[Hit]:
    backend = adapter or default_adapter()
    return backend.search(query, max_results=max_results)


def summarize(text: str, max_length: int = 300) -> str:
    compact = " ".join(text.split())
    if len(compact) <= max_length:
        return compact
    return compact[: max_length - 3] + "..."


def format_hits(hits: list[Hit]) -> str:
    if not hits:
        return "(no results)"
    lines: list[str] = []
    for i, hit in enumerate(hits, 1):
        label = f"{hit.title} [{hit.source}]" if hit.source else hit.title
        lines.append(f"{i}. {label}")
        if hit.url:
            lines.append(f"   {hit.url}")
        if hit.snippet:
            lines.append(f"   {summarize(hit.snippet, 180)}")
    return "\n".join(lines)


def record_hits(
    query: str,
    hits: list[Hit],
    journal: Journal | None = None,
    root: Path | None = None,
    tags: Iterable[str] | None = None,
) -> MemoryEntry:
    """Append a kind=research journal entry summarizing the hits."""
    log = journal or Journal((root or Path.cwd()) / "memory" / "journal.jsonl")
    extra = list(tags) if tags is not None else []
    sources = [hit.source for hit in hits if hit.source]
    entry = MemoryEntry.now(
        "research",
        f"Research {query!r}: {len(hits)} hit(s)",
        format_hits(hits),
        tags=normalize_tags(["research", *sources, *extra]),
    )
    log.append(entry)
    return entry


def parse_openlibrary_payload(payload: dict, limit: int = 5):
    from tools.openlibrary import parse_openlibrary_payload as _parse
    return _parse(payload, limit=limit)


def parse_hackernews_payload(payload: dict, limit: int = 5):
    from tools.hackernews import parse_hackernews_payload as _parse
    return _parse(payload, limit=limit)


def parse_arxiv_payload(payload: dict, limit: int = 5):
    from tools.arxiv import parse_arxiv_payload as _parse
    return _parse(payload, limit=limit)


def parse_crossref_payload(payload: dict, limit: int = 5):
    from tools.crossref import parse_crossref_payload as _parse
    return _parse(payload, limit=limit)


def parse_semanticscholar_payload(payload: dict, limit: int = 5):
    from tools.semanticscholar import parse_semanticscholar_payload as _parse
    return _parse(payload, limit=limit)


def parse_pubmed_payload(payload: dict, limit: int = 5):
    from tools.pubmed import parse_pubmed_payload as _parse
    return _parse(payload, limit=limit)


def parse_europepmc_payload(payload: dict, limit: int = 5):
    from tools.europepmc import parse_europepmc_payload as _parse
    return _parse(payload, limit=limit)


def merge_hits(*groups, limit: int = 5):
    from tools.openlibrary import merge_hits as _merge
    return _merge(*groups, limit=limit)


def __getattr__(name: str):
    if name in {"OpenLibraryAdapter", "MultiAdapter"}:
        from tools import openlibrary as olmod
        return getattr(olmod, name)
    if name == "HackerNewsAdapter":
        from tools.hackernews import HackerNewsAdapter
        return HackerNewsAdapter
    if name == "ArxivAdapter":
        from tools.arxiv import ArxivAdapter
        return ArxivAdapter
    if name == "CrossrefAdapter":
        from tools.crossref import CrossrefAdapter
        return CrossrefAdapter
    if name == "SemanticScholarAdapter":
        from tools.semanticscholar import SemanticScholarAdapter
        return SemanticScholarAdapter
    if name == "PubMedAdapter":
        from tools.pubmed import PubMedAdapter
        return PubMedAdapter
    if name == "EuropePMCAdapter":
        from tools.europepmc import EuropePMCAdapter
        return EuropePMCAdapter
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
