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
