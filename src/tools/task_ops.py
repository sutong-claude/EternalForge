"""List, format, add, and update operations for tasks."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Iterable

from core.memory import Journal, MemoryEntry, normalize_tags
from tools.task_const import (
    DEFAULT_DUE_SOON_DAYS,
    normalize_due,
    normalize_due_soon_days,
    normalize_priority,
    normalize_status,
    utc_now,
)
from tools.task_model import Task
from tools.task_store import load_tasks, next_id, save_tasks


def sort_tasks(tasks: Iterable[Task], sort: str | None = "due") -> list[Task]:
    return sorted(tasks, key=lambda task: task.sort_key(sort))


def list_tasks(
    root: Path,
    status: str | None = None,
    priority: str | None = None,
    *,
    tag: str | Iterable[str] | None = None,
    query: str | None = None,
    task_id: str | None = None,
    exact_id: bool = False,
    since: str | None = None,
    until: str | None = None,
    updated_since: str | None = None,
    updated_until: str | None = None,
    overdue: bool = False,
    due_soon: bool | int | str | None = False,
    sort: str | None = "due",
    today: date | str | None = None,
) -> list[Task]:
    wanted = status.strip() if status and status.strip() else None
    wanted_pri = priority.strip() if priority and priority.strip() else None
    if isinstance(tag, str) or tag is None:
        tag_filter: list[str] = [tag] if tag and str(tag).strip() else []
    else:
        tag_filter = [item for item in tag if item and str(item).strip()]
    rows = [
        task
        for task in load_tasks(root)
        if task.matches_status(wanted)
        and task.matches_priority(wanted_pri)
        and task.matches_tags(tag_filter)
        and task.matches_query(query)
        and task.matches_id(task_id, exact=exact_id)
        and task.matches_created(since=since, until=until)
        and task.matches_updated(since=updated_since, until=updated_until)
    ]
    if overdue:
        rows = [task for task in rows if task.is_overdue(today)]
    if due_soon not in (False, None):
        window = normalize_due_soon_days(
            DEFAULT_DUE_SOON_DAYS if due_soon is True else due_soon
        )
        rows = [task for task in rows if task.is_due_soon(window, today=today)]
    return sort_tasks(rows, sort=sort)


def format_tasks(tasks: list[Task], today: date | str | None = None) -> str:
    if not tasks:
        return "(no tasks)"
    lines: list[str] = []
    for task in tasks:
        tag_bit = f" #{',#'.join(task.tags)}" if task.tags else ""
        due_bit = f" due={task.due}" if task.due else ""
        pri_bit = f" p={task.priority}" if task.priority != "medium" else ""
        flag = ""
        if task.is_overdue(today):
            flag = " OVERDUE"
        elif task.is_due_soon(today=today):
            flag = " DUE-SOON"
        lines.append(
            f"{task.id}\t{task.status}{flag}\t{task.title}{pri_bit}{due_bit}{tag_bit}"
        )
        if task.notes:
            lines.append(f"\t{task.notes}")
    return "\n".join(lines)


def add_task(
    root: Path,
    title: str,
    *,
    notes: str = "",
    tags: Iterable[str] | None = None,
    due: str | None = None,
    priority: str | None = None,
    journal: Journal | None = None,
) -> Task:
    cleaned = (title or "").strip()
    if not cleaned:
        raise ValueError("task title must not be empty")
    existing = load_tasks(root)
    stamp = utc_now()
    task = Task(
        id=next_id(existing),
        title=cleaned,
        status="open",
        notes=(notes or "").strip(),
        tags=normalize_tags(list(tags) if tags is not None else []),
        created=stamp,
        updated=stamp,
        due=normalize_due(due),
        priority=normalize_priority(priority),
    )
    existing.append(task)
    save_tasks(root, existing)
    log = journal or Journal(root / "memory" / "journal.jsonl")
    extra = list(task.tags)
    bits = [f"Added {task.id}: {task.title}"]
    if task.due:
        bits.append(f"due {task.due}")
    if task.priority != "medium":
        bits.append(f"p={task.priority}")
    log.append(
        MemoryEntry.now(
            "task",
            "; ".join(bits),
            task.notes,
            tags=normalize_tags(["task", "open", task.priority, *extra]),
        )
    )
    return task


def set_task_status(
    root: Path,
    task_id: str,
    status: str,
    *,
    journal: Journal | None = None,
) -> Task:
    return update_task(root, task_id, status=status, journal=journal)


def update_task(
    root: Path,
    task_id: str,
    *,
    status: str | None = None,
    due: str | None = None,
    priority: str | None = None,
    notes: str | None = None,
    tags: Iterable[str] | None = None,
    title: str | None = None,
    journal: Journal | None = None,
) -> Task:
    wanted = (task_id or "").strip()
    if not wanted:
        raise ValueError("task id is required")
    tasks = load_tasks(root)
    found: Task | None = None
    for task in tasks:
        if task.id.lower() == wanted.lower():
            found = task
            break
    if found is None:
        raise ValueError(f"unknown task id {wanted!r}")
    if status is not None:
        found.status = normalize_status(status)
    if due is not None:
        found.due = normalize_due(due)
    if priority is not None:
        found.priority = normalize_priority(priority)
    if notes is not None:
        found.notes = str(notes).strip()
    if tags is not None:
        found.tags = normalize_tags(list(tags))
    if title is not None:
        cleaned = str(title).strip()
        if not cleaned:
            raise ValueError("task title must not be empty")
        found.title = cleaned
    found.updated = utc_now()
    save_tasks(root, tasks)
    log = journal or Journal(root / "memory" / "journal.jsonl")
    parts = [f"Set {found.id}"]
    if status is not None:
        parts.append(found.status)
    if due is not None:
        parts.append(f"due={found.due or '-'}")
    if priority is not None:
        parts.append(f"p={found.priority}")
    if notes is not None:
        parts.append("notes" if found.notes else "notes=-")
    if tags is not None:
        parts.append("#" + ",#".join(found.tags) if found.tags else "tags=-")
    if title is not None:
        parts.append(f"title={found.title}")
    parts.append(f": {found.title}")
    log.append(
        MemoryEntry.now(
            "task",
            " ".join(parts),
            found.notes if notes is not None else "",
            tags=normalize_tags(["task", found.status, found.priority, *found.tags]),
        )
    )
    return found
