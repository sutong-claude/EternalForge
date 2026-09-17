"""Task tracker constants and normalizers."""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path

STATUSES = ("open", "done", "cancelled")
PRIORITIES = ("low", "medium", "high", "urgent")
PRIORITY_RANK = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
SORTS = ("due", "priority", "created", "updated")
DEFAULT_DUE_SOON_DAYS = 7


def tasks_path(root: Path) -> Path:
    return Path(root) / "memory" / "tasks.jsonl"


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
        "age": "created",
        "new": "updated",
        "newest": "updated",
        "recent": "updated",
    }
    raw = aliases.get(raw, raw)
    if raw not in SORTS:
        raise ValueError(f"sort must be one of {', '.join(SORTS)}, got {sort!r}")
    return raw


def normalize_tag_token(tag: str | None) -> str:
    return (tag or "").strip().lstrip("#").lower()


def normalize_query(query: str | None) -> str:
    return " ".join((query or "").strip().lower().split())


def normalize_id_prefix(prefix: str | None) -> str:
    raw = (prefix or "").strip().lower()
    return raw


def normalize_created_day(value: str | None) -> str:
    raw = (value or "").strip()
    if not raw:
        return ""
    try:
        return date.fromisoformat(raw[:10]).isoformat()
    except ValueError as exc:
        raise ValueError(f"created day must be YYYY-MM-DD, got {value!r}") from exc


def normalize_updated_day(value: str | None) -> str:
    raw = (value or "").strip()
    if not raw:
        return ""
    try:
        return date.fromisoformat(raw[:10]).isoformat()
    except ValueError as exc:
        raise ValueError(f"updated day must be YYYY-MM-DD, got {value!r}") from exc


def created_day(stamp: str | None) -> str:
    raw = (stamp or "").strip()
    if len(raw) >= 10:
        try:
            return date.fromisoformat(raw[:10]).isoformat()
        except ValueError:
            return ""
    return ""


def updated_day(stamp: str | None) -> str:
    return created_day(stamp)


def normalize_due_soon_days(days: int | str | None) -> int:
    if days is None or days is False:
        return DEFAULT_DUE_SOON_DAYS
    raw = str(days).strip().lower()
    if raw in ("", "true", "yes", "soon"):
        return DEFAULT_DUE_SOON_DAYS
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"due-soon days must be an integer >= 0, got {days!r}") from exc
    if value < 0:
        raise ValueError(f"due-soon days must be an integer >= 0, got {days!r}")
    return value


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today(value: date | str | None = None) -> date:
    if value is None:
        return datetime.now(timezone.utc).date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))
