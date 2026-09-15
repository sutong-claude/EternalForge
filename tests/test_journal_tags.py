from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.memory import Journal
from tools.capture import capture
from tools.report import write_report
from tools.research import FixtureAdapter, Hit, record_hits


def test_record_hits_stores_kind_source_and_extra_tags(tmp_path: Path) -> None:
    hits = [
        Hit("EternalForge", "https://example.com", "platform", source="fixture"),
    ]
    journal = Journal(tmp_path / "journal.jsonl")
    entry = record_hits("eternalforge", hits, journal=journal, tags=["#Agents", "fixture"])
    assert entry.tags == ["research", "fixture", "agents"]
    row = json.loads(journal.path.read_text(encoding="utf-8").splitlines()[-1])
    assert row["tags"] == ["research", "fixture", "agents"]


def test_capture_journals_capture_tag(tmp_path: Path) -> None:
    result = capture(
        tmp_path,
        topics=["eternalforge"],
        adapter=FixtureAdapter(),
        day="2026-09-15",
        tags=["daily", "#Capture"],
    )
    assert result.path.exists()
    row = json.loads((tmp_path / "memory" / "journal.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert row["kind"] == "capture"
    assert row["tags"] == ["capture", "daily"]


def test_write_report_journals_report_tag(tmp_path: Path) -> None:
    journal = Journal(tmp_path / "memory" / "journal.jsonl")
    record_hits("agents", [], journal=journal, tags=["notes"])
    write_report(tmp_path, journal=journal, day="2026-09-15", tags=["weekly"])
    row = json.loads(journal.path.read_text(encoding="utf-8").splitlines()[-1])
    assert row["kind"] == "report"
    assert row["tags"] == ["report", "weekly"]
