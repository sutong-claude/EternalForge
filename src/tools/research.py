"""Research tool with a pluggable SearchAdapter interface.

Live backends: Wikipedia OpenSearch, DuckDuckGo Instant Answer,
and Open Library (stdlib urllib, no API key). Tests inject
FixtureAdapter or call parse_*_payload helpers so they never hit
the network. Backend ``multi`` merges those three live adapters.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Protocol
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from core.memory import Journal, MemoryEntry

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
    # Deduplicate by URL+title while preserving order.
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


def get_adapter(name: str | None = None) -> SearchAdapter:
    key = (name or "wikipedia").strip().lower()
    if key in {"openlibrary", "ol", "books", "multi", "all"}:
        from tools import openlibrary as olmod
        if key in {"multi", "all"}:
            return olmod.MultiAdapter()
        return olmod.OpenLibraryAdapter()
    cls = ADAPTERS.get(key)
    if cls is None:
        known = ", ".join(sorted(set(ADAPTERS) | {"openlibrary", "multi"}))
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
) -> MemoryEntry:
    """Append a kind=research journal entry summarizing the hits."""
    log = journal or Journal((root or Path.cwd()) / "memory" / "journal.jsonl")
    entry = MemoryEntry.now(
        "research",
        f"Research {query!r}: {len(hits)} hit(s)",
        format_hits(hits),
    )
    log.append(entry)
    return entry


def parse_openlibrary_payload(payload: dict, limit: int = 5):
    from tools.openlibrary import parse_openlibrary_payload as _parse
    return _parse(payload, limit=limit)


def merge_hits(*groups, limit: int = 5):
    from tools.openlibrary import merge_hits as _merge
    return _merge(*groups, limit=limit)


def __getattr__(name: str):
    if name in {"OpenLibraryAdapter", "MultiAdapter"}:
        from tools import openlibrary as olmod
        return getattr(olmod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
