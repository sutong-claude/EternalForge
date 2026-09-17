"""Period aliases and journal/task windows for review sketches."""

from __future__ import annotations

from datetime import date, timedelta

from core.memory import Journal, MemoryEntry
from tools.report import entry_day
from tools.review_const import PERIODS
from tools.tasks import Task


def normalize_period(period: str | None) -> str:
    raw = (period or "daily").strip().lower()
    aliases = {
        "day": "daily",
        "d": "daily",
        "week": "weekly",
        "w": "weekly",
        "7d": "weekly",
    }
    raw = aliases.get(raw, raw)
    if raw not in PERIODS:
        raise ValueError(f"period must be one of {', '.join(PERIODS)}, got {period!r}")
    return raw


def review_window(day: date, period: str) -> tuple[date, date]:
    kind = normalize_period(period)
    if kind == "weekly":
        return day - timedelta(days=6), day
    return day, day


def journal_in_window(
    journal: Journal,
    *,
    since: date,
    until: date,
    max_entries: int | None = None,
) -> list[MemoryEntry]:
    rows: list[MemoryEntry] = []
    for entry in journal.load():
        day = entry_day(entry.timestamp)
        if day is None:
            continue
        if day < since or day > until:
            continue
        rows.append(entry)
    if max_entries is not None and max_entries >= 0:
        rows = rows[-max_entries:]
    return rows


def done_in_window(task: Task, since: date, until: date) -> bool:
    if task.status != "done":
        return False
    stamp = (task.updated or task.created or "").strip()
    if len(stamp) < 10:
        return False
    try:
        day = date.fromisoformat(stamp[:10])
    except ValueError:
        return False
    return since <= day <= until
