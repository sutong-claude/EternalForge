from pathlib import Path
import json
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.memory import Journal, MemoryEntry
from tools.kb import (
    build_index,
    collect_documents,
    document_matches,
    extract_day,
    format_index_hits,
    parse_day,
    search_index,
    search_kb,
    tokenize,
    write_index,
)


def _seed(tmp_path: Path) -> Path:
    memory = tmp_path / "memory"
    memory.mkdir()
    (memory / "2026-09-14.md").write_text(
        "# Knowledge capture \u2014 2026-09-14\n\n"
        "Notes about autonomous software agents and personal knowledge.\n",
        encoding="utf-8",
    )
    journal = Journal(memory / "journal.jsonl")
    journal.append(
        MemoryEntry(
            timestamp="2026-09-10T12:00:00Z",
            kind="research",
            summary="agents paper",
            details="attention mechanism notes",
        )
    )
    journal.append(
        MemoryEntry(
            timestamp="2026-09-14T18:00:00Z",
            kind="capture",
            summary="daily digest",
            details="personal knowledge management",
        )
    )
    return tmp_path


def test_tokenize_lowercases() -> None:
    assert tokenize("Hello, Agents!") == ["hello", "agents"]


def test_extract_and_parse_day() -> None:
    assert extract_day("2026-09-14.md") == "2026-09-14"
    assert extract_day("2026-09-14T18:00:00Z") == "2026-09-14"
    assert extract_day("no-date") is None
    assert parse_day("") is None
    assert parse_day("2026-09-14") == "2026-09-14"
    with pytest.raises(ValueError):
        parse_day("not-a-date")


def test_collect_markdown_and_journal(tmp_path: Path) -> None:
    docs = collect_documents(_seed(tmp_path))
    sources = {d.source for d in docs}
    assert "markdown" in sources
    assert "journal" in sources
    titles = [d.title for d in docs]
    assert any("Knowledge capture" in t for t in titles)
    md = next(d for d in docs if d.source == "markdown")
    assert md.kind == "markdown"
    assert md.timestamp == "2026-09-14"


def test_search_ranks_matching_docs(tmp_path: Path) -> None:
    root = _seed(tmp_path)
    hits = search_kb(root, "agents knowledge")
    assert hits
    assert hits[0].score >= hits[-1].score
    blob = " ".join(h.title + h.snippet for h in hits).lower()
    assert "agent" in blob or "knowledge" in blob


def test_search_filters_by_kind(tmp_path: Path) -> None:
    root = _seed(tmp_path)
    research = search_kb(root, "agents knowledge", kind="research")
    assert research
    assert all(h.kind.lower() == "research" for h in research)
    capture = search_kb(root, "knowledge", kind="CAPTURE")
    assert capture
    assert all(h.kind.lower() == "capture" for h in capture)
    missing = search_kb(root, "knowledge", kind="cycle")
    assert missing == []


def test_search_filters_by_date_range(tmp_path: Path) -> None:
    root = _seed(tmp_path)
    early = search_kb(root, "agents", until="2026-09-12")
    assert early
    assert all(extract_day(h.timestamp) <= "2026-09-12" for h in early)
    late = search_kb(root, "knowledge", since="2026-09-13")
    assert late
    assert all(extract_day(h.timestamp) >= "2026-09-13" for h in late)
    window = search_kb(root, "knowledge", since="2026-09-14", until="2026-09-14")
    assert window
    assert all(extract_day(h.timestamp) == "2026-09-14" for h in window)
    none = search_kb(root, "knowledge", since="2026-01-01", until="2026-01-02")
    assert none == []


def test_document_matches_undated_excluded_when_ranged() -> None:
    from tools.kb import Document

    undated = Document("x", "markdown", "memory/note.md", "t", "alpha", kind="markdown", timestamp="")
    assert document_matches(undated, kind="markdown")
    assert not document_matches(undated, since="2026-09-01")


def test_empty_query_and_missing_memory(tmp_path: Path) -> None:
    assert search_kb(tmp_path, "") == []
    assert search_kb(tmp_path, "anything") == []
    assert format_index_hits([]) == "(no matches)"


def test_skips_bad_journal_lines(tmp_path: Path) -> None:
    memory = tmp_path / "memory"
    memory.mkdir()
    (memory / "journal.jsonl").write_text(
        "not-json\n"
        '{"kind": "research", "summary": "valid token zebra", "details": ""}\n',
        encoding="utf-8",
    )
    hits = search_kb(tmp_path, "zebra")
    assert len(hits) == 1
    assert hits[0].source == "journal"


def test_write_index_snapshot(tmp_path: Path) -> None:
    root = _seed(tmp_path)
    index = build_index(root=root)
    path = write_index(index, root)
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["document_count"] == index.document_count()
    assert data["token_count"] == len(index.postings)


def test_max_results_limit(tmp_path: Path) -> None:
    memory = tmp_path / "memory"
    memory.mkdir()
    for i in range(5):
        (memory / f"note-{i}.md").write_text(f"# note {i}\nshared token alpha\n", encoding="utf-8")
    hits = search_index(build_index(root=tmp_path), "alpha", max_results=2)
    assert len(hits) == 2
