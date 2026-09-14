"""Research tool with a pluggable SearchAdapter interface.

Default live backend is Wikipedia OpenSearch (stdlib urllib, no API key).
Tests inject FixtureAdapter so they never hit the network.
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
        req = Request(url, headers={"User-Agent": "EternalForge/0.1 (research tool)"})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return [
                Hit(
                    title=f"Wikipedia unavailable for: {q}",
                    url="",
                    snippet="Network or parse error; use FixtureAdapter offline.",
                    source=self.name,
                )
            ]
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
                    source=self.name,
                )
            )
        return hits[:limit]


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
        lines.append(f"{i}. {hit.title}")
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
