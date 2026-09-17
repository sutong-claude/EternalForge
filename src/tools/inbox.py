"""Gmail / Drive listing sketch (read-only) with optional capture-to-journal.

Live OAuth is not called. Tests and CLI --offline use FixtureInboxAdapter so
nothing hits the network. LiveInboxAdapter discovers a token path from env or
local files but never reads token contents into logs, and still returns no
items until a Google client is wired.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import os
from typing import Iterable, Protocol

from core.memory import Journal, MemoryEntry, normalize_kind, normalize_tags


TOKEN_ENV_PATH = "ETERNALFORGE_GOOGLE_TOKEN_PATH"
TOKEN_ENV_DIR = "ETERNALFORGE_CONFIG_DIR"
DEFAULT_TOKEN_NAME = "google-token.json"


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


def candidate_token_paths(root: Path | None = None) -> list[Path]:
    """Ordered paths that may hold a Google OAuth token. Never invent secrets."""
    paths: list[Path] = []
    env_path = (os.environ.get(TOKEN_ENV_PATH) or "").strip()
    if env_path:
        paths.append(Path(env_path).expanduser())
    env_dir = (os.environ.get(TOKEN_ENV_DIR) or "").strip()
    if env_dir:
        paths.append(Path(env_dir).expanduser() / DEFAULT_TOKEN_NAME)
    if root is not None:
        paths.append(Path(root) / ".secrets" / DEFAULT_TOKEN_NAME)
    home = Path.home()
    paths.append(home / ".config" / "eternalforge" / DEFAULT_TOKEN_NAME)
    seen: set[str] = set()
    unique: list[Path] = []
    for path in paths:
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        unique.append(path)
    return unique


def find_google_token(root: Path | None = None) -> Path | None:
    """Return the first existing non-empty token file, or None."""
    for path in candidate_token_paths(root):
        try:
            if path.is_file() and path.stat().st_size > 0:
                return path
        except OSError:
            continue
    return None


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
    """Discover a local token path; listing stays empty until a client is wired."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = Path(root) if root is not None else None
        self.token_path = find_google_token(self.root)

    def creds_status(self) -> InboxCredsStatus:
        present = self.token_path is not None
        return InboxCredsStatus(
            token_present=present,
            path=str(self.token_path) if self.token_path else "",
            listing="stub-empty",
            adapter="live",
        )

    def list_items(
        self,
        source: str | None = None,
        query: str | None = None,
        limit: int = 10,
    ) -> list[InboxItem]:
        # Read-only listing is not implemented: never call Google APIs here.
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
    """Count journal rows whose kind is inbox (missing journal → 0)."""
    log = journal or Journal(root / "memory" / "journal.jsonl")
    return sum(1 for entry in log.load() if normalize_kind(entry.kind) == "inbox")
