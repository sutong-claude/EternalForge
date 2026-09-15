from datetime import date
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.memory import Journal, MemoryEntry
from tools.report import (
    count_reports,
    parse_research_query,
    render_report,
    research_entries,
    write_report,
)


def _seed(journal: Journal) -> None:
    journal.append(
        MemoryEntry(
            timestamp="2026-09-10T12:00:00Z",
            kind="research",
            summary="Research 'agents': 1 hit(s)",
            details="1. Software agent [fixture]\n   https://example.com/agent",
        )
    )
    journal.append(
        MemoryEntry(
            timestamp="2026-09-12T08:00:00Z",
            kind="capture",
            summary="Captured 1 topic(s) into 2026-09-12.md",
            details="",
        )
    )
    journal.append(
        MemoryEntry(
            timestamp="2026-09-14T18:00:00Z",
            kind="research",
            summary="Research 'agents': 2 hit(s)",
            details="1. Multi-agent systems [wikipedia]",
        )
    )
    journal.append(
        MemoryEntry(
            timestamp="2026-09-14T19:00:00Z",
            kind="research",
            summary="Research 'memory': 0 hit(s)",
            details="(no results)",
        )
    )


def test_parse_research_query() -> None:
    assert parse_research_query("Research 'agents': 2 hit(s)") == "agents"
    assert parse_research_query('Research "memory": 0 hit(s)') == "memory"
    assert parse_research_query("") == "(untitled)"
    assert parse_research_query("odd summary") == "odd summary"


def test_research_entries_filters_kind_and_window(tmp_path: Path) -> None:
    journal = Journal(tmp_path / "journal.jsonl")
    _seed(journal)
    all_research = research_entries(journal)
    assert len(all_research) == 3
    windowed = research_entries(
        journal, since=date(2026, 9, 12), until=date(2026, 9, 14)
    )
    assert [e.summary for e in windowed] == [
        "Research 'agents': 2 hit(s)",
        "Research 'memory': 0 hit(s)",
    ]
    limited = research_entries(journal, max_entries=1)
    assert len(limited) == 1
    assert "memory" in limited[0].summary


def test_render_report_groups_by_query() -> None:
    entries = [
        MemoryEntry("2026-09-10T12:00:00Z", "research", "Research 'agents': 1 hit(s)", "hit-a"),
        MemoryEntry("2026-09-14T18:00:00Z", "research", "Research 'agents': 2 hit(s)", "hit-b"),
        MemoryEntry("2026-09-14T19:00:00Z", "research", "Research 'memory': 0 hit(s)", "(no results)"),
    ]
    text = render_report("2026-09-15", entries)
    assert "# Research report — 2026-09-15" in text
    assert text.count("## agents") == 1
    assert "## memory" in text
    assert "3 research run(s) across 2 query(ies)" in text
    assert "hit-a" in text


def test_render_report_empty() -> None:
    text = render_report("2026-01-01", [])
    assert "(no research entries)" in text


def test_write_report_persists_markdown_and_journal(tmp_path: Path) -> None:
    journal = Journal(tmp_path / "memory" / "journal.jsonl")
    _seed(journal)
    result = write_report(
        tmp_path,
        journal=journal,
        day="2026-09-15",
        since=date(2026, 9, 10),
        until=date(2026, 9, 14),
    )
    assert result.path == tmp_path / "memory" / "reports" / "2026-09-15.md"
    assert result.path.exists()
    text = result.path.read_text(encoding="utf-8")
    assert "Window: 2026-09-10 → 2026-09-14" in text
    assert result.entry_count == 3
    assert result.query_count == 2
    assert "agents" in result.queries
    row = json.loads(journal.path.read_text(encoding="utf-8").splitlines()[-1])
    assert row["kind"] == "report"
    assert "2026-09-15.md" in row["summary"]
    assert count_reports(tmp_path) == 1


def test_count_reports_missing_dir_is_zero(tmp_path: Path) -> None:
    assert count_reports(tmp_path) == 0


def test_count_reports_counts_markdown_only(tmp_path: Path) -> None:
    folder = tmp_path / "memory" / "reports"
    folder.mkdir(parents=True)
    (folder / "2026-09-14.md").write_text("# a\n", encoding="utf-8")
    (folder / "2026-09-15.md").write_text("# b\n", encoding="utf-8")
    (folder / "notes.txt").write_text("ignore\n", encoding="utf-8")
    (folder / "nested").mkdir()
    assert count_reports(tmp_path) == 2


def test_invalid_day_raises(tmp_path: Path) -> None:
    try:
        write_report(tmp_path, day="not-a-date")
    except ValueError as exc:
        assert "YYYY-MM-DD" in str(exc)
    else:
        raise AssertionError("expected ValueError")
