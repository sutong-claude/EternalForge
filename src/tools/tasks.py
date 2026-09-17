"""Lightweight personal task tracker.

Persists tasks as JSONL under memory/tasks.jsonl. Implementation is split
into task_const / task_model / task_store / task_ops; this module is the
public facade so imports stay `tools.tasks`.
"""

from __future__ import annotations

from tools.task_const import (
    DEFAULT_DUE_SOON_DAYS,
    PRIORITIES,
    PRIORITY_RANK,
    SORTS,
    STATUSES,
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
    today as _today,
    updated_day,
    utc_now as _utc_now,
)
from tools.task_model import Task
from tools.task_ops import (
    add_task,
    format_tasks,
    list_tasks,
    set_task_status,
    sort_tasks,
    update_task,
)
from tools.task_store import count_open_tasks, load_tasks, next_id as _next_id, save_tasks

__all__ = [
    "DEFAULT_DUE_SOON_DAYS",
    "PRIORITIES",
    "PRIORITY_RANK",
    "SORTS",
    "STATUSES",
    "Task",
    "add_task",
    "count_open_tasks",
    "created_day",
    "format_tasks",
    "list_tasks",
    "load_tasks",
    "normalize_created_day",
    "normalize_due",
    "normalize_due_soon_days",
    "normalize_id_prefix",
    "normalize_priority",
    "normalize_query",
    "normalize_sort",
    "normalize_status",
    "normalize_tag_token",
    "normalize_updated_day",
    "save_tasks",
    "set_task_status",
    "sort_tasks",
    "tasks_path",
    "update_task",
    "updated_day",
]
