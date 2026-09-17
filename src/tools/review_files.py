"""Filesystem helpers for memory/reviews/*.md."""

from __future__ import annotations

from pathlib import Path

from tools.review_const import DIGEST_KINDS


def reviews_dir(root: Path) -> Path:
    return root / "memory" / "reviews"


def classify_review_name(name: str) -> tuple[str, str]:
    """Return (kind, day-or-stem) for a review filename."""
    stem = name[:-3] if name.lower().endswith(".md") else name
    for kind in ("daily", "weekly", "digest"):
        prefix = f"{kind}-"
        if stem.lower().startswith(prefix):
            return kind, stem[len(prefix) :]
    return "other", stem


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


def list_digest_files(root: Path) -> list[Path]:
    """Sorted digest-*.md files under memory/reviews/ (missing dir → [])."""
    files: list[Path] = []
    for path in list_review_files(root):
        kind, _ = classify_review_name(path.name)
        if kind == "digest":
            files.append(path)
    return files


def count_digests(root: Path) -> int:
    """Count reviews coverage digests (digest-*.md) under memory/reviews/."""
    return len(list_digest_files(root))


def format_digest_listing(root: Path) -> str:
    """Status snippet: digests=N plus one filename per digest."""
    files = list_digest_files(root)
    lines = [f"digests={len(files)}"]
    for path in files:
        lines.append(f"- {path.name}")
    return "\n".join(lines)


def digest_tallies(files: list[Path]) -> dict[str, int]:
    tallies = {kind: 0 for kind in DIGEST_KINDS}
    for path in files:
        kind, _ = classify_review_name(path.name)
        tallies[kind] = tallies.get(kind, 0) + 1
    return tallies
