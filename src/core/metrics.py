"""Recount workspace metrics and bump cycle counters on STATE."""

from __future__ import annotations

from pathlib import Path

from core.state import ForgeState

_SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"}


def _int(metrics: dict[str, str], key: str, default: int = 0) -> int:
    raw = metrics.get(key, str(default))
    try:
        return int(str(raw).split()[0])
    except ValueError:
        return default


def count_files(root: Path) -> int:
    n = 0
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in _SKIP_DIRS for part in path.parts):
            continue
        n += 1
    return n


def count_tests(root: Path) -> int:
    tests_dir = root / "tests"
    if not tests_dir.exists():
        return 0
    n = 0
    for path in tests_dir.rglob("test_*.py"):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        n += sum(1 for line in text.splitlines() if line.strip().startswith("def test_"))
    return n


def bump_metrics(state: ForgeState, root: Path | None = None) -> ForgeState:
    """Increment Cycles; refresh Files/Tests when a workspace root is given."""
    cycles = _int(state.metrics, "Cycles") + 1
    features = _int(state.metrics, "Features shipped")
    state.metrics["Cycles"] = str(cycles)
    if root is not None:
        state.metrics["Files"] = str(count_files(root))
        state.metrics["Tests"] = str(count_tests(root))
    if "Features shipped" not in state.metrics:
        state.metrics["Features shipped"] = str(features)
    if "Documentation coverage" not in state.metrics:
        state.metrics["Documentation coverage"] = "Core"
    return state
