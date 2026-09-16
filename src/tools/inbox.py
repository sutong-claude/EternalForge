"""Gmail / Drive listing sketch (read-only) with optional capture-to-journal.

Live OAuth is not wired. Tests and CLI --offline use FixtureInboxAdapter so
nothing hits the network. A LiveInboxAdapter stub returns no items when
credentials are absent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Protocol

from core.memory import Journal, MemoryEntry, normalize_tags
from pathlib import Path


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


class LiveInboxAdapter:
    """Placeholder until OAuth tokens exist. Never raises on missing creds."""

    def list_items(
        self,
        source: str | None = None,
        query: str | None = None,
        limit: int = 10,
    ) -> list[InboxItem]:
        return []


def get_inbox_adapter(name: str | None = None) -> InboxAdapter:
    key = (name or "fixture").strip().lower()
    if key in {"live", "gmail", "drive", "google"}:
        return LiveInboxAdapter()
    return FixtureInboxAdapter()


def list_inbox(
    source: str | None = None,
    query: str | None = None,
    limit: int = 10,
    adapter: InboxAdapter | None = None,
) -> list[InboxItem]:
    backend = adapter or FixtureInboxAdapter()
    return backend.list_items(source=source, query=query, limit=limit)


def format_items(items: list[InboxItem]) -> str:
    if not items:
        return "(no inbox items)"
    lines: list[str] = []
    for item in items:
        when = f"\t{item.when}" if item.when else ""
        url = f"\t{item.url}" if item.url else ""
        lines.append(f"{item.source}\t{item.item_id}\t{item.title}{when}{url}")
        if item.snippet:
            lines.append(f"\t{item.snippet}")
    return "\n".join(lines)


@dataclass
class InboxCaptureResult:
    count: int
    items: list[InboxItem] = field(default_factory=list)
    summary: str = ""


def capture_inbox(
    root: Path,
    source: str | None = None,
    query: str | None = None,
    limit: int = 10,
    adapter: InboxAdapter | None = None,
    journal: Journal | None = None,
    tags: Iterable[str] | None = None,
) -> InboxCaptureResult:
    items = list_inbox(source=source, query=query, limit=limit, adapter=adapter)
    memory_dir = root / "memory"
    log = journal or Journal(memory_dir / "journal.jsonl")
    extra = list(tags) if tags is not None else []
    summary = f"Captured {len(items)} inbox item(s)"
    if source:
        summary += f" source={source}"
    if query:
        summary += f" query={query!r}"
    details = format_items(items)
    log.append(
        MemoryEntry.now(
            "inbox",
            summary,
            details,
            tags=normalize_tags(["inbox", "gmail", "drive", *extra]),
        )
    )
    return InboxCaptureResult(count=len(items), items=items, summary=summary)
