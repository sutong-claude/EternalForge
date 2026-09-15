"""Lightweight personal task tracker.

Persists tasks as JSONL under memory/tasks.jsonl. This is a skeleton for
Phase 3 productivity: add, list, and close tasks without a database.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
import json
from pathlib import Path
from typing import Iterable

from core.memory import Journal, MemoryEntry, normalize_tags

STATUSES = ("open", "done", "cancelled")
PRIORITIES = ("low", "medium", "high", "urgent")
PRIORITY_RANK = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
SORTS = ("due", "priority")


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
    aliases = {"date": "due", "deadline": "due", "pri": "priority", "p": "priority"}
    raw = aliases.get(raw, raw)
    if raw not in SORTS:
        raise ValueError(f"sort must be one of {', '.join(SORTS)}, got {sort!r}")
    return raw


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

    def is_overdue(self, today: date | str | None = None) -> bool:
        if self.status != "open" or not self.due:
            return False
        return date.fromisoformat(self.due) < _today(today)

    def sort_key(self, sort: str | None = None) -> tuple:
        mode = normalize_sort(sort)
        rank = PRIORITY_RANK.get(self.priority, 2)
        undated = 1 if not self.due else 0
        due = self.due or "9999-12-31"
        if mode == "priority":
            return (rank, undated, due, self.id)
        return (undated, due, rank, self.id)


def _next_id(existing: list[Task]) -> str:
    n = 0
    for task in existing:
        raw = (task.id or "").lstrip("Tt")
        try:
            n = max(n, int(raw))
        except ValueError:
            continue
    return f"T{n + 1:03d}"


def load_tasks(root: Path) -> list[Task]:
    path = tasks_path(root)
    if not path.exists():
        return []
    out: list[Task] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            continue
        title = str(data.get("title", "")).strip()
        tid = str(data.get("id", "")).strip()
        if not title or not tid:
            continue
        try:
            status = normalize_status(str(data.get("status", "open")))
        except ValueError:
            status = "open"
        try:
            priority = normalize_priority(str(data.get("priority", "medium") or "medium"))
        except ValueError:
            priority = "medium"
        try:
            due = normalize_due(str(data.get("due", "") or ""))
        except ValueError:
            due = ""
        out.append(
            Task(
                id=tid,
                title=title,
                status=status,
                notes=str(data.get("notes", "")),
                tags=normalize_tags(data.get("tags", [])),
                created=str(data.get("created", "")),
                updated=str(data.get("updated", "")),
                due=due,
                priority=priority,
            )
        )
    return out


def save_tasks(root: Path, tasks: list[Task]) -> Path:
    path = tasks_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for task in tasks:
        payload = asdict(task)
        payload["tags"] = normalize_tags(task.tags)
        payload["status"] = normalize_status(task.status)
        payload["priority"] = normalize_priority(task.priority)
        payload["due"] = normalize_due(task.due)
        lines.append(json.dumps(payload, ensure_ascii=False))
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return path


def count_open_tasks(root: Path) -> int:
    return sum(1 for task in load_tasks(root) if task.status == "open")


def sort_tasks(tasks: Iterable[Task], sort: str | None = "due") -> list[Task]:
    return sorted(tasks, key=lambda task: task.sort_key(sort))


def list_tasks(
    root: Path,
    status: str | None = None,
    priority: str | None = None,
    *,
    overdue: bool = False,
    sort: str | None = "due",
    today: date | str | None = None,
) -> list[Task]:
    wanted = status.strip() if status and status.strip() else None
    wanted_pri = priority.strip() if priority and priority.strip() else None
    rows = [
        task
        for task in load_tasks(root)
        if task.matches_status(wanted) and task.matches_priority(wanted_pri)
    ]
    if overdue:
        rows = [task for task in rows if task.is_overdue(today)]
    return sort_tasks(rows, sort=sort)


def format_tasks(tasks: list[Task], today: date | str | None = None) -> str:
    if not tasks:
        return "(no tasks)"
    lines: list[str] = []
    for task in tasks:
        tag_bit = f" #{',#'.join(task.tags)}" if task.tags else ""
        due_bit = f" due={task.due}" if task.due else ""
        pri_bit = f" p={task.priority}" if task.priority != "medium" else ""
        overdue_bit = " OVERDUE" if task.is_overdue(today) else ""
        lines.append(
            f"{task.id}\t{task.status}{overdue_bit}\t{task.title}{pri_bit}{due_bit}{tag_bit}"
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
    stamp = _utc_now()
    task = Task(
        id=_next_id(existing),
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
    found.updated = _utc_now()
    save_tasks(root, tasks)
    log = journal or Journal(root / "memory" / "journal.jsonl")
    parts = [f"Set {found.id}"]
    if status is not None:
        parts.append(found.status)
    if due is not None:
        parts.append(f"due={found.due or '-'}")
    if priority is not None:
        parts.append(f"p={found.priority}")
    parts.append(f": {found.title}")
    log.append(
        MemoryEntry.now(
            "task",
            " ".join(parts),
            "",
            tags=normalize_tags(["task", found.status, found.priority, *found.tags]),
        )
    )
    return found
