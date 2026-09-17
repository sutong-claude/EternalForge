"""Reviews coverage digest listing every sketch on disk."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from core.memory import Journal, MemoryEntry, normalize_tags
from tools.report import parse_day
from tools.review_const import DIGEST_KINDS
from tools.review_files import classify_review_name, digest_tallies, list_review_files, reviews_dir


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

    tallies = digest_tallies(planned)
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
