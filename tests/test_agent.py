from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.agent import Agent
from core.state import dump_state, ForgeState


def _seed(tmp: Path) -> Path:
    state = ForgeState(
        last_updated="2026-09-14",
        phase="Core Agent",
        progress=0.18,
        current_goal="Build the loop",
        priorities=["Implement CLI", "Add research tool"],
        notes="Keep one task per cycle.",
    )
    (tmp / "STATE.md").write_text(dump_state(state), encoding="utf-8")
    return tmp


def test_plan_returns_first_priority(tmp_path: Path) -> None:
    agent = Agent(_seed(tmp_path))
    assert agent.plan() == "Implement CLI"


def test_dry_run_does_not_mutate(tmp_path: Path) -> None:
    root = _seed(tmp_path)
    before = (root / "STATE.md").read_text(encoding="utf-8")
    Agent(root).run_once(dry_run=True)
    after = (root / "STATE.md").read_text(encoding="utf-8")
    assert before == after
