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
