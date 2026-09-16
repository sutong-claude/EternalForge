"""JSONL persistence and list/add/update helpers for tools.tasks."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Iterable

from core.memory import Journal, MemoryEntry, normalize_tags
from tools.tasks import (
    DEFAULT_DUE_SOON_DAYS,
    PRIORITY_RANK,
    created_day,
    normalize_created_day,
    normalize_due,
    normalize_due_soon_days,
    normalize_id_prefix,
    normalize_priority,
    normalize_query,
    normalize_sort,
    normalize_status,
    normalize_tag_token,
    normalize_updated_day,
    tasks_path,
    updated_day,
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _today(today: date | str | None = None) -> date:
    if today is None:
        return datetime.now(timezone.utc).date()
    if isinstance(today, date):
        return today
    return date.fromisoformat(str(today))


@dataclass
class Task:
    id: str
    title: str
    status: str = "open"
    notes: str = ""
    tags: list[str] = field(default_factory=list)
    created: str = ""
    updated: str = ""
    due: str = ""
    priority: str = "medium"

    def matches_status(self, status: str | None) -> bool:
        if not status or not str(status).strip():
            return True
        return self.status == normalize_status(status)

    def matches_priority(self, priority: str | None) -> bool:
        if not priority or not str(priority).strip():
            return True
        return self.priority == normalize_priority(priority)

    def matches_tag(self, tag: str | None) -> bool:
        wanted = normalize_tag_token(tag)
        if not wanted:
            return True
        have = {normalize_tag_token(item) for item in self.tags}
        return wanted in have

    def matches_tags(self, tags: Iterable[str] | None) -> bool:
        wanted = [item for item in (tags or []) if normalize_tag_token(item)]
        if not wanted:
            return True
        return any(self.matches_tag(item) for item in wanted)

    def matches_query(self, query: str | None) -> bool:
        needle = normalize_query(query)
        if not needle:
            return True
        return needle in f"{self.title} {self.notes}".lower()

    def matches_id(self, prefix: str | None, *, exact: bool = False) -> bool:
        needle = normalize_id_prefix(prefix)
        if not needle:
            return True
        have = self.id.lower()
        return have == needle if exact else have.startswith(needle)

    def matches_created(self, since: str | None = None, until: str | None = None) -> bool:
        start = normalize_created_day(since) if since else ""
        end = normalize_created_day(until) if until else ""
        if not start and not end:
            return True
        day = created_day(self.created)
        if not day:
            return False
        if start and day < start:
            return False
        if end and day > end:
            return False
        return True

    def matches_updated(self, since: str | None = None, until: str | None = None) -> bool:
        start = normalize_updated_day(since) if since else ""
        end = normalize_updated_day(until) if until else ""
        if not start and not end:
            return True
        day = updated_day(self.updated)
        if not day:
            return False
        if start and day < start:
            return False
        if end and day > end:
            return False
        return True
