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
