"""JSONL persistence for the task tracker."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from core.memory import normalize_tags
from tools.task_const import (
    normalize_due,
    normalize_priority,
    normalize_status,
    tasks_path,
)
from tools.task_model import Task


def next_id(existing: list[Task]) -> str:
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
