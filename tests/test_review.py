from datetime import date
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.memory import Journal, MemoryEntry
from interfaces.cli import build_parser, main
from tools.review import (
    classify_review_name,
    count_reviews,
    journal_in_window,
    list_review_files,
    normalize_period,
    render_digest,
    render_review,
    review_window,
    write_digest,
    write_review,
)
from tools.tasks import Task, save_tasks


def test_normalize_period_aliases() -> None:
    assert normalize_period("day") == "daily"
    assert normalize_period("w") == "weekly"
    try:
        normalize_period("monthly")
    except ValueError as exc:
        assert "period" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_review_window_daily_and_weekly() -> None:
    day = date(2026, 9, 16)
    assert review_window(day, "daily") == (day, day)
    assert review_window(day, "weekly") == (date(2026, 9, 10), day)


def test_journal_in_window(tmp_path: Path) -> None:
    journal = Journal(tmp_path / "journal.jsonl")
    journal.append(MemoryEntry("2026-09-10T12:00:00Z", "research", "old", ""))
    journal.append(MemoryEntry("2026-09-16T08:00:00Z", "task", "today", ""))
    journal.append(MemoryEntry("2026-09-17T08:00:00Z", "cycle", "tomorrow", ""))
    rows = journal_in_window(
        journal, since=date(2026, 9, 16), until=date(2026, 9, 16)
    )
    assert [e.summary for e in rows] == ["today"]


def test_render_review_empty() -> None:
    text = render_review(
        "2026-09-16",
        "daily",
        since=date(2026, 9, 16),
        until=date(2026, 9, 16),
        entries=[],
        open_tasks=[],
        overdue_tasks=[],
        due_soon_tasks=[],
        done_tasks=[],
    )
    assert "# Daily review — 2026-09-16" in text
    assert "(no journal entries)" in text
    assert "(no tasks)" in text


def test_write_review_persists_markdown_and_journal(tmp_path: Path) -> None:
    journal = Journal(tmp_path / "memory" / "journal.jsonl")
    journal.append(
        MemoryEntry(
            timestamp="2026-09-16T10:00:00Z",
            kind="research",
            summary="Research 'agents': 1 hit(s)",
            details="hit",
            tags=["agents"],
        )
    )
    save_tasks(
        tmp_path,
        [
            Task(
                id="T001",
                title="Ship review sketch",
                status="open",
                due="2026-09-10",
                priority="high",
                created="2026-09-01T00:00:00Z",
                updated="2026-09-01T00:00:00Z",
            ),
            Task(
                id="T002",
                title="Closed item",
                status="done",
                created="2026-09-14T00:00:00Z",
                updated="2026-09-16T12:00:00Z",
            ),
        ],
    )
    result = write_review(
        tmp_path,
        journal=journal,
        day="2026-09-16",
        period="daily",
        today=date(2026, 9, 16),
    )
    assert result.path == tmp_path / "memory" / "reviews" / "daily-2026-09-16.md"
    assert result.path.exists()
    text = result.path.read_text(encoding="utf-8")
    assert "Window: 2026-09-16 → 2026-09-16" in text
    assert "T001" in text
    assert "OVERDUE" in text
    assert "Closed item" in text
    assert result.journal_count == 1
    assert result.open_count == 1
    assert result.overdue_count == 1
    assert result.done_count == 1
    assert count_reviews(tmp_path) == 1
    row = json.loads(journal.path.read_text(encoding="utf-8").splitlines()[-1])
    assert row["kind"] == "review"
    assert "daily-2026-09-16.md" in row["summary"]


def test_write_review_weekly_window(tmp_path: Path) -> None:
    journal = Journal(tmp_path / "memory" / "journal.jsonl")
    journal.append(MemoryEntry("2026-09-11T00:00:00Z", "capture", "mid-week", ""))
    result = write_review(
        tmp_path,
        journal=journal,
        day="2026-09-16",
        period="weekly",
    )
    assert result.path.name == "weekly-2026-09-16.md"
    assert result.since == "2026-09-10"
    assert result.until == "2026-09-16"
    assert result.journal_count == 1
    assert "Window: 2026-09-10 → 2026-09-16" in result.markdown


def test_count_reviews_missing_dir_is_zero(tmp_path: Path) -> None:
    assert count_reviews(tmp_path) == 0


def test_classify_and_list_review_files(tmp_path: Path) -> None:
    assert classify_review_name("daily-2026-09-16.md") == ("daily", "2026-09-16")
    assert classify_review_name("weekly-2026-09-16.md") == ("weekly", "2026-09-16")
    assert classify_review_name("digest-2026-09-16.md") == ("digest", "2026-09-16")
    assert classify_review_name("notes.md") == ("other", "notes")
    folder = tmp_path / "memory" / "reviews"
    folder.mkdir(parents=True)
    (folder / "weekly-2026-09-16.md").write_text("# w\n", encoding="utf-8")
    (folder / "daily-2026-09-14.md").write_text("# d\n", encoding="utf-8")
    names = [p.name for p in list_review_files(tmp_path)]
    assert names == ["daily-2026-09-14.md", "weekly-2026-09-16.md"]
    assert list_review_files(tmp_path / "missing") == []


def test_render_digest_empty() -> None:
    text = render_digest("2026-09-16", [], review_count=0)
    assert "# Reviews digest — 2026-09-16" in text
    assert "Reviews=0" in text
    assert "(no review files)" in text


def test_write_digest_persists_markdown_and_journal(tmp_path: Path) -> None:
    folder = tmp_path / "memory" / "reviews"
    folder.mkdir(parents=True)
    (folder / "daily-2026-09-14.md").write_text("# d\n", encoding="utf-8")
    (folder / "weekly-2026-09-16.md").write_text("# w\n", encoding="utf-8")
    journal = Journal(tmp_path / "memory" / "journal.jsonl")
    result = write_digest(tmp_path, journal=journal, day="2026-09-16")
    assert result.path == folder / "digest-2026-09-16.md"
    assert result.path.exists()
    text = result.path.read_text(encoding="utf-8")
    assert "Reviews=3" in text
    assert "daily-2026-09-14.md" in text
    assert "digest-2026-09-16.md" in text
    assert result.review_count == 3
    assert result.daily_count == 1
    assert result.weekly_count == 1
    assert result.digest_count == 1
    assert count_reviews(tmp_path) == 3
    row = json.loads(journal.path.read_text(encoding="utf-8").splitlines()[-1])
    assert row["kind"] == "review"
    assert "digest-2026-09-16.md" in row["summary"]
    assert "digest" in row["tags"]


def test_cli_review_digest_flag(tmp_path: Path, capsys) -> None:
    ns = build_parser().parse_args(["review", "--digest", "--day", "2026-09-16"])
    assert ns.digest is True
    folder = tmp_path / "memory" / "reviews"
    folder.mkdir(parents=True)
    (folder / "daily-2026-09-14.md").write_text("# d\n", encoding="utf-8")
    rc = main(["--root", str(tmp_path), "review", "--digest", "--day", "2026-09-16"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "digest-2026-09-16.md" in out
    assert "Reviews=2" in out
    assert (folder / "digest-2026-09-16.md").exists()


def test_count_reviews_counts_markdown_only(tmp_path: Path) -> None:
    folder = tmp_path / "memory" / "reviews"
    folder.mkdir(parents=True)
    (folder / "daily-2026-09-14.md").write_text("# a\n", encoding="utf-8")
    (folder / "weekly-2026-09-16.md").write_text("# b\n", encoding="utf-8")
    (folder / "notes.txt").write_text("ignore\n", encoding="utf-8")
    (folder / "nested").mkdir()
    assert count_reviews(tmp_path) == 2
