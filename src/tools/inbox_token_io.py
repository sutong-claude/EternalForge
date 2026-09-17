"""Token file discovery and parse. Never log values."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import os

from tools.inbox_const import (
    DEFAULT_TOKEN_NAME,
    EXPIRY_SKEW,
    TOKEN_ENV_DIR,
    TOKEN_ENV_PATH,
)


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
