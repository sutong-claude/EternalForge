"""Task dataclass and matching helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Iterable

from tools.task_const import (
    DEFAULT_DUE_SOON_DAYS,
    PRIORITY_RANK,
    created_day,
    normalize_created_day,
    normalize_due_soon_days,
    normalize_id_prefix,
    normalize_priority,
    normalize_query,
    normalize_sort,
    normalize_status,
    normalize_tag_token,
    normalize_updated_day,
    today as _today,
    updated_day,
)


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
        haystack = f"{self.title} {self.notes}".lower()
        return needle in haystack

    def matches_id(self, prefix: str | None, exact: bool = False) -> bool:
        needle = normalize_id_prefix(prefix)
        if not needle:
            return True
        hid = self.id.lower()
        if exact:
            return hid == needle
        return hid.startswith(needle)

    def matches_created(
        self,
        since: str | None = None,
        until: str | None = None,
    ) -> bool:
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

    def matches_updated(
        self,
        since: str | None = None,
        until: str | None = None,
    ) -> bool:
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

    def is_overdue(self, today: date | str | None = None) -> bool:
        if self.status != "open" or not self.due:
            return False
        return date.fromisoformat(self.due) < _today(today)

    def is_due_soon(
        self,
        days: int | str | None = DEFAULT_DUE_SOON_DAYS,
        today: date | str | None = None,
    ) -> bool:
        if self.status != "open" or not self.due:
            return False
        window = normalize_due_soon_days(days)
        due = date.fromisoformat(self.due)
        start = _today(today)
        end = start + timedelta(days=window)
        return start <= due <= end

    def sort_key(self, sort: str | None = None) -> tuple:
        mode = normalize_sort(sort)
        rank = PRIORITY_RANK.get(self.priority, 2)
        undated = 1 if not self.due else 0
        due = self.due or "9999-12-31"
        if mode == "priority":
            return (rank, undated, due, self.id)
        if mode == "created":
            return (self.created or "", self.id)
        if mode == "updated":
            return (self.updated or "", self.id)
        return (undated, due, rank, self.id)
