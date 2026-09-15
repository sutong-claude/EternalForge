from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.memory import Journal, MemoryEntry, entry_has_tag, normalize_tags


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


def test_recent_filters_by_kind(tmp_path: Path) -> None:
    path = tmp_path / "journal.jsonl"
    journal = Journal(path)
    journal.append(MemoryEntry("t1", "cycle", "one"))
    journal.append(MemoryEntry("t2", "Research", "wiki"))
    journal.append(MemoryEntry("t3", "capture", "notes"))
    journal.append(MemoryEntry("t4", "research", "books"))
    hits = journal.recent(10, kind="RESEARCH")
    assert [h.summary for h in hits] == ["wiki", "books"]
    assert journal.recent_kinds(8, kind="research") == ["Research", "research"]
    assert journal.format_recent_kinds(kind="missing") == "-"


def test_format_recent_dump(tmp_path: Path) -> None:
    path = tmp_path / "journal.jsonl"
    journal = Journal(path)
    assert "no journal entries" in journal.format_recent(kind="cycle")
    journal.append(MemoryEntry("t1", "cycle", "did work", "ok"))
    text = journal.format_recent(kind="cycle")
    assert "t1\tcycle\tdid work" in text
    assert "\tok" in text


def test_normalize_tags_dedupes_and_strips() -> None:
    assert normalize_tags(["#Research", "research", "  Agents ", ""]) == ["research", "agents"]
    assert normalize_tags("Alpha, #beta; ALPHA") == ["alpha", "beta"]
    assert normalize_tags(None) == []


def test_journal_persists_tags(tmp_path: Path) -> None:
    path = tmp_path / "journal.jsonl"
    journal = Journal(path)
    journal.append(MemoryEntry.now("research", "wiki", "ok", tags=["#Research", "wiki", "research"]))
    row = json.loads(path.read_text(encoding="utf-8").splitlines()[-1])
    assert row["tags"] == ["research", "wiki"]
    loaded = journal.load()[-1]
    assert loaded.tags == ["research", "wiki"]
    text = journal.format_recent()
    assert "#research,#wiki" in text


def test_journal_loads_legacy_rows_without_tags(tmp_path: Path) -> None:
    path = tmp_path / "journal.jsonl"
    path.write_text(
        '{"timestamp": "t", "kind": "cycle", "summary": "old", "details": ""}\n',
        encoding="utf-8",
    )
    entry = Journal(path).load()[0]
    assert entry.tags == []
    assert entry.summary == "old"


def test_recent_filters_by_tag(tmp_path: Path) -> None:
    path = tmp_path / "journal.jsonl"
    journal = Journal(path)
    journal.append(MemoryEntry("t1", "research", "wiki", tags=["#Research", "wiki"]))
    journal.append(MemoryEntry("t2", "capture", "notes", tags=["daily"]))
    journal.append(MemoryEntry("t3", "research", "arxiv", tags=["research", "arxiv"]))
    journal.append(MemoryEntry("t4", "cycle", "done"))
    hits = journal.recent(10, tag="RESEARCH")
    assert [h.summary for h in hits] == ["wiki", "arxiv"]
    hashed = journal.recent(10, tag="#Wiki")
    assert [h.summary for h in hashed] == ["wiki"]
    combo = journal.recent(10, kind="research", tag="arxiv")
    assert [h.summary for h in combo] == ["arxiv"]
    assert journal.format_recent_kinds(tag="missing") == "-"
    empty = journal.format_recent(tag="nope")
    assert "tag=nope" in empty
    assert entry_has_tag(hits[0], "#research")
    assert not entry_has_tag(hits[0], "daily")
