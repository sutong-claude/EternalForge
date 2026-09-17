"""Gmail / Drive listing sketch (read-only) with optional capture-to-journal.

Tests and CLI --offline use FixtureInboxAdapter so nothing hits the network.
LiveInboxAdapter discovers a token path from env or local files, never logs
token contents, and lists via an injectable GoogleApiClient. The default
HttpGoogleClient is read-only (Gmail metadata + Drive file list) and swallows
network errors so a missing or unusable token still yields an empty list.
Expired access tokens are refreshed with the OAuth refresh_token grant when
refresh_token + client_id are available (file or env). Secrets stay off logs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
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
CLIENT_ID_ENV = "ETERNALFORGE_GOOGLE_CLIENT_ID"
CLIENT_SECRET_ENV = "ETERNALFORGE_GOOGLE_CLIENT_SECRET"
DEFAULT_TOKEN_NAME = "google-token.json"
GMAIL_LIST_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
GMAIL_GET_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/{id}"
DRIVE_LIST_URL = "https://www.googleapis.com/drive/v3/files"
TOKEN_REFRESH_URL = "https://oauth2.googleapis.com/token"
HTTP_TIMEOUT = 8
EXPIRY_SKEW = timedelta(seconds=60)


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


def load_token_payload(path: Path) -> dict | None:
    """Parse OAuth JSON. Never log values."""
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError):
        return None
    return data if isinstance(data, dict) else None


def _field(data: dict, *keys: str) -> str:
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def load_access_token(path: Path) -> str | None:
    """Read access_token or token from a Google OAuth JSON file. Never log the value."""
    data = load_token_payload(path)
    if data is None:
        return None
    value = _field(data, "access_token", "token")
    return value or None


def token_expiry(data: dict) -> datetime | None:
    """Best-effort expiry from common Google token JSON keys."""
    raw = data.get("expiry") or data.get("token_expiry") or data.get("expires_at")
    if isinstance(raw, (int, float)):
        try:
            return datetime.fromtimestamp(float(raw), tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None
    if isinstance(raw, str) and raw.strip():
        text = raw.strip().replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    return None


def access_token_expired(data: dict, now: datetime | None = None) -> bool:
    """True when expiry is known and already passed (with a small skew)."""
    expiry = token_expiry(data)
    if expiry is None:
        return False
    stamp = now or datetime.now(timezone.utc)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return stamp + EXPIRY_SKEW >= expiry


def refresh_client_fields(data: dict) -> tuple[str, str, str]:
    """refresh_token, client_id, client_secret from file or env. Empty strings if missing."""
    refresh = _field(data, "refresh_token")
    client_id = _field(data, "client_id") or (os.environ.get(CLIENT_ID_ENV) or "").strip()
    client_secret = _field(data, "client_secret") or (os.environ.get(CLIENT_SECRET_ENV) or "").strip()
    return refresh, client_id, client_secret


def can_refresh_token(data: dict) -> bool:
    refresh, client_id, _secret = refresh_client_fields(data)
    return bool(refresh and client_id)


def persist_access_token(path: Path, data: dict, access_token: str, expires_in: int | None) -> None:
    """Write the new access token back to the same file. Never log values."""
    updated = dict(data)
    updated["access_token"] = access_token
    if expires_in is not None and expires_in > 0:
        updated["expires_in"] = int(expires_in)
        expiry = datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))
        updated["expiry"] = expiry.strftime("%Y-%m-%dT%H:%M:%SZ")
    path.write_text(json.dumps(updated, indent=2) + "\n", encoding="utf-8")


def refresh_access_token(path: Path, opener=None, payload: dict | None = None) -> str | None:
    """POST refresh_token grant. Returns new access token or None. Does not log secrets."""
    data = payload if payload is not None else load_token_payload(path)
    if not data:
        return None
    refresh, client_id, client_secret = refresh_client_fields(data)
    if not refresh or not client_id:
        return None
    body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh,
        "client_id": client_id,
    }
    if client_secret:
        body["client_secret"] = client_secret
    request = Request(
        TOKEN_REFRESH_URL,
        data=urlencode(body).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
        method="POST",
    )
    fetch = opener or urlopen
    try:
        with fetch(request, timeout=HTTP_TIMEOUT) as response:
            raw = response.read()
        parsed = json.loads(raw.decode("utf-8"))
    except (OSError, URLError, HTTPError, json.JSONDecodeError, TimeoutError, ValueError, TypeError):
        return None
    if not isinstance(parsed, dict):
        return None
    token = parsed.get("access_token")
    if not isinstance(token, str) or not token.strip():
        return None
    token = token.strip()
    expires_in = parsed.get("expires_in")
    seconds = int(expires_in) if isinstance(expires_in, (int, float)) else None
    new_refresh = parsed.get("refresh_token")
    if isinstance(new_refresh, str) and new_refresh.strip():
        data = dict(data)
        data["refresh_token"] = new_refresh.strip()
    try:
        persist_access_token(path, data, token, seconds)
    except OSError:
        pass
    return token


def resolve_access_token(path: Path, opener=None, now: datetime | None = None) -> str | None:
    """Return a usable access token, refreshing when expired or missing."""
    data = load_token_payload(path)
    if data is None:
        return None
    current = _field(data, "access_token", "token")
    if current and not access_token_expired(data, now=now):
        return current
    refreshed = refresh_access_token(path, opener=opener, payload=data)
    if refreshed:
        return refreshed
    return current or None


def listing_status_for_payload(data: dict | None) -> str:
    if not data:
        return "no-token"
    current = _field(data, "access_token", "token")
    expired = access_token_expired(data)
    if current and not expired:
        return "google-api"
    if can_refresh_token(data):
        return "google-api"
    if current and expired:
        return "expired"
    return "expired" if data else "no-token"


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
        token = resolve_access_token(token_path, opener=self._opener)
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
    """Count journal rows whose kind is inbox (missing journal → 0)."""
    log = journal or Journal(root / "memory" / "journal.jsonl")
    return sum(1 for entry in log.load() if normalize_kind(entry.kind) == "inbox")
