from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.agent import Agent
from core.state import dump_state, ForgeState, parse_state


def _seed(tmp: Path) -> Path:
    state = ForgeState(
        last_updated="2026-09-14",
        phase="Core Agent",
        progress=0.18,
        current_goal="Build the loop",
        priorities=["Implement CLI", "Add research tool"],
        metrics={"Files": "1", "Tests": "0", "Features shipped": "1", "Cycles": "0"},
        notes="Keep one task per cycle.",
    )
    (tmp / "STATE.md").write_text(dump_state(state), encoding="utf-8")
    (tmp / "CHANGELOG.md").write_text(
        "# Changelog\n\n## 0.1.0 — 2026-09-14\n\n- bootstrap\n",
        encoding="utf-8",
    )
    return tmp


def test_plan_returns_first_priority(tmp_path: Path) -> None:
    agent = Agent(_seed(tmp_path))
    assert agent.plan() == "Implement CLI"


def test_status_includes_changelog_versions(tmp_path: Path) -> None:
    agent = Agent(_seed(tmp_path))
    text = agent.status()
    assert "changelog_versions=1" in text
    assert "phase=Core Agent" in text
    assert "progress=18%" in text


def test_status_zero_versions_when_changelog_missing(tmp_path: Path) -> None:
    root = _seed(tmp_path)
    (root / "CHANGELOG.md").unlink()
    text = Agent(root).status()
    assert "changelog_versions=0" in text


def test_dry_run_does_not_mutate(tmp_path: Path) -> None:
    root = _seed(tmp_path)
    before = (root / "STATE.md").read_text(encoding="utf-8")
    Agent(root).run_once(dry_run=True)
    after = (root / "STATE.md").read_text(encoding="utf-8")
    assert before == after


def test_cycle_writes_changelog_and_bumps_metrics(tmp_path: Path) -> None:
    root = _seed(tmp_path)
    Agent(root).run_once(dry_run=False)
    log = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## 0.1.1" in log
    assert "Implement CLI" in log
    state = parse_state((root / "STATE.md").read_text(encoding="utf-8"))
    assert state.metrics["Cycles"] == "1"
    assert state.priorities == ["Add research tool"]
    journal = (root / "memory" / "journal.jsonl").read_text(encoding="utf-8")
    assert "changelog=" in journal
    assert "changelog_versions=2" in Agent(root).status()
