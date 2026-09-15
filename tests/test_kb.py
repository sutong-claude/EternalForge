from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.memory import Journal, MemoryEntry
from tools.kb import (
    build_index,
    collect_documents,
    format_index_hits,
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
    journal.append(MemoryEntry.now("research", "agents paper", "attention mechanism notes"))
    journal.append(MemoryEntry.now("capture", "daily digest", "personal knowledge management"))
    return tmp_path


def test_tokenize_lowercases() -> None:
    assert tokenize("Hello, Agents!") == ["hello", "agents"]


def test_collect_markdown_and_journal(tmp_path: Path) -> None:
    docs = collect_documents(_seed(tmp_path))
    sources = {d.source for d in docs}
    assert "markdown" in sources
    assert "journal" in sources
    titles = [d.title for d in docs]
    assert any("Knowledge capture" in t for t in titles)


def test_search_ranks_matching_docs(tmp_path: Path) -> None:
    root = _seed(tmp_path)
    hits = search_kb(root, "agents knowledge")
    assert hits
    assert hits[0].score >= hits[-1].score
    blob = " ".join(h.title + h.snippet for h in hits).lower()
    assert "agent" in blob or "knowledge" in blob


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
