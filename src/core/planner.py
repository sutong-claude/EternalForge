"""Select exactly one high-leverage next task."""

from __future__ import annotations

from core.state import ForgeState

FALLBACK = "Review STATE.md and propose next priorities"


def _actionable(task: str) -> str | None:
    cleaned = task.strip()
    if not cleaned:
        return None
    if cleaned.lower() in {"none", "none yet", "none yet."}:
        return None
    return cleaned


def select_task(state: ForgeState) -> str:
    """Return the first non-empty priority, or FALLBACK when the queue is empty."""
    for task in state.priorities:
        cleaned = _actionable(task)
        if cleaned:
            return cleaned
    return FALLBACK
