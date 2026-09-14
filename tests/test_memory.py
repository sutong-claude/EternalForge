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
