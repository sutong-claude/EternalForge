from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.changelog import (
    append_entry,
    count_versions,
    count_versions_file,
    cycle_extras,
    next_version,
)
from core.metrics import bump_metrics, count_tests
from core.state import ForgeState


def test_next_version_bumps_patch() -> None:
    text = "# Changelog\n\n## 0.3.0 — 2026-09-14\n\n- item\n"
    assert next_version(text) == "0.3.1"


def test_count_versions_ignores_non_semver() -> None:
    text = (
        "# Changelog\n\n"
        "## 0.2.0 — 2026-09-14\n\n- a\n\n"
        "## Notes\n\n"
        "## 0.1.0 — 2026-09-13\n\n- b\n"
    )
    assert count_versions(text) == 2
    assert count_versions("") == 0


def test_count_versions_file_missing(tmp_path: Path) -> None:
    assert count_versions_file(tmp_path / "CHANGELOG.md") == 0
    path = tmp_path / "CHANGELOG.md"
    path.write_text("# Changelog\n\n## 1.0.0 — today\n\n- x\n", encoding="utf-8")
    assert count_versions_file(path) == 1


def test_cycle_extras_formats_counts() -> None:
    assert cycle_extras(reports=0, tasks=0) == [
        "reports=0",
        "tasks=0",
        "reviews=0",
        "digests=0",
    ]
    assert cycle_extras(reports=3, tasks=1, reviews=2, digests=1) == [
        "reports=3",
        "tasks=1",
        "reviews=2",
        "digests=1",
    ]


def test_append_entry_prepends_section(tmp_path: Path) -> None:
    path = tmp_path / "CHANGELOG.md"
    path.write_text("# Changelog\n\n## 0.1.0 — 2026-09-14\n\n- start\n", encoding="utf-8")
    version = append_entry(path, "Did the thing", extra=["detail"], day="2026-09-14")
    assert version == "0.1.1"
    text = path.read_text(encoding="utf-8")
    assert text.startswith("# Changelog\n\n## 0.1.1 — 2026-09-14\n")
    assert "Did the thing" in text
    assert "## 0.1.0" in text
    assert count_versions(text) == 2


def test_bump_metrics_increments_cycles(tmp_path: Path) -> None:
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_demo.py").write_text(
        "def test_ok():\n    assert True\n", encoding="utf-8"
    )
    (tmp_path / "README.md").write_text("x", encoding="utf-8")
    state = ForgeState(
        last_updated="x",
        phase="p",
        progress=0.2,
        current_goal="g",
        metrics={"Cycles": "2", "Features shipped": "5"},
    )
    bump_metrics(state, tmp_path)
    assert state.metrics["Cycles"] == "3"
    assert int(state.metrics["Files"]) >= 2
    assert count_tests(tmp_path) == 1
    assert state.metrics["Tests"] == "1"
