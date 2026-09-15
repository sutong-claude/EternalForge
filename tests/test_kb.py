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
    extract_tags,
    format_index_hits,
    journal_extra_tags,
    merge_tags,
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
        "tags: agents, pkm\n\n"
        "Notes about autonomous software agents and personal knowledge. #agents\n",
        encoding="utf-8",
    )
    reports = memory / "reports"
    reports.mkdir()
    (reports / "2026-09-15.md").write_text(
        "# Research report \u2014 2026-09-15\n\n"
        "Compiled findings on transformer attention and retrieval. #transformers\n",
        encoding="utf-8",
    )
    journal = Journal(memory / "journal.jsonl")
    journal.append(
        MemoryEntry(
            timestamp="2026-09-10T12:00:00Z",
            kind="research",
            summary="agents paper #agents",
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


def test_extract_tags_hashtags_and_lines() -> None:
    text = "tags: Agents, PKM\nNotes #Agents and #pkm in the body."
    assert extract_tags(text) == ["agents", "pkm"]
    assert extract_tags("#Heading is not a tag because of the space") == []
    assert extract_tags("") == []


def test_merge_tags_dedupes_and_preserves_order() -> None:
    assert merge_tags(["Agents", "#pkm"], ["#agents", "notes", "PKM"]) == ["agents", "pkm", "notes"]
    assert merge_tags(None, [], [""]) == []
    assert journal_extra_tags("Agents, #pkm; agents") == ["agents", "pkm"]
    assert journal_extra_tags(["#Agents", "pkm", "Agents"]) == ["agents", "pkm"]
    assert journal_extra_tags(None) == []


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
    assert "report" in sources
    titles = [d.title for d in docs]
    assert any("Knowledge capture" in t for t in titles)
    md = next(d for d in docs if d.source == "markdown")
    assert md.kind == "markdown"
    assert md.timestamp == "2026-09-14"
    assert md.doc_id.startswith("md:")
    assert "agents" in md.tags
    assert "pkm" in md.tags


def test_collect_indexes_reports_subdir(tmp_path: Path) -> None:
    docs = collect_documents(_seed(tmp_path))
    reports = [d for d in docs if d.source == "report"]
    assert len(reports) == 1
    doc = reports[0]
    assert doc.kind == "report"
    assert doc.path == "memory/reports/2026-09-15.md"
    assert doc.doc_id == "md:memory/reports/2026-09-15.md"
    assert doc.timestamp == "2026-09-15"
    assert "transformer" in doc.text.lower()
    assert "transformers" in doc.tags


def test_journal_tags_merge_dedupes_extra_and_extracted(tmp_path: Path) -> None:
    memory = tmp_path / "memory"
    memory.mkdir()
    (memory / "journal.jsonl").write_text(
        json.dumps(
            {
                "timestamp": "2026-09-15T07:00:00Z",
                "kind": "research",
                "summary": "overlap paper #Agents #notes",
                "details": "body mentions #pkm",
                "tags": ["Agents", "#pkm", "extra"],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    docs = collect_documents(tmp_path)
    journal = next(d for d in docs if d.source == "journal")
    assert journal.tags == ["agents", "notes", "pkm", "extra"]
    assert len(journal.tags) == len(set(journal.tags))


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
    report = search_kb(root, "transformer retrieval", kind="report")
    assert report
    assert all(h.kind.lower() == "report" for h in report)
    assert all("reports/" in h.path for h in report)
    missing = search_kb(root, "knowledge", kind="cycle")
    assert missing == []


def test_search_filters_by_source(tmp_path: Path) -> None:
    root = _seed(tmp_path)
    journal = search_kb(root, "agents", source="journal")
    assert journal
    assert all(h.source == "journal" for h in journal)
    markdown = search_kb(root, "agents", source="MARKDOWN")
    assert markdown
    assert all(h.source == "markdown" for h in markdown)
    report = search_kb(root, "transformer", source="report")
    assert report
    assert all(h.source == "report" for h in report)
    missing = search_kb(root, "agents", source="email")
    assert missing == []


def test_search_filters_by_tag(tmp_path: Path) -> None:
    root = _seed(tmp_path)
    tagged = search_kb(root, "agents", tag="agents")
    assert tagged
    assert all("agents" in h.tags for h in tagged)
    hashed = search_kb(root, "transformer", tag="#Transformers")
    assert hashed
    assert all("transformers" in h.tags for h in hashed)
    missing = search_kb(root, "agents", tag="nonexistent")
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
    tagged = Document(
        "y", "journal", "memory/journal.jsonl", "t", "alpha", kind="research", tags=["agents"]
    )
    assert document_matches(tagged, source="journal", tag="#Agents")
    assert not document_matches(tagged, source="markdown")
    assert not document_matches(tagged, tag="pkm")


def test_empty_query_and_missing_memory(tmp_path: Path) -> None:
    assert search_kb(tmp_path, "") == []
    assert search_kb(tmp_path, "anything") == []
    assert format_index_hits([]) == "(no matches)"


def test_format_includes_source_and_tags() -> None:
    from tools.kb import IndexHit

    text = format_index_hits(
        [
            IndexHit(
                "md:memory/note.md",
                "markdown",
                "memory/note.md",
                "Note",
                3,
                "snippet",
                kind="markdown",
                tags=["agents"],
            )
        ]
    )
    assert "#agents" in text
    assert "Note" in text


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
    assert any(doc.get("tags") for doc in data["documents"])


def test_max_results_limit(tmp_path: Path) -> None:
    memory = tmp_path / "memory"
    memory.mkdir()
    for i in range(5):
        (memory / f"note-{i}.md").write_text(f"# note {i}\nshared token alpha\n", encoding="utf-8")
    hits = search_index(build_index(root=tmp_path), "alpha", max_results=2)
    assert len(hits) == 2


def test_missing_reports_dir_is_fine(tmp_path: Path) -> None:
    memory = tmp_path / "memory"
    memory.mkdir()
    (memory / "2026-09-14.md").write_text("# note\nalpha token\n", encoding="utf-8")
    docs = collect_documents(tmp_path)
    assert all(d.source != "report" for d in docs)
    assert search_kb(tmp_path, "alpha")
