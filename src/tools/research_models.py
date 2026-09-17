"""Hit model, SearchAdapter protocol, and fixture backend."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


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


def unavailable(name: str, query: str) -> list[Hit]:
    return [
        Hit(
            title=f"{name} unavailable for: {query}",
            url="",
            snippet="Network or parse error; use FixtureAdapter offline.",
            source=name,
        )
    ]
