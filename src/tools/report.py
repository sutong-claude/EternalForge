"""Compile a markdown research report from journal kind=research hits.

Reads memory/journal.jsonl, groups entries by query, writes
memory/reports/YYYY-MM-DD.md, and records a kind=report journal row.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
import re
from pathlib import Path

from core.memory import Journal, MemoryEntry, normalize_kind

_QUERY_RE = re.compile(r"^Research\s+['\"](.+)['\"]\s*:", re.IGNORECASE)


def _utc_day(when: datetime | None = None) -> str:
    stamp = when or datetime.now(timezone.utc)
    return stamp.strftime("%Y-%m-%d")


def parse_day(value: str | None) -> date | None:
    if value is None or not str(value).strip():
        return None
    raw = str(value).strip()
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"day must be YYYY-MM-DD, got {raw!r}") from exc


def entry_day(timestamp: str) -> date | None:
    raw = (timestamp or "").strip()
    if not raw:
        return None
    try:
        return date.fromisoformat(raw[:10])
    except ValueError:
        return None


def parse_research_query(summary: str) -> str:
    """Extract the query from a record_hits summary, else the whole summary."""
    text = (summary or "").strip()
    if not text:
        return "(untitled)"
    match = _QUERY_RE.match(text)
    if match:
        return match.group(1).strip() or "(untitled)"
    return text


@dataclass
class ReportResult:
    day: str
    path: Path
    entry_count: int
    query_count: int
    markdown: str
    queries: list[str] = field(default_factory=list)


def research_entries(
    journal: Journal,
    *,
    since: date | None = None,
    until: date | None = None,
    max_entries: int | None = None,
) -> list[MemoryEntry]:
    rows = [
        entry
        for entry in journal.load()
        if normalize_kind(entry.kind) == "research"
    ]
    if since or until:
        filtered: list[MemoryEntry] = []
        for entry in rows:
            day = entry_day(entry.timestamp)
            if day is None:
                continue
            if since and day < since:
                continue
            if until and day > until:
                continue
            filtered.append(entry)
        rows = filtered
    if max_entries is not None and max_entries >= 0:
        rows = rows[-max_entries:]
    return rows


def render_report(
    day: str,
    entries: list[MemoryEntry],
    *,
    since: date | None = None,
    until: date | None = None,
) -> str:
    lines = [
        f"# Research report — {day}",
        "",
        "Compiled from journal entries with kind=research.",
        "",
    ]
    if since or until:
        window = f"{since.isoformat() if since else '…'} → {until.isoformat() if until else '…'}"
        lines.append(f"Window: {window}")
        lines.append("")
    if not entries:
        lines.append("(no research entries)")
        lines.append("")
        return "\n".join(lines)

    grouped: dict[str, list[MemoryEntry]] = {}
    order: list[str] = []
    for entry in entries:
        query = parse_research_query(entry.summary)
        if query not in grouped:
            grouped[query] = []
            order.append(query)
        grouped[query].append(entry)

    lines.append(f"{len(entries)} research run(s) across {len(order)} query(ies).")
    lines.append("")
    for query in order:
        lines.append(f"## {query}")
        lines.append("")
        for entry in grouped[query]:
            stamp = entry.timestamp or "(no timestamp)"
            lines.append(f"- {stamp} — {entry.summary}")
            details = (entry.details or "").strip()
            if details:
                for dline in details.splitlines():
                    lines.append(f"  {dline}")
        lines.append("")
    return "\n".join(lines)


def write_report(
    root: Path,
    *,
    journal: Journal | None = None,
    day: str | None = None,
    since: date | None = None,
    until: date | None = None,
    max_entries: int | None = None,
) -> ReportResult:
    """Render a report from journal research hits and persist it."""
    day_key = day or _utc_day()
    try:
        date.fromisoformat(day_key)
    except ValueError as exc:
        raise ValueError(f"day must be YYYY-MM-DD, got {day_key!r}") from exc

    memory_dir = root / "memory"
    log = journal or Journal(memory_dir / "journal.jsonl")
    entries = research_entries(
        log, since=since, until=until, max_entries=max_entries
    )
    markdown = render_report(day_key, entries, since=since, until=until)

    reports_dir = memory_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{day_key}.md"
    path.write_text(markdown, encoding="utf-8")

    queries: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        q = parse_research_query(entry.summary)
        if q not in seen:
            seen.add(q)
            queries.append(q)

    log.append(
        MemoryEntry.now(
            "report",
            f"Wrote research report {path.name} ({len(entries)} run(s), {len(queries)} query(ies))",
            markdown[:800],
        )
    )
    return ReportResult(
        day=day_key,
        path=path,
        entry_count=len(entries),
        query_count=len(queries),
        markdown=markdown,
        queries=queries,
    )
