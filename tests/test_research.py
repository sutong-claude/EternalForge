from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.memory import Journal
from tools.research import FixtureAdapter, Hit, format_hits, record_hits, search, summarize


def test_fixture_adapter_matches_seeded_topic() -> None:
    hits = search("EternalForge vision", adapter=FixtureAdapter())
    assert hits
    assert hits[0].title == "EternalForge"
    assert "github.com" in hits[0].url


def test_empty_query_returns_nothing() -> None:
    assert FixtureAdapter().search("   ") == []


def test_unknown_topic_returns_placeholder() -> None:
    hits = FixtureAdapter().search("quantum-xyz-unknown")
    assert len(hits) == 1
    assert hits[0].source == "fixture"


def test_max_results_is_respected() -> None:
    catalog = {
        "alpha": [
            Hit("A", "u1", "s1", "fixture"),
            Hit("B", "u2", "s2", "fixture"),
            Hit("C", "u3", "s3", "fixture"),
        ]
    }
    hits = FixtureAdapter(catalog).search("alpha", max_results=2)
    assert [h.title for h in hits] == ["A", "B"]


def test_summarize_truncates() -> None:
    text = "word " * 80
    out = summarize(text, max_length=40)
    assert len(out) == 40
    assert out.endswith("...")


def test_format_hits_empty() -> None:
    assert format_hits([]) == "(no results)"


def test_record_hits_writes_journal(tmp_path: Path) -> None:
    hits = [
        Hit(
            title="EternalForge",
            url="https://github.com/sutong-claude/EternalForge",
            snippet="Personal AI research platform.",
            source="fixture",
        )
    ]
    journal = Journal(tmp_path / "memory" / "journal.jsonl")
    entry = record_hits("eternalforge", hits, journal=journal)
    assert entry.kind == "research"
    assert "eternalforge" in entry.summary
    assert "1 hit" in entry.summary
    path = tmp_path / "memory" / "journal.jsonl"
    assert path.exists()
    row = json.loads(path.read_text(encoding="utf-8").splitlines()[-1])
    assert row["kind"] == "research"
    assert "EternalForge" in row["details"]


def test_record_hits_empty_query_still_journals(tmp_path: Path) -> None:
    journal = Journal(tmp_path / "journal.jsonl")
    entry = record_hits("blank", [], journal=journal)
    assert entry.kind == "research"
    assert "0 hit" in entry.summary
    assert "(no results)" in entry.details
