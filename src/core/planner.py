"""Select exactly one high-leverage next task."""

from __future__ import annotations

from core.state import ForgeState

FALLBACK = "Review STATE.md and propose next priorities"


def select_task(state: ForgeState) -> str:
    task = state.next_task()
    return task if task else FALLBACK
