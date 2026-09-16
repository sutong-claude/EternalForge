"""Lightweight personal task tracker.

Persists tasks as JSONL under memory/tasks.jsonl. This is a skeleton for
Phase 3 productivity: add, list, and close tasks without a database.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Iterable

from core.memory import Journal, MemoryEntry, normalize_tags

STATUSES = ("open", "done", "cancelled")
PRIORITIES = ("low", "medium", "high", "urgent")
PRIORITY_RANK = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
SORTS = ("due", "priority", "created", "updated")
DEFAULT_DUE_SOON_DAYS = 7


def tasks_path(root: Path) -> Path:
    return root / "memory" / "tasks.jsonl"


def normalize_status(status: str | None) -> str:
    raw = (status or "open").strip().lower()
    aliases = {
        "todo": "open",
        "pending": "open",
        "in-progress": "open",
        "in_progress": "open",
        "complete": "done",
        "completed": "done",
        "closed": "done",
        "cancel": "cancelled",
        "canceled": "cancelled",
    }
    raw = aliases.get(raw, raw)
    if raw not in STATUSES:
        raise ValueError(f"status must be one of {', '.join(STATUSES)}, got {status!r}")
    return raw


def normalize_priority(priority: str | None) -> str:
    raw = (priority or "medium").strip().lower()
    aliases = {
        "lo": "low",
        "med": "medium",
        "normal": "medium",
        "default": "medium",
        "hi": "high",
        "important": "high",
        "p0": "urgent",
        "p1": "high",
        "p2": "medium",
        "p3": "low",
        "crit": "urgent",
        "critical": "urgent",
    }
    raw = aliases.get(raw, raw)
    if raw not in PRIORITIES:
        raise ValueError(
            f"priority must be one of {', '.join(PRIORITIES)}, got {priority!r}"
        )
    return raw


def normalize_due(due: str | None) -> str:
    raw = (due or "").strip()
    if not raw:
        return ""
    try:
        parsed = date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"due must be YYYY-MM-DD, got {due!r}") from exc
    return parsed.isoformat()


def normalize_sort(sort: str | None) -> str:
    raw = (sort or "due").strip().lower()
    aliases = {
        "date": "due",
        "deadline": "due",
        "pri": "priority",
        "p": "priority",
        "create": "created",
        "added": "created",
        "new": "created",
        "mtime": "updated",
        "modified": "updated",
        "edit": "updated",
    }
    raw = aliases.get(raw, raw)
    if raw not in SORTS:
        raise ValueError(f"sort must be one of {', '.join(SORTS)}, got {sort!r}")
    return raw
