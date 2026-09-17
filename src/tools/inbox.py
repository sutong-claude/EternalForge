"""Gmail / Drive listing sketch (read-only) with optional capture-to-journal.

Tests and CLI --offline use FixtureInboxAdapter so nothing hits the network.
LiveInboxAdapter discovers a token path from env or local files, never logs
token contents, and lists via an injectable GoogleApiClient. The default
HttpGoogleClient is read-only (Gmail metadata + Drive file list) and swallows
network errors so a missing or unusable token still yields an empty list.
Expired access tokens are refreshed with the OAuth refresh_token grant when
refresh_token + client_id are available (file or env). Env client_id/secret
win and are not written back to the token file. Secrets stay off logs.
"""

from __future__ import annotations

from tools.inbox_const import (
    CLIENT_ID_ENV,
    CLIENT_SECRET_ENV,
    DEFAULT_TOKEN_NAME,
    DRIVE_LIST_URL,
    EXPIRY_SKEW,
    GMAIL_GET_URL,
    GMAIL_LIST_URL,
    HTTP_TIMEOUT,
    TOKEN_ENV_DIR,
    TOKEN_ENV_PATH,
    TOKEN_REFRESH_URL,
)
from tools.inbox_http import HttpGoogleClient
from tools.inbox_item import (
    DEFAULT_FIXTURE,
    FixtureInboxAdapter,
    GoogleApiClient,
    InboxAdapter,
    InboxItem,
)
from tools.inbox_live import (
    InboxCaptureResult,
    InboxCredsStatus,
    LiveInboxAdapter,
    capture_inbox,
    count_inbox_entries,
    format_items,
    get_inbox_adapter,
    list_inbox,
)
from tools.inbox_token_io import (
    access_token_expired,
    candidate_token_paths,
    find_google_token,
    load_access_token,
    load_token_payload,
    token_expiry,
)
from tools.inbox_token_refresh import (
    can_refresh_token,
    env_client_id,
    env_client_secret,
    persist_access_token,
    refresh_access_token,
    refresh_client_fields,
    resolve_access_token,
)

__all__ = [
    "CLIENT_ID_ENV",
    "CLIENT_SECRET_ENV",
    "DEFAULT_FIXTURE",
    "DEFAULT_TOKEN_NAME",
    "DRIVE_LIST_URL",
    "EXPIRY_SKEW",
    "FixtureInboxAdapter",
    "GMAIL_GET_URL",
    "GMAIL_LIST_URL",
    "GoogleApiClient",
    "HTTP_TIMEOUT",
    "HttpGoogleClient",
    "InboxAdapter",
    "InboxCaptureResult",
    "InboxCredsStatus",
    "InboxItem",
    "LiveInboxAdapter",
    "TOKEN_ENV_DIR",
    "TOKEN_ENV_PATH",
    "TOKEN_REFRESH_URL",
    "access_token_expired",
    "can_refresh_token",
    "candidate_token_paths",
    "capture_inbox",
    "count_inbox_entries",
    "env_client_id",
    "env_client_secret",
    "find_google_token",
    "format_items",
    "get_inbox_adapter",
    "list_inbox",
    "load_access_token",
    "load_token_payload",
    "persist_access_token",
    "refresh_access_token",
    "refresh_client_fields",
    "resolve_access_token",
    "token_expiry",
]
