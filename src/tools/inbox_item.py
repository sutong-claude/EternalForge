"""Inbox item model, fixture catalog, and adapter protocols."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Protocol


@dataclass(frozen=True)
class InboxItem:
    source: str
    item_id: str
    title: str
    snippet: str = ""
    url: str = ""
    when: str = ""

    def matches(self, query: str | None = None, source: str | None = None) -> bool:
        wanted_source = (source or "").strip().lower()
        if wanted_source and wanted_source not in {"all", "*"}:
            if self.source.strip().lower() != wanted_source:
                return False
        needle = (query or "").strip().lower()
        if not needle:
            return True
        hay = " ".join([self.title, self.snippet, self.item_id, self.url]).lower()
        return needle in hay


DEFAULT_FIXTURE: tuple[InboxItem, ...] = (
    InboxItem(
        source="gmail",
        item_id="m001",
        title="Weekly research digest",
        snippet="Three papers on autonomous agents landed in the inbox.",
        url="https://mail.example/m001",
        when="2026-09-16T09:00:00Z",
    ),
    InboxItem(
        source="gmail",
        item_id="m002",
        title="Invoice reminder",
        snippet="Your workspace invoice is ready.",
        url="https://mail.example/m002",
        when="2026-09-15T18:10:00Z",
    ),
    InboxItem(
        source="drive",
        item_id="d001",
        title="EternalForge notes.gdoc",
        snippet="Shared research outline for Phase 3 productivity.",
        url="https://drive.example/d001",
        when="2026-09-14T12:00:00Z",
    ),
)


class InboxAdapter(Protocol):
    def list_items(
        self,
        source: str | None = None,
        query: str | None = None,
        limit: int = 10,
    ) -> list[InboxItem]:
        ...


class GoogleApiClient(Protocol):
    """Read-only Gmail/Drive listing. Implementations must not log secrets."""

    def list_items(
        self,
        token_path: Path,
        source: str | None = None,
        query: str | None = None,
        limit: int = 10,
    ) -> list[InboxItem]:
        ...


class FixtureInboxAdapter:
    """Deterministic catalog for tests and --offline."""

    def __init__(self, items: Iterable[InboxItem] | None = None) -> None:
        self.items = list(items) if items is not None else list(DEFAULT_FIXTURE)

    def list_items(
        self,
        source: str | None = None,
        query: str | None = None,
        limit: int = 10,
    ) -> list[InboxItem]:
        matched = [item for item in self.items if item.matches(query=query, source=source)]
        cap = max(0, int(limit))
        return matched[:cap]
