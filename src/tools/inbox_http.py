"""Read-only Gmail + Drive HTTP client."""

from __future__ import annotations

from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

from tools.inbox_const import DRIVE_LIST_URL, GMAIL_GET_URL, GMAIL_LIST_URL, HTTP_TIMEOUT
from tools.inbox_item import InboxItem
from tools.inbox_token_refresh import resolve_access_token


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
