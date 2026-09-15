"""Lightweight personal task tracker.

Persists tasks as JSONL under memory/tasks.jsonl. This is a skeleton for
Phase 3 productivity: add, list, and close tasks without a database.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Iterable

from core.memory import Journal, MemoryEntry, normalize_tags

STATUSES = ("open", "done", "cancelled")


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


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class Task:
    id: str
    title: str
    status: str = "open"
    notes: str = ""
    tags: list[str] = field(default_factory=list)
    created: str = ""
    updated: str = ""

    def matches_status(self, status: str | None) -> bool:
        if not status or not str(status).strip():
            return True
        return self.status == normalize_status(status)


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
        out.append(
            Task(
                id=tid,
                title=title,
                status=status,
                notes=str(data.get("notes", "")),
                tags=normalize_tags(data.get("tags", [])),
                created=str(data.get("created", "")),
                updated=str(data.get("updated", "")),
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
        lines.append(json.dumps(payload, ensure_ascii=False))
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return path


def count_open_tasks(root: Path) -> int:
    return sum(1 for task in load_tasks(root) if task.status == "open")


def list_tasks(root: Path, status: str | None = None) -> list[Task]:
    wanted = status.strip() if status and status.strip() else None
    return [task for task in load_tasks(root) if task.matches_status(wanted)]


def format_tasks(tasks: list[Task]) -> str:
    if not tasks:
        return "(no tasks)"
    lines: list[str] = []
    for task in tasks:
        tag_bit = f" #{',#'.join(task.tags)}" if task.tags else ""
        lines.append(f"{task.id}\t{task.status}\t{task.title}{tag_bit}")
        if task.notes:
            lines.append(f"\t{task.notes}")
    return "\n".join(lines)


def add_task(
    root: Path,
    title: str,
    *,
    notes: str = "",
    tags: Iterable[str] | None = None,
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
    )
    existing.append(task)
    save_tasks(root, existing)
    log = journal or Journal(root / "memory" / "journal.jsonl")
    extra = list(task.tags)
    log.append(
        MemoryEntry.now(
            "task",
            f"Added {task.id}: {task.title}",
            task.notes,
            tags=normalize_tags(["task", "open", *extra]),
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
    wanted = (task_id or "").strip()
    if not wanted:
        raise ValueError("task id is required")
    new_status = normalize_status(status)
    tasks = load_tasks(root)
    found: Task | None = None
    for task in tasks:
        if task.id.lower() == wanted.lower():
            task.status = new_status
            task.updated = _utc_now()
            found = task
            break
    if found is None:
        raise ValueError(f"unknown task id {wanted!r}")
    save_tasks(root, tasks)
    log = journal or Journal(root / "memory" / "journal.jsonl")
    log.append(
        MemoryEntry.now(
            "task",
            f"Set {found.id} {new_status}: {found.title}",
            "",
            tags=normalize_tags(["task", new_status, *found.tags]),
        )
    )
    return found
