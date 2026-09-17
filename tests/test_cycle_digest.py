from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.agent import Agent
from core.memory import Journal
from core.state import dump_state, ForgeState, parse_state
from tools.review import write_cycle_daily, write_cycle_digest, write_cycle_weekly


def _seed(tmp: Path) -> Path:
    state = ForgeState(
        last_updated="2026-09-16",
        phase="Core Agent",
        progress=0.98,
        current_goal="Build the loop",
        priorities=["Write digest on cycle"],
        metrics={"Files": "1", "Tests": "0", "Features shipped": "1", "Cycles": "0"},
        notes="Keep one task per cycle.",
    )
    (tmp / "STATE.md").write_text(dump_state(state), encoding="utf-8")
    (tmp / "CHANGELOG.md").write_text(
        "# Changelog\n\n## 0.1.0 — 2026-09-14\n\n- bootstrap\n",
        encoding="utf-8",
    )
    return tmp


def test_write_cycle_digest_tags_cycle(tmp_path: Path) -> None:
    result = write_cycle_digest(tmp_path, day="2026-09-16")
    assert result.path.name == "digest-2026-09-16.md"
    assert result.path.is_file()
    journal = Journal(tmp_path / "memory" / "journal.jsonl")
    rows = journal.load()
    assert rows[-1].kind == "review"
    assert "cycle" in rows[-1].tags
    assert "digest" in rows[-1].tags


def test_write_cycle_weekly_tags_cycle(tmp_path: Path) -> None:
    result = write_cycle_weekly(tmp_path, day="2026-09-16")
    assert result.path.name == "weekly-2026-09-16.md"
    assert result.period == "weekly"
    assert result.path.is_file()
    text = result.path.read_text(encoding="utf-8")
    assert "Weekly review" in text
    assert "Window: 2026-09-10" in text
    journal = Journal(tmp_path / "memory" / "journal.jsonl")
    rows = journal.load()
    assert rows[-1].kind == "review"
    assert "cycle" in rows[-1].tags
    assert "weekly" in rows[-1].tags


def test_write_cycle_daily_tags_cycle(tmp_path: Path) -> None:
    result = write_cycle_daily(tmp_path, day="2026-09-16")
    assert result.path.name == "daily-2026-09-16.md"
    assert result.period == "daily"
    assert result.path.is_file()
    text = result.path.read_text(encoding="utf-8")
    assert "Daily review" in text
    assert "Window: 2026-09-16" in text
    journal = Journal(tmp_path / "memory" / "journal.jsonl")
    rows = journal.load()
    assert rows[-1].kind == "review"
    assert "cycle" in rows[-1].tags
    assert "daily" in rows[-1].tags


def test_cycle_writes_today_digest(tmp_path: Path) -> None:
    root = _seed(tmp_path)
    folder = root / "memory" / "reviews"
    folder.mkdir(parents=True)
    (folder / "daily-2026-09-16.md").write_text("# daily\n", encoding="utf-8")
    Agent(root).run_once(dry_run=False)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    digest = folder / f"digest-{today}.md"
    weekly = folder / f"weekly-{today}.md"
    daily = folder / f"daily-{today}.md"
    assert digest.is_file()
    assert weekly.is_file()
    assert daily.is_file()
    text = digest.read_text(encoding="utf-8")
    assert "Reviews digest" in text
    assert f"weekly-{today}.md" in text
    assert f"daily-{today}.md" in text
    state = parse_state((root / "STATE.md").read_text(encoding="utf-8"))
    assert int(state.metrics["Digests"]) >= 1
    assert int(state.metrics["Reviews"]) >= 3
    log = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "digests=" in log
    journal = (root / "memory" / "journal.jsonl").read_text(encoding="utf-8")
    assert "digest-" in journal
    assert "weekly-" in journal
    assert "daily-" in journal


def test_dry_run_does_not_write_digest(tmp_path: Path) -> None:
    root = _seed(tmp_path)
    Agent(root).run_once(dry_run=True)
    reviews = root / "memory" / "reviews"
    assert not reviews.exists() or not any(reviews.glob("digest-*.md"))
    assert not reviews.exists() or not any(reviews.glob("weekly-*.md"))
    assert not reviews.exists() or not any(reviews.glob("daily-*.md"))
