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
