"""Daily / weekly review sketches and a reviews digest from journal + tasks.

Writes memory/reviews/{daily|weekly|digest}-YYYY-MM-DD.md and a kind=review journal row.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

from core.memory import Journal, MemoryEntry, normalize_kind, normalize_tags
from tools.report import entry_day, parse_day
from tools.tasks import Task, format_tasks, list_tasks, load_tasks

PERIODS = ("daily", "weekly")
DIGEST_KINDS = ("daily", "weekly", "digest", "other")


def reviews_dir(root: Path) -> Path:
    return root / "memory" / "reviews"


def count_reviews(root: Path) -> int:
    """Count daily/weekly review sketches under memory/reviews/*.md."""
    folder = reviews_dir(root)
    if not folder.is_dir():
        return 0
    n = 0
    try:
        for path in folder.iterdir():
            if path.is_file() and path.suffix.lower() == ".md":
                n += 1
    except OSError:
        return 0
    return n


def count_digests(root: Path) -> int:
    """Count reviews coverage digests (digest-*.md) under memory/reviews/."""
    return len(list_digest_files(root))


def list_digest_files(root: Path) -> list[Path]:
    """Sorted digest-*.md files under memory/reviews/ (missing dir → [])."""
    files: list[Path] = []
    for path in list_review_files(root):
        kind, _ = classify_review_name(path.name)
        if kind == "digest":
            files.append(path)
    return files


def format_digest_listing(root: Path) -> str:
    """Status snippet: digests=N plus one filename per digest."""
    files = list_digest_files(root)
    lines = [f"digests={len(files)}"]
    for path in files:
        lines.append(f"- {path.name}")
    return "\n".join(lines)


def normalize_period(period: str | None) -> str:
    raw = (period or "daily").strip().lower()
    aliases = {
        "day": "daily",
        "d": "daily",
        "week": "weekly",
        "w": "weekly",
        "7d": "weekly",
    }
    raw = aliases.get(raw, raw)
    if raw not in PERIODS:
        raise ValueError(f"period must be one of {', '.join(PERIODS)}, got {period!r}")
    return raw


def review_window(day: date, period: str) -> tuple[date, date]:
    kind = normalize_period(period)
    if kind == "weekly":
        return day - timedelta(days=6), day
    return day, day


def journal_in_window(
    journal: Journal,
    *,
    since: date,
    until: date,
    max_entries: int | None = None,
) -> list[MemoryEntry]:
    rows: list[MemoryEntry] = []
    for entry in journal.load():
        day = entry_day(entry.timestamp)
        if day is None:
            continue
        if day < since or day > until:
            continue
        rows.append(entry)
    if max_entries is not None and max_entries >= 0:
        rows = rows[-max_entries:]
    return rows


def _done_in_window(task: Task, since: date, until: date) -> bool:
    if task.status != "done":
        return False
    stamp = (task.updated or task.created or "").strip()
    if len(stamp) < 10:
        return False
    try:
        day = date.fromisoformat(stamp[:10])
    except ValueError:
        return False
    return since <= day <= until


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
        task for task in load_tasks(root) if _done_in_window(task, since, until)
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


def list_review_files(root: Path) -> list[Path]:
    """Sorted markdown files under memory/reviews/ (missing dir → [])."""
    folder = reviews_dir(root)
    if not folder.is_dir():
        return []
    try:
        files = [
            path
            for path in folder.iterdir()
            if path.is_file() and path.suffix.lower() == ".md"
        ]
    except OSError:
        return []
    files.sort(key=lambda path: path.name)
    return files


def classify_review_name(name: str) -> tuple[str, str]:
    """Return (kind, day-or-stem) for a review filename."""
    stem = name[:-3] if name.lower().endswith(".md") else name
    for kind in ("daily", "weekly", "digest"):
        prefix = f"{kind}-"
        if stem.lower().startswith(prefix):
            return kind, stem[len(prefix) :]
    return "other", stem


@dataclass
class DigestResult:
    day: str
    path: Path
    review_count: int
    daily_count: int
    weekly_count: int
    digest_count: int
    markdown: str


def render_digest(day: str, files: list[Path], *, review_count: int | None = None) -> str:
    """Markdown coverage note listing every review sketch on disk."""
    tallies = {kind: 0 for kind in DIGEST_KINDS}
    rows: list[tuple[str, str, str]] = []
    for path in files:
        kind, stamp = classify_review_name(path.name)
        tallies[kind] = tallies.get(kind, 0) + 1
        rows.append((kind, stamp, path.name))
    total = review_count if review_count is not None else len(files)
    lines = [
        f"# Reviews digest — {day}",
        "",
        f"Reviews={total} under memory/reviews/*.md",
        "",
        f"- daily: {tallies['daily']}",
        f"- weekly: {tallies['weekly']}",
        f"- digest: {tallies['digest']}",
        f"- other: {tallies['other']}",
        "",
        "## Coverage",
        "",
    ]
    if not rows:
        lines.append("(no review files)")
        lines.append("")
        return "\n".join(lines)
    for kind, stamp, name in rows:
        label = stamp or name
        lines.append(f"- {kind}: {name} ({label})")
    lines.append("")
    return "\n".join(lines)


def write_digest(
    root: Path,
    *,
    journal: Journal | None = None,
    day: str | None = None,
    tags: Iterable[str] | None = None,
) -> DigestResult:
    """Write memory/reviews/digest-YYYY-MM-DD.md and a kind=review journal row."""
    day_key = day or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if parse_day(day_key) is None:
        raise ValueError(f"day must be YYYY-MM-DD, got {day_key!r}")

    files = list_review_files(root)
    existing_names = {path.name for path in files}
    digest_name = f"digest-{day_key}.md"
    planned = list(files)
    dest = reviews_dir(root) / digest_name
    if digest_name not in existing_names:
        planned.append(dest)
        planned.sort(key=lambda path: path.name)

    tallies = {kind: 0 for kind in DIGEST_KINDS}
    for path in planned:
        kind, _ = classify_review_name(path.name)
        tallies[kind] = tallies.get(kind, 0) + 1

    markdown = render_digest(day_key, planned, review_count=len(planned))
    folder = reviews_dir(root)
    folder.mkdir(parents=True, exist_ok=True)
    dest.write_text(markdown, encoding="utf-8")

    memory_dir = root / "memory"
    log = journal or Journal(memory_dir / "journal.jsonl")
    extra = list(tags) if tags is not None else []
    log.append(
        MemoryEntry.now(
            "review",
            f"Wrote reviews digest {dest.name} (Reviews={len(planned)})",
            markdown[:800],
            tags=normalize_tags(["review", "digest", *extra]),
        )
    )
    return DigestResult(
        day=day_key,
        path=dest,
        review_count=len(planned),
        daily_count=tallies["daily"],
        weekly_count=tallies["weekly"],
        digest_count=tallies["digest"],
        markdown=markdown,
    )


def write_cycle_digest(
    root: Path,
    *,
    journal: Journal | None = None,
    day: str | None = None,
) -> DigestResult:
    """Write today's reviews digest as part of a non-dry cycle (tags include cycle)."""
    return write_digest(root, journal=journal, day=day, tags=["cycle"])
