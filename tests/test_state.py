from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.state import dump_state, ForgeState, parse_progress, parse_state

SAMPLE = """# EternalForge Live State

**Last updated:** 2026-09-14 13:00 UTC
**Current phase:** Core Agent
**Overall progress:** 18%

## Current Goal
Ship a durable agent loop.

## Immediate Priorities (next few runs)
1. Implement CLI
2. Add research tool

## Recent Actions
- [2026-09-14] Initialized repo

## Known Issues / Blockers
- None yet.

## Metrics
- Files: 22
- Tests: 8

## Notes for next agent
One task per hour.
"""


def test_parse_round_trip() -> None:
    state = parse_state(SAMPLE)
    assert state.phase == "Core Agent"
    assert abs(state.progress - 0.18) < 1e-9
    assert state.priorities[0] == "Implement CLI"
    assert state.metrics["Files"] == "22"
    again = parse_state(dump_state(state))
    assert again.priorities == state.priorities
    assert again.current_goal == state.current_goal


def test_complete_current_rotates_queue() -> None:
    state = ForgeState(
        last_updated="x",
        phase="p",
        progress=0.1,
        current_goal="g",
        priorities=["a", "b"],
    )
    state.complete_current("did a")
    assert state.priorities == ["b"]
    assert "did a" in state.recent_actions[0]


def test_parse_progress_percent_and_fraction() -> None:
    assert parse_progress("34%") == 0.34
    assert parse_progress("  18 % ") == 0.18
    assert parse_progress("0.34") == 0.34
    assert parse_progress("34") == 0.34
    assert parse_progress("100%") == 1.0
    assert parse_progress("0%") == 0.0


def test_parse_progress_percent_word_and_comma() -> None:
    assert parse_progress("34 percent") == 0.34
    assert parse_progress("34 percentage") == 0.34
    assert parse_progress("1,000%") == 1.0


def test_parse_progress_invalid_and_edge() -> None:
    assert parse_progress(None) == 0.0
    assert parse_progress("") == 0.0
    assert parse_progress("   ") == 0.0
    assert parse_progress("n/a") == 0.0
    assert parse_progress("about 25% complete") == 0.25
    assert parse_progress("-5%") == 0.0
    assert parse_progress("150%") == 1.0


def test_parse_state_progress_fraction_field() -> None:
    text = SAMPLE.replace("18%", "0.42")
    state = parse_state(text)
    assert abs(state.progress - 0.42) < 1e-9


def test_parse_state_progress_garbage_defaults_zero() -> None:
    text = SAMPLE.replace("18%", "not-a-number")
    state = parse_state(text)
    assert state.progress == 0.0
