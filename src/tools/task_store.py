"""Load/save/list/add/update for the personal task tracker."""

from __future__ import annotations

from dataclasses import asdict
from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Iterable

from core.memory import Journal, MemoryEntry, normalize_tags
from tools.task_ops import Task, _today, _utc_now
from tools.tasks import (
    DEFAULT_DUE_SOON_DAYS,
    PRIORITY_RANK,
    normalize_due,
    normalize_due_soon_days,
    normalize_priority,
    normalize_sort,
    normalize_status,
    normalize_tags as _unused,
    tasks_path,
)
