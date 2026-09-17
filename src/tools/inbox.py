"""Gmail / Drive listing sketch (read-only) with optional capture-to-journal.

Tests and CLI --offline use FixtureInboxAdapter so nothing hits the network.
LiveInboxAdapter discovers a token path from env or local files, never logs
token contents, and lists via an injectable GoogleApiClient. The default
HttpGoogleClient is read-only (Gmail metadata + Drive file list) and swallows
network errors so a missing or unusable token still yields an empty list.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import os

from core.memory import Journal, MemoryEntry, normalize_kind, normalize_tags


TOKEN_ENV_PATH = "ETERNALFORGE_GOOGLE_TOKEN_PATH"
TOKEN_ENV_DIR = "ETERNALFORGE_CONFIG_DIR"
DEFAULT_TOKEN_NAME = "google-token.json"
GMAIL_LIST_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
GMAIL_GET_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/{id}"
DRIVE_LIST_URL = "https://www.googleapis.com/drive/v3/files"
HTTP_TIMEOUT = 8


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


def load_access_token(path: Path) -> str | None:
    """Read access_token or token from a Google OAuth JSON file. Never log the value."""
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError):
        return None
    if not isinstance(data, dict):
        return None
    for key in ("access_token", "token"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _header_value(headers: dict[str, str], name: str) -> str:
    wanted = name.lower()
    for key, value in headers.items():
        if key.lower() == wanted:
            return str(value)
    return ""


def _gmail_subject(payload: dict) -> str:
    headers = payload.get("payload") if isinstance(payload.get("payload"), dict) else payload
    raw_headers = headers.get("headers") if isinstance(headers, dict) else None
    if isinstance(raw_headers, list):
        for item in raw_headers:
            if isinstance(item, dict) and str(item.get("name", "")).lower() == "subject":
                return str(item.get("value") or "").strip()
    return ""


class HttpGoogleClient:
    """Read-only Gmail + Drive list using a bearer access token."""

    def __init__(self, opener=None) -> None:
        self._opener = opener

    def _get_json(self, url: str, token: str) -> dict:
        request = Request(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
        opener = self._opener or urlopen
        with opener(request, timeout=HTTP_TIMEOUT) as response:
            body = response.read()
        data = json.loads(body.decode("utf-8"))
        return data if isinstance(data, dict) else {}

    def list_items(
        self,
        token_path: Path,
        source: str | None = None,
        query: str | None = None,
        limit: int = 10,
    ) -> list[InboxItem]:
        token = load_access_token(token_path)
        if not token:
            return []
        cap = max(0, int(limit))
        if cap == 0:
            return []
        wanted = (source or "all").strip().lower() or "all"
        items: list[InboxItem] = []
        try:
            if wanted in {"all", "*", "gmail", "mail"}:
                items.extend(self._list_gmail(token, query=query, limit=cap))
            if wanted in {"all", "*", "drive"}:
                remain = cap - len(items) if wanted in {"all", "*"} else cap
                if remain > 0:
                    items.extend(self._list_drive(token, query=query, limit=remain))
        except (OSError, URLError, HTTPError, json.JSONDecodeError, TimeoutError, ValueError):
            return []
        matched = [item for item in items if item.matches(query=query, source=source)]
        return matched[:cap]

    def _list_gmail(self, token: str, query: str | None, limit: int) -> list[InboxItem]:
        params = {"maxResults": max(1, limit)}
        if query and query.strip():
            params["q"] = query.strip()
        listing = self._get_json(f"{GMAIL_LIST_URL}?{urlencode(params)}", token)
        messages = listing.get("messages") if isinstance(listing.get("messages"), list) else []
        items: list[InboxItem] = []
        for row in messages[:limit]:
            if not isinstance(row, dict):
                continue
            msg_id = str(row.get("id") or "").strip()
            if not msg_id:
                continue
            detail: dict = {}
            try:
                get_url = GMAIL_GET_URL.format(id=msg_id) + "?" + urlencode(
                    {"format": "metadata", "metadataHeaders": "Subject"}
                )
                detail = self._get_json(get_url, token)
            except (OSError, URLError, HTTPError, json.JSONDecodeError, TimeoutError, ValueError):
                detail = {}
            title = _gmail_subject(detail) or msg_id
            snippet = str(detail.get("snippet") or "").strip()
            when = str(detail.get("internalDate") or "").strip()
            items.append(
                InboxItem(
                    source="gmail",
                    item_id=msg_id,
                    title=title,
                    snippet=snippet,
                    url=f"https://mail.google.com/mail/u/0/#inbox/{msg_id}",
                    when=when,
                )
            )
        return items

    def _list_drive(self, token: str, query: str | None, limit: int) -> list[InboxItem]:
        params = {
            "pageSize": max(1, limit),
            "fields": "files(id,name,modifiedTime,webViewLink,mimeType)",
            "orderBy": "modifiedTime desc",
        }
        if query and query.strip():
            safe = query.strip().replace("'", " ")
            params["q"] = f"name contains '{safe}' and trashed = false"
        listing = self._get_json(f"{DRIVE_LIST_URL}?{urlencode(params)}", token)
        files = listing.get("files") if isinstance(listing.get("files"), list) else []
        items: list[InboxItem] = []
        for row in files[:limit]:
            if not isinstance(row, dict):
                continue
            file_id = str(row.get("id") or "").strip()
            if not file_id:
                continue
            title = str(row.get("name") or file_id).strip()
            mime = str(row.get("mimeType") or "").strip()
            items.append(
                InboxItem(
                    source="drive",
                    item_id=file_id,
                    title=title,
                    snippet=mime,
                    url=str(row.get("webViewLink") or f"https://drive.google.com/file/d/{file_id}/view"),
                    when=str(row.get("modifiedTime") or "").strip(),
                )
            )
        return items


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
        listing = "google-api" if present else "no-token"
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
    """Count journal rows whose kind is inbox (missing journal → 0)."""
    log = journal or Journal(root / "memory" / "journal.jsonl")
    return sum(1 for entry in log.load() if normalize_kind(entry.kind) == "inbox")
