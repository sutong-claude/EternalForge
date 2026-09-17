"""Live adapter, listing helpers, and journal capture."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
import json

from core.memory import Journal, MemoryEntry, normalize_kind, normalize_tags
from tools.inbox_http import HttpGoogleClient
from tools.inbox_item import FixtureInboxAdapter, GoogleApiClient, InboxAdapter, InboxItem
from tools.inbox_token_io import find_google_token, load_token_payload
from tools.inbox_token_refresh import listing_status_for_payload


@dataclass(frozen=True)
class InboxCredsStatus:
    token_present: bool
    path: str
    listing: str
    adapter: str = "live"

    def format(self) -> str:
        token = "present" if self.token_present else "absent"
        path = self.path or "(none)"
        return (
            f"adapter={self.adapter}\n"
            f"token={token}\n"
            f"path={path}\n"
            f"listing={self.listing}"
        )


class LiveInboxAdapter:
    """Discover a local token path and list via GoogleApiClient when present."""

    def __init__(self, root: Path | None = None, client: GoogleApiClient | None = None) -> None:
        self.root = Path(root) if root is not None else None
        self.token_path = find_google_token(self.root)
        self.client = client if client is not None else HttpGoogleClient()

    def creds_status(self) -> InboxCredsStatus:
        present = self.token_path is not None
        if not present:
            listing = "no-token"
        else:
            listing = listing_status_for_payload(load_token_payload(self.token_path))
        return InboxCredsStatus(
            token_present=present,
            path=str(self.token_path) if self.token_path else "",
            listing=listing,
            adapter="live",
        )

    def list_items(
        self,
        source: str | None = None,
        query: str | None = None,
        limit: int = 10,
    ) -> list[InboxItem]:
        if self.token_path is None:
            return []
        try:
            return list(self.client.list_items(self.token_path, source=source, query=query, limit=limit))
        except (OSError, URLError, HTTPError, json.JSONDecodeError, TimeoutError, ValueError, TypeError):
            return []


def get_inbox_adapter(name: str | None = None, root: Path | None = None) -> InboxAdapter:
    key = (name or "fixture").strip().lower()
    if key in {"live", "gmail", "drive", "google"}:
        return LiveInboxAdapter(root=root)
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


def count_inbox_entries(root: Path, journal: Journal | None = None) -> int:
    """Count journal rows whose kind is inbox (missing journal \u2192 0)."""
    log = journal or Journal(root / "memory" / "journal.jsonl")
    return sum(1 for entry in log.load() if normalize_kind(entry.kind) == "inbox")
