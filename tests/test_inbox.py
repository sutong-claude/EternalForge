from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import parse_qs
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.memory import Journal, MemoryEntry
from interfaces.cli import build_parser, main
from tools.inbox import (
    FixtureInboxAdapter,
    HttpGoogleClient,
    InboxItem,
    LiveInboxAdapter,
    access_token_expired,
    capture_inbox,
    count_inbox_entries,
    find_google_token,
    format_items,
    get_inbox_adapter,
    list_inbox,
    load_access_token,
    refresh_access_token,
    resolve_access_token,
)


class FakeGoogleClient:
    def __init__(self, items: list[InboxItem] | None = None) -> None:
        self.items = list(items) if items is not None else []
        self.calls: list[tuple] = []

    def list_items(self, token_path, source=None, query=None, limit=10):
        self.calls.append((token_path, source, query, limit))
        matched = [item for item in self.items if item.matches(query=query, source=source)]
        return matched[: max(0, int(limit))]


def test_list_filters_source_and_query() -> None:
    items = list_inbox(source="gmail", query="research", limit=5)
    assert len(items) == 1
    assert items[0].item_id == "m001"
    drive = list_inbox(source="drive")
    assert len(drive) == 1
    assert drive[0].source == "drive"


def test_format_empty() -> None:
    assert format_items([]) == "(no inbox items)"


def test_live_adapter_is_empty_without_token() -> None:
    assert LiveInboxAdapter().list_items() == []
    assert isinstance(get_inbox_adapter("live"), LiveInboxAdapter)
    assert isinstance(get_inbox_adapter("fixture"), FixtureInboxAdapter)


def test_item_matches() -> None:
    item = InboxItem(source="gmail", item_id="x", title="Hello", snippet="world")
    assert item.matches(query="HELLO")
    assert not item.matches(source="drive")
    assert item.matches(source="all")


def test_capture_writes_journal(tmp_path: Path) -> None:
    result = capture_inbox(tmp_path, source="drive", limit=3)
    assert result.count == 1
    journal = tmp_path / "memory" / "journal.jsonl"
    row = json.loads(journal.read_text(encoding="utf-8").splitlines()[-1])
    assert row["kind"] == "inbox"
    assert "drive" in row["summary"]
    assert "inbox" in row["tags"]
    assert "EternalForge notes" in row["details"]


def test_count_inbox_entries(tmp_path: Path) -> None:
    assert count_inbox_entries(tmp_path) == 0
    capture_inbox(tmp_path, source="gmail", query="invoice")
    capture_inbox(tmp_path, source="drive")
    journal = Journal(tmp_path / "memory" / "journal.jsonl")
    journal.append(MemoryEntry.now("research", "not inbox"))
    assert count_inbox_entries(tmp_path) == 2
    assert count_inbox_entries(tmp_path, journal=journal) == 2


def test_cli_inbox_list_offline(capsys) -> None:
    ns = build_parser().parse_args(["inbox", "list", "--source", "gmail", "--offline"])
    assert ns.cmd == "inbox"
    assert ns.inbox_cmd == "list"
    rc = main(["inbox", "list", "--source", "gmail", "--offline", "--max", "2"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "m001" in out
    assert "gmail" in out


def test_cli_inbox_capture(tmp_path: Path, capsys) -> None:
    rc = main(
        [
            "--root",
            str(tmp_path),
            "inbox",
            "capture",
            "--source",
            "gmail",
            "--query",
            "invoice",
            "--offline",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "Captured 1" in out
    journal = tmp_path / "memory" / "journal.jsonl"
    row = json.loads(journal.read_text(encoding="utf-8").splitlines()[-1])
    assert row["kind"] == "inbox"
    assert "invoice" in row["details"].lower()


def test_find_google_token_absent(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("ETERNALFORGE_GOOGLE_TOKEN_PATH", raising=False)
    monkeypatch.delenv("ETERNALFORGE_CONFIG_DIR", raising=False)
    monkeypatch.setattr("tools.inbox.Path.home", lambda: tmp_path / "home")
    assert find_google_token(tmp_path) is None
    status = LiveInboxAdapter(root=tmp_path).creds_status()
    assert status.token_present is False
    assert status.listing == "no-token"
    assert "token=absent" in status.format()


def test_find_google_token_env_path(tmp_path, monkeypatch) -> None:
    token = tmp_path / "tok.json"
    token.write_text('{"token": "redacted"}', encoding="utf-8")
    monkeypatch.setenv("ETERNALFORGE_GOOGLE_TOKEN_PATH", str(token))
    found = find_google_token(tmp_path)
    assert found == token
    status = LiveInboxAdapter(root=tmp_path).creds_status()
    assert status.token_present is True
    assert status.path == str(token)
    assert status.listing == "google-api"
    assert load_access_token(token) == "redacted"


def test_live_list_uses_injected_client(tmp_path, monkeypatch) -> None:
    token = tmp_path / "tok.json"
    token.write_text('{"access_token": "secret-value"}', encoding="utf-8")
    monkeypatch.setenv("ETERNALFORGE_GOOGLE_TOKEN_PATH", str(token))
    fake = FakeGoogleClient(
        [
            InboxItem(source="gmail", item_id="gx", title="Hello from Gmail"),
            InboxItem(source="drive", item_id="dx", title="Notes doc"),
        ]
    )
    adapter = LiveInboxAdapter(root=tmp_path, client=fake)
    items = adapter.list_items(source="gmail", limit=5)
    assert [item.item_id for item in items] == ["gx"]
    assert fake.calls
    assert fake.calls[0][0] == token


def test_http_client_maps_gmail_and_drive(tmp_path) -> None:
    token = tmp_path / "tok.json"
    token.write_text('{"access_token": "abc"}', encoding="utf-8")

    class DummyResponse:
        def __init__(self, payload: dict) -> None:
            self._payload = json.dumps(payload).encode("utf-8")

        def read(self) -> bytes:
            return self._payload

        def __enter__(self):
            return self

        def __exit__(self, *args) -> None:
            return None

    def opener(request, timeout=0):
        url = request.full_url
        auth = request.get_header("Authorization")
        assert auth == "Bearer abc"
        if "gmail.googleapis.com" in url and "/messages/" in url and "format=" in url:
            return DummyResponse(
                {
                    "id": "m99",
                    "snippet": "body preview",
                    "payload": {"headers": [{"name": "Subject", "value": "Paper alert"}]},
                    "internalDate": "1710000000000",
                }
            )
        if "gmail.googleapis.com" in url:
            return DummyResponse({"messages": [{"id": "m99"}]})
        if "googleapis.com/drive" in url:
            return DummyResponse(
                {
                    "files": [
                        {
                            "id": "d99",
                            "name": "Outline.gdoc",
                            "modifiedTime": "2026-09-16T00:00:00Z",
                            "webViewLink": "https://drive.google.com/file/d/d99/view",
                            "mimeType": "application/vnd.google-apps.document",
                        }
                    ]
                }
            )
        raise AssertionError(url)

    client = HttpGoogleClient(opener=opener)
    items = client.list_items(token, source="all", limit=5)
    assert [item.item_id for item in items] == ["m99", "d99"]
    assert items[0].title == "Paper alert"
    assert items[1].title == "Outline.gdoc"


def test_find_google_token_secrets_dir(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("ETERNALFORGE_GOOGLE_TOKEN_PATH", raising=False)
    monkeypatch.delenv("ETERNALFORGE_CONFIG_DIR", raising=False)
    monkeypatch.setattr("tools.inbox.Path.home", lambda: tmp_path / "home")
    secrets = tmp_path / ".secrets"
    secrets.mkdir()
    token = secrets / "google-token.json"
    token.write_text("{}", encoding="utf-8")
    assert find_google_token(tmp_path) == token
    assert load_access_token(token) is None


def test_cli_inbox_status(tmp_path, capsys) -> None:
    rc = main(["--root", str(tmp_path), "inbox", "status"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "adapter=live" in out
    assert "token=absent" in out
    assert "listing=no-token" in out


def test_cli_inbox_live_list_empty(tmp_path, capsys) -> None:
    rc = main(["--root", str(tmp_path), "inbox", "list", "--live"])
    assert rc == 0
    assert capsys.readouterr().out.strip() == "(no inbox items)"


def test_access_token_expired_from_iso() -> None:
    past = {"expiry": "2020-01-01T00:00:00Z", "access_token": "old"}
    future = {"expiry": "2099-01-01T00:00:00Z", "access_token": "fresh"}
    now = datetime(2026, 9, 17, tzinfo=timezone.utc)
    assert access_token_expired(past, now=now) is True
    assert access_token_expired(future, now=now) is False
    assert access_token_expired({"access_token": "no-expiry"}, now=now) is False


def test_refresh_access_token_updates_file(tmp_path, monkeypatch) -> None:
    token = tmp_path / "tok.json"
    token.write_text(
        json.dumps(
            {
                "access_token": "old",
                "refresh_token": "rt-1",
                "client_id": "cid",
                "client_secret": "csec",
                "expiry": "2020-01-01T00:00:00Z",
            }
        ),
        encoding="utf-8",
    )

    class DummyResponse:
        def read(self) -> bytes:
            return json.dumps({"access_token": "new-token", "expires_in": 3600}).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args) -> None:
            return None

    def opener(request, timeout=0):
        assert request.full_url == "https://oauth2.googleapis.com/token"
        body = parse_qs(request.data.decode("utf-8"))
        assert body["grant_type"] == ["refresh_token"]
        assert body["refresh_token"] == ["rt-1"]
        assert body["client_id"] == ["cid"]
        return DummyResponse()

    got = refresh_access_token(token, opener=opener)
    assert got == "new-token"
    saved = json.loads(token.read_text(encoding="utf-8"))
    assert saved["access_token"] == "new-token"
    assert saved["refresh_token"] == "rt-1"
    assert "expiry" in saved


def test_resolve_refreshes_when_expired(tmp_path) -> None:
    token = tmp_path / "tok.json"
    token.write_text(
        json.dumps(
            {
                "access_token": "stale",
                "refresh_token": "rt-2",
                "client_id": "cid",
                "expiry": "2020-01-01T00:00:00Z",
            }
        ),
        encoding="utf-8",
    )

    class DummyResponse:
        def read(self) -> bytes:
            return json.dumps({"access_token": "rotated"}).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args) -> None:
            return None

    def opener(request, timeout=0):
        return DummyResponse()

    assert resolve_access_token(token, opener=opener) == "rotated"


def test_status_expired_without_refresh(tmp_path, monkeypatch) -> None:
    token = tmp_path / "tok.json"
    token.write_text(
        json.dumps({"access_token": "stale", "expiry": "2020-01-01T00:00:00Z"}),
        encoding="utf-8",
    )
    monkeypatch.setenv("ETERNALFORGE_GOOGLE_TOKEN_PATH", str(token))
    status = LiveInboxAdapter(root=tmp_path).creds_status()
    assert status.token_present is True
    assert status.listing == "expired"


def test_refresh_uses_env_client_id_and_strips_file(tmp_path, monkeypatch) -> None:
    token = tmp_path / "tok.json"
    token.write_text(
        json.dumps(
            {
                "access_token": "old",
                "refresh_token": "rt-env",
                "client_id": "file-cid",
                "client_secret": "file-sec",
                "expiry": "2020-01-01T00:00:00Z",
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("ETERNALFORGE_GOOGLE_CLIENT_ID", "env-cid")
    monkeypatch.setenv("ETERNALFORGE_GOOGLE_CLIENT_SECRET", "env-sec")

    class DummyResponse:
        def read(self) -> bytes:
            return json.dumps({"access_token": "env-token", "expires_in": 3600}).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args) -> None:
            return None

    def opener(request, timeout=0):
        body = parse_qs(request.data.decode("utf-8"))
        assert body["client_id"] == ["env-cid"]
        assert body["client_secret"] == ["env-sec"]
        return DummyResponse()

    got = refresh_access_token(token, opener=opener)
    assert got == "env-token"
    saved = json.loads(token.read_text(encoding="utf-8"))
    assert saved["access_token"] == "env-token"
    assert saved["refresh_token"] == "rt-env"
    assert "client_id" not in saved
    assert "client_secret" not in saved


def test_status_google_api_with_env_client_id(tmp_path, monkeypatch) -> None:
    token = tmp_path / "tok.json"
    token.write_text(
        json.dumps(
            {
                "access_token": "stale",
                "refresh_token": "rt-3",
                "expiry": "2020-01-01T00:00:00Z",
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("ETERNALFORGE_GOOGLE_TOKEN_PATH", str(token))
    monkeypatch.setenv("ETERNALFORGE_GOOGLE_CLIENT_ID", "env-only")
    status = LiveInboxAdapter(root=tmp_path).creds_status()
    assert status.listing == "google-api"
