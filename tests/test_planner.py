from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.planner import FALLBACK, select_task
from core.state import ForgeState, dump_state, parse_state


def _state(**kwargs) -> ForgeState:
    base = dict(
        last_updated="2026-09-14",
        phase="Core Agent",
        progress=0.28,
        current_goal="Build the loop",
    )
    base.update(kwargs)
    return ForgeState(**base)


def test_selects_first_priority() -> None:
    state = _state(priorities=["Expand tests", "Persist research hits"])
    assert select_task(state) == "Expand tests"


def test_empty_priorities_returns_fallback() -> None:
    assert select_task(_state(priorities=[])) == FALLBACK


def test_skips_blank_and_whitespace_entries() -> None:
    state = _state(priorities=["", "   ", "\t", "Persist research hits"])
    assert select_task(state) == "Persist research hits"


def test_strips_surrounding_whitespace() -> None:
    state = _state(priorities=["  Count changelog versions  "])
    assert select_task(state) == "Count changelog versions"


def test_skips_none_yet_placeholders() -> None:
    state = _state(priorities=["None yet.", "None", "Add a second live SearchAdapter backend"])
    assert select_task(state) == "Add a second live SearchAdapter backend"


def test_all_placeholders_fall_back() -> None:
    state = _state(priorities=["None yet", "  none  ", ""])
    assert select_task(state) == FALLBACK


def test_fallback_after_completing_last_task() -> None:
    state = _state(priorities=["Only task"])
    state.complete_current("did only task")
    assert state.priorities == []
    assert select_task(state) == FALLBACK


def test_complete_current_on_empty_queue_still_falls_back() -> None:
    state = _state(priorities=[])
    state.complete_current("nothing to complete")
    assert select_task(state) == FALLBACK
    assert "nothing to complete" in state.recent_actions[0]


def test_parsed_state_with_no_priorities_section() -> None:
    text = dump_state(_state(priorities=[]))
    parsed = parse_state(text)
    assert parsed.priorities == []
    assert select_task(parsed) == FALLBACK


def test_parsed_numbered_priorities_preserve_order() -> None:
    text = dump_state(
        _state(priorities=["Persist research hits", "Add a second live SearchAdapter backend"])
    )
    parsed = parse_state(text)
    assert select_task(parsed) == "Persist research hits"
    parsed.complete_current("persisted")
    assert select_task(parsed) == "Add a second live SearchAdapter backend"
