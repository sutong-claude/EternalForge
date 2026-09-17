"""Render and persist daily/weekly review sketches."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable

from core.memory import Journal, MemoryEntry, normalize_kind, normalize_tags
from tools.report import parse_day
from tools.review_files import reviews_dir
from tools.review_window import done_in_window, journal_in_window, normalize_period, review_window
from tools.tasks import Task, format_tasks, list_tasks, load_tasks


@dataclass
class ReviewResult:
    day: str
    period: str
    path: Path
    journal_count: int
    open_count: int
    overdue_count: int
    done_count: int
    markdown: str
    since: str = ""
    until: str = ""
    kinds: list[str] = field(default_factory=list)


def render_review(
    day: str,
    period: str,
    *,
    since: date,
    until: date,
    entries: list[MemoryEntry],
    open_tasks: list[Task],
    overdue_tasks: list[Task],
    due_soon_tasks: list[Task],
    done_tasks: list[Task],
    today: date | None = None,
) -> str:
    lines = [
        f"# {period.capitalize()} review — {day}",
        "",
        f"Window: {since.isoformat()} → {until.isoformat()}",
        "",
    ]
    if not entries:
        lines.append("## Journal")
        lines.append("")
        lines.append("(no journal entries)")
        lines.append("")
    else:
        kind_counts: dict[str, int] = {}
        order: list[str] = []
        for entry in entries:
            kind = normalize_kind(entry.kind) or "(none)"
            if kind not in kind_counts:
                kind_counts[kind] = 0
                order.append(kind)
            kind_counts[kind] += 1
        lines.append("## Journal")
        lines.append("")
        lines.append(f"{len(entries)} journal row(s) across {len(order)} kind(s).")
        lines.append("")
        for kind in order:
            lines.append(f"- {kind}: {kind_counts[kind]}")
        lines.append("")
        lines.append("### Recent")
        lines.append("")
        for entry in entries[-12:]:
            stamp = entry.timestamp or "(no timestamp)"
            tag_bit = f" #{',#'.join(entry.tags)}" if entry.tags else ""
            lines.append(f"- {stamp} [{entry.kind}] {entry.summary}{tag_bit}")
        lines.append("")

    lines.append("## Tasks")
    lines.append("")
    lines.append(
        f"Open: {len(open_tasks)} · Overdue: {len(overdue_tasks)} · Due soon: {len(due_soon_tasks)} · Done in window: {len(done_tasks)}"
    )
    lines.append("")
    if overdue_tasks:
        lines.append("### Overdue")
        lines.append("")
        lines.append(format_tasks(overdue_tasks, today=today))
        lines.append("")
    if due_soon_tasks:
        lines.append("### Due soon")
        lines.append("")
        lines.append(format_tasks(due_soon_tasks, today=today))
        lines.append("")
    if open_tasks:
        lines.append("### Open")
        lines.append("")
        lines.append(format_tasks(open_tasks, today=today))
        lines.append("")
    if done_tasks:
        lines.append("### Done in window")
        lines.append("")
        lines.append(format_tasks(done_tasks, today=today))
        lines.append("")
    if not (open_tasks or overdue_tasks or due_soon_tasks or done_tasks):
        lines.append("(no tasks)")
        lines.append("")
    return "\n".join(lines)


def write_review(
    root: Path,
    *,
    journal: Journal | None = None,
    day: str | None = None,
    period: str = "daily",
    max_entries: int | None = None,
    tags: Iterable[str] | None = None,
    today: date | None = None,
) -> ReviewResult:
    period_key = normalize_period(period)
    day_key = day or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    day_value = parse_day(day_key)
    if day_value is None:
        raise ValueError(f"day must be YYYY-MM-DD, got {day_key!r}")

    since, until = review_window(day_value, period_key)
    memory_dir = root / "memory"
    log = journal or Journal(memory_dir / "journal.jsonl")
    entries = journal_in_window(log, since=since, until=until, max_entries=max_entries)

    as_of = today or until
    open_tasks = list_tasks(root, status="open", today=as_of)
    overdue_tasks = [task for task in open_tasks if task.is_overdue(as_of)]
    due_soon_tasks = [
        task for task in open_tasks if task.is_due_soon(today=as_of) and not task.is_overdue(as_of)
    ]
    done_tasks = [
        task for task in load_tasks(root) if done_in_window(task, since, until)
    ]

    markdown = render_review(
        day_key,
        period_key,
        since=since,
        until=until,
        entries=entries,
        open_tasks=open_tasks,
        overdue_tasks=overdue_tasks,
        due_soon_tasks=due_soon_tasks,
        done_tasks=done_tasks,
        today=as_of,
    )

    folder = reviews_dir(root)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{period_key}-{day_key}.md"
    path.write_text(markdown, encoding="utf-8")

    kinds: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        kind = normalize_kind(entry.kind) or "(none)"
        if kind not in seen:
            seen.add(kind)
            kinds.append(kind)

    extra = list(tags) if tags is not None else []
    log.append(
        MemoryEntry.now(
            "review",
            f"Wrote {period_key} review {path.name} ({len(entries)} journal, {len(open_tasks)} open)",
            markdown[:800],
            tags=normalize_tags(["review", period_key, *extra]),
        )
    )
    return ReviewResult(
        day=day_key,
        period=period_key,
        path=path,
        journal_count=len(entries),
        open_count=len(open_tasks),
        overdue_count=len(overdue_tasks),
        done_count=len(done_tasks),
        markdown=markdown,
        since=since.isoformat(),
        until=until.isoformat(),
        kinds=kinds,
    )


def write_cycle_weekly(
    root: Path,
    *,
    journal: Journal | None = None,
    day: str | None = None,
) -> ReviewResult:
    """Write today's weekly review sketch as part of a non-dry cycle (tags include cycle)."""
    return write_review(
        root,
        journal=journal,
        day=day,
        period="weekly",
        tags=["cycle"],
    )


def write_cycle_daily(
    root: Path,
    *,
    journal: Journal | None = None,
    day: str | None = None,
) -> ReviewResult:
    """Write today's daily review sketch as part of a non-dry cycle (tags include cycle)."""
    return write_review(
        root,
        journal=journal,
        day=day,
        period="daily",
        tags=["cycle"],
    )
