"""Refresh grant helpers. Env client credentials win and are not persisted."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import os

from tools.inbox_const import CLIENT_ID_ENV, CLIENT_SECRET_ENV, HTTP_TIMEOUT, TOKEN_REFRESH_URL
from tools.inbox_token_io import _field, access_token_expired, load_token_payload


def env_client_id() -> str:
    return (os.environ.get(CLIENT_ID_ENV) or "").strip()


def env_client_secret() -> str:
    return (os.environ.get(CLIENT_SECRET_ENV) or "").strip()


def refresh_client_fields(data: dict) -> tuple[str, str, str]:
    """refresh_token, client_id, client_secret. Env wins over file. Empty if missing."""
    refresh = _field(data, "refresh_token")
    client_id = env_client_id() or _field(data, "client_id")
    client_secret = env_client_secret() or _field(data, "client_secret")
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
    if env_client_id():
        updated.pop("client_id", None)
    if env_client_secret():
        updated.pop("client_secret", None)
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
