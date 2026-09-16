from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.metrics import bump_metrics
from core.state import ForgeState
from tools.inbox import capture_inbox
from tools.tasks import add_task, set_task_status


def _state() -> ForgeState:
    return ForgeState(
        last_updated="2026-09-15",
        phase="Core Agent",
        progress=0.56,
        current_goal="Build the loop",
        metrics={"Files": "1", "Tests": "0", "Features shipped": "1", "Cycles": "3"},
        notes="",
    )


def test_bump_without_root_does_not_add_reports() -> None:
    state = bump_metrics(_state(), root=None)
    assert state.metrics["Cycles"] == "4"
    assert "Reports" not in state.metrics
    assert "Tasks" not in state.metrics
    assert "Reviews" not in state.metrics
    assert "Digests" not in state.metrics
    assert "Inbox" not in state.metrics


def test_bump_with_root_sets_reports_zero(tmp_path: Path) -> None:
    state = bump_metrics(_state(), root=tmp_path)
    assert state.metrics["Reports"] == "0"
    assert state.metrics["Tasks"] == "0"
    assert state.metrics["Reviews"] == "0"
    assert state.metrics["Digests"] == "0"
    assert state.metrics["Inbox"] == "0"
    assert state.metrics["Cycles"] == "4"


def test_bump_with_root_counts_report_markdown(tmp_path: Path) -> None:
    folder = tmp_path / "memory" / "reports"
    folder.mkdir(parents=True)
    (folder / "2026-09-14.md").write_text("# a\n", encoding="utf-8")
    (folder / "2026-09-15.md").write_text("# b\n", encoding="utf-8")
    (folder / "skip.txt").write_text("no\n", encoding="utf-8")
    state = bump_metrics(_state(), root=tmp_path)
    assert state.metrics["Reports"] == "2"


def test_bump_with_root_counts_review_markdown(tmp_path: Path) -> None:
    folder = tmp_path / "memory" / "reviews"
    folder.mkdir(parents=True)
    (folder / "daily-2026-09-14.md").write_text("# a\n", encoding="utf-8")
    (folder / "weekly-2026-09-16.md").write_text("# b\n", encoding="utf-8")
    (folder / "skip.txt").write_text("no\n", encoding="utf-8")
    state = bump_metrics(_state(), root=tmp_path)
    assert state.metrics["Reviews"] == "2"
    assert state.metrics["Digests"] == "0"


def test_bump_with_root_counts_digest_markdown(tmp_path: Path) -> None:
    folder = tmp_path / "memory" / "reviews"
    folder.mkdir(parents=True)
    (folder / "daily-2026-09-14.md").write_text("# a\n", encoding="utf-8")
    (folder / "digest-2026-09-16.md").write_text("# d\n", encoding="utf-8")
    (folder / "digest-2026-09-15.md").write_text("# d2\n", encoding="utf-8")
    (folder / "skip.txt").write_text("no\n", encoding="utf-8")
    state = bump_metrics(_state(), root=tmp_path)
    assert state.metrics["Reviews"] == "3"
    assert state.metrics["Digests"] == "2"


def test_bump_with_root_counts_open_tasks(tmp_path: Path) -> None:
    add_task(tmp_path, "keep open")
    closed = add_task(tmp_path, "close me")
    set_task_status(tmp_path, closed.id, "done")
    state = bump_metrics(_state(), root=tmp_path)
    assert state.metrics["Tasks"] == "1"


def test_bump_with_root_counts_inbox_entries(tmp_path: Path) -> None:
    capture_inbox(tmp_path, source="gmail", query="invoice")
    capture_inbox(tmp_path, source="drive")
    state = bump_metrics(_state(), root=tmp_path)
    assert state.metrics["Inbox"] == "2"
