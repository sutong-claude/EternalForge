from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.memory import Journal, MemoryEntry


def test_journal_append_and_read(tmp_path: Path) -> None:
    path = tmp_path / "memory" / "journal.jsonl"
    journal = Journal(path)
    journal.append(MemoryEntry.now("cycle", "first", "ok"))
    journal.append(MemoryEntry.now("cycle", "second", "ok"))
    recents = journal.recent(10)
    assert len(recents) == 2
    assert recents[-1].summary == "second"


def test_recent_kinds_order_and_limit(tmp_path: Path) -> None:
    path = tmp_path / "journal.jsonl"
    journal = Journal(path)
    journal.append(MemoryEntry.now("cycle", "a"))
    journal.append(MemoryEntry.now("capture", "b"))
    journal.append(MemoryEntry.now("research", "c"))
    assert journal.recent_kinds(2) == ["capture", "research"]
    assert journal.format_recent_kinds(8) == "cycle,capture,research"


def test_recent_kinds_empty_and_skips_junk(tmp_path: Path) -> None:
    path = tmp_path / "journal.jsonl"
    journal = Journal(path)
    assert journal.recent_kinds() == []
    assert journal.format_recent_kinds() == "-"
    path.write_text(
        "not-json\n"
        '{"timestamp": "t", "kind": "", "summary": "x"}\n'
        '{"timestamp": "t", "kind": "research", "summary": "ok"}\n',
        encoding="utf-8",
    )
    assert journal.recent_kinds() == ["research"]
