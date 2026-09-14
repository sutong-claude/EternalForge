from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.capture import capture, render_digest
from tools.research import FixtureAdapter, Hit


def test_capture_writes_markdown_and_journal(tmp_path: Path) -> None:
    catalog = {
        "agents": [
            Hit(
                title="Software agent",
                url="https://example.com/agent",
                snippet="A program that acts on behalf of a user.",
                source="fixture",
            )
        ]
    }
    result = capture(
        tmp_path,
        topics=["agents"],
        adapter=FixtureAdapter(catalog),
        day="2026-09-14",
        max_results=2,
    )
    assert result.path.exists()
    text = result.path.read_text(encoding="utf-8")
    assert "# Knowledge capture — 2026-09-14" in text
    assert "Software agent" in text
    assert "https://example.com/agent" in text
    journal = tmp_path / "memory" / "journal.jsonl"
    assert journal.exists()
    row = json.loads(journal.read_text(encoding="utf-8").splitlines()[-1])
    assert row["kind"] == "capture"
    assert "2026-09-14.md" in row["summary"]


def test_capture_appends_same_day(tmp_path: Path) -> None:
    adapter = FixtureAdapter()
    capture(tmp_path, topics=["eternalforge"], adapter=adapter, day="2026-09-14")
    capture(tmp_path, topics=["eternalforge"], adapter=adapter, day="2026-09-14")
    text = (tmp_path / "memory" / "2026-09-14.md").read_text(encoding="utf-8")
    assert text.count("# Knowledge capture") == 2


def test_invalid_day_raises() -> None:
    try:
        capture(Path("/tmp"), topics=["x"], adapter=FixtureAdapter(), day="not-a-date")
    except ValueError as exc:
        assert "YYYY-MM-DD" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_render_digest_empty() -> None:
    out = render_digest("2026-01-01", {})
    assert "(no topics)" in out
