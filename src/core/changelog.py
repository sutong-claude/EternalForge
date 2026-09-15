"""Keep CHANGELOG.md in lockstep with each completed cycle."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re

_VERSION_HEADING = re.compile(r"^##\s+(\d+\.\d+\.\d+)\b")


def utc_day() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def count_versions(text: str) -> int:
    """Count ## X.Y.Z headings in a changelog body."""
    n = 0
    for line in text.splitlines():
        if _VERSION_HEADING.match(line.strip()):
            n += 1
    return n


def count_versions_file(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        return count_versions(path.read_text(encoding="utf-8"))
    except OSError:
        return 0


def next_version(existing: str) -> str:
    """Bump the patch of the first ## X.Y.Z heading. Default 0.1.0."""
    for line in existing.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            token = stripped[3:].split()[0]
            parts = token.split(".")
            if len(parts) == 3 and all(p.isdigit() for p in parts):
                major, minor, patch = (int(p) for p in parts)
                return f"{major}.{minor}.{patch + 1}"
            break
    return "0.1.0"


def cycle_extras(*, reports: int, tasks: int) -> list[str]:
    """Metric bullets appended to each cycle CHANGELOG section."""
    return [f"reports={int(reports)}", f"tasks={int(tasks)}"]


def render_section(version: str, day: str, bullets: list[str]) -> str:
    items = "\n".join(f"- {b}" for b in bullets) or "- Cycle completed."
    return f"## {version} — {day}\n\n{items}\n"


def append_entry(
    path: Path,
    summary: str,
    *,
    extra: list[str] | None = None,
    day: str | None = None,
) -> str:
    """Prepend a new version section under the title. Returns the version."""
    day = day or utc_day()
    bullets = [summary]
    if extra:
        bullets.extend(extra)
    existing = path.read_text(encoding="utf-8") if path.exists() else "# Changelog\n"
    version = next_version(existing)
    section = render_section(version, day, bullets)
    if existing.lstrip().startswith("#"):
        first_nl = existing.find("\n")
        title = existing[: first_nl + 1] if first_nl >= 0 else existing + "\n"
        rest = existing[len(title) :].lstrip("\n")
        text = title + "\n" + section + ("\n" + rest if rest else "")
    else:
        text = "# Changelog\n\n" + section + "\n" + existing
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return version
