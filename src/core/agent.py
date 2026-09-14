"""Plan → act → reflect loop. Hourly automations and the CLI share this contract."""

from __future__ import annotations

from pathlib import Path

from core.changelog import append_entry
from core.memory import Journal, MemoryEntry
from core.metrics import bump_metrics
from core.planner import select_task
from core.state import ForgeState, load_state_file, save_state_file


class Agent:
    def __init__(self, root: Path | None = None):
        self.root = (root or Path.cwd()).resolve()
        self.state_path = self.root / "STATE.md"
        self.changelog_path = self.root / "CHANGELOG.md"
        self.journal = Journal(self.root / "memory" / "journal.jsonl")

    def load_state(self) -> ForgeState:
        if not self.state_path.exists():
            raise FileNotFoundError(f"Missing {self.state_path}")
        return load_state_file(self.state_path)

    def plan(self) -> str:
        return select_task(self.load_state())

    def status(self) -> str:
        state = self.load_state()
        pct = int(round(state.progress * 100))
        nxt = state.next_task() or "(none)"
        return (
            f"phase={state.phase} progress={pct}%\n"
            f"next={nxt}\n"
            f"updated={state.last_updated}"
        )

    def act(self, task: str) -> str:
        """Local cycle records intent. Code-producing agents implement the task themselves."""
        return f"queued-for-implementation: {task}"

    def reflect(self, state: ForgeState, task: str, result: str) -> None:
        state.complete_current(f"Cycled task: {task} ({result})")
        bump_metrics(state, self.root)
        save_state_file(self.state_path, state)
        version = append_entry(
            self.changelog_path,
            f"Cycle: {task}",
            extra=[result],
        )
        self.journal.append(
            MemoryEntry.now("cycle", task, f"{result} changelog={version}"),
        )

    def run_once(self, dry_run: bool = False) -> str:
        state = self.load_state()
        task = select_task(state)
        result = self.act(task)
        if dry_run:
            return f"DRY {task} -> {result}"
        self.reflect(state, task, result)
        return result


if __name__ == "__main__":
    print(Agent().status())
