from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.memory import Journal, MemoryEntry
from interfaces.cli import build_parser, main
from tools.inbox import (
    FixtureInboxAdapter,
    InboxItem,
    LiveInboxAdapter,
    capture_inbox,
    count_inbox_entries,
    find_google_token,
    format_items,
    get_inbox_adapter,
    list_inbox,
)


def test_list_filters_source_and_query() -> None:
    items = list_inbox(source="gmail", query="research", limit=5)
    assert len(items) == 1
    assert items[0].item_id == "m001"
    drive = list_inbox(source="drive")
    assert len(drive) == 1
    assert drive[0].source == "drive"


def test_format_empty() -> None:
    assert format_items([]) == "(no inbox items)"


def test_live_adapter_is_empty() -> None:
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
    assert status.listing == "stub-empty"
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
    assert LiveInboxAdapter(root=tmp_path).list_items() == []


def test_find_google_token_secrets_dir(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("ETERNALFORGE_GOOGLE_TOKEN_PATH", raising=False)
    monkeypatch.delenv("ETERNALFORGE_CONFIG_DIR", raising=False)
    monkeypatch.setattr("tools.inbox.Path.home", lambda: tmp_path / "home")
    secrets = tmp_path / ".secrets"
    secrets.mkdir()
    token = secrets / "google-token.json"
    token.write_text("{}", encoding="utf-8")
    assert find_google_token(tmp_path) == token


def test_cli_inbox_status(tmp_path, capsys) -> None:
    rc = main(["--root", str(tmp_path), "inbox", "status"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "adapter=live" in out
    assert "token=absent" in out
    assert "listing=stub-empty" in out


def test_cli_inbox_live_list_empty(tmp_path, capsys) -> None:
    rc = main(["--root", str(tmp_path), "inbox", "list", "--live"])
    assert rc == 0
    assert capsys.readouterr().out.strip() == "(no inbox items)"
