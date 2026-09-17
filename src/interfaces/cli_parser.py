"""Argparse surface for eternalforge."""

from __future__ import annotations

import argparse
from pathlib import Path

from interfaces.cli_const import BACKEND_HELP


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="eternalforge")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="cmd", required=True)
    status = sub.add_parser("status", help="Print phase, progress, next task")
    status.add_argument(
        "--kind",
        default=None,
        help="Only include this journal kind in journal_kinds",
    )
    status.add_argument(
        "--digest",
        action="store_true",
        help="List digest-*.md filenames after the status block",
    )
    sub.add_parser("next", help="Print the planned next task")
    cycle = sub.add_parser("cycle", help="Run one plan-act-reflect loop")
    cycle.add_argument("--dry-run", action="store_true")
    recent = sub.add_parser("recent", help="Dump recent journal entries")
    recent.add_argument(
        "--kind",
        default=None,
        help="Filter entries by kind (cycle, research, capture, ...)",
    )
    recent.add_argument(
        "--tag",
        default=None,
        help="Filter entries by persisted tag (case-insensitive; leading # optional)",
    )
    recent.add_argument("--max", type=int, default=20, dest="max_results")
    research = sub.add_parser("research", help="Run a search via an adapter")
    research.add_argument("query", nargs="+", help="Search query")
    research.add_argument("--max", type=int, default=5, dest="max_results")
    research.add_argument("--backend", default="wikipedia", help=BACKEND_HELP)
    research.add_argument(
        "--offline",
        action="store_true",
        help="Use FixtureAdapter instead of a live backend",
    )
    research.add_argument(
        "--no-journal",
        action="store_true",
        help="Skip writing hits to memory/journal.jsonl",
    )
    research.add_argument(
        "--tag",
        action="append",
        dest="tags",
        help="Tag to persist on the journal row (repeatable)",
    )
    cap = sub.add_parser("capture", help="Research topics and write memory/YYYY-MM-DD.md")
    cap.add_argument(
        "--topic",
        action="append",
        dest="topics",
        help="Topic to capture (repeatable). Defaults to a small curated list.",
    )
    cap.add_argument("--max", type=int, default=3, dest="max_results")
    cap.add_argument("--day", default=None, help="Override date key YYYY-MM-DD")
    cap.add_argument("--backend", default="wikipedia", help=BACKEND_HELP)
    cap.add_argument(
        "--offline",
        action="store_true",
        help="Use FixtureAdapter instead of a live backend",
    )
    cap.add_argument(
        "--tag",
        action="append",
        dest="tags",
        help="Tag to persist on the journal row (repeatable)",
    )
    kb = sub.add_parser("kb", help="Search memory markdown + journal")
    kb.add_argument("query", nargs="+", help="Knowledge-base query")
    kb.add_argument("--max", type=int, default=8, dest="max_results")
    kb.add_argument(
        "--kind",
        default=None,
        help="Filter by document kind (research, capture, markdown, journal, ...)",
    )
    kb.add_argument(
        "--source",
        default=None,
        help="Filter by source facet (markdown, journal, report)",
    )
    kb.add_argument(
        "--tag",
        default=None,
        help="Filter by tag / hashtag extracted from the document",
    )
    kb.add_argument(
        "--since",
        default=None,
        help="Only documents on or after YYYY-MM-DD",
    )
    kb.add_argument(
        "--until",
        default=None,
        help="Only documents on or before YYYY-MM-DD",
    )
    kb.add_argument(
        "--write-index",
        action="store_true",
        help="Also persist memory/kb-index.json",
    )
    report = sub.add_parser(
        "report",
        help="Compile a markdown report from journal research hits",
    )
    report.add_argument("--day", default=None, help="Output date key YYYY-MM-DD")
    report.add_argument(
        "--since",
        default=None,
        help="Only research entries on or after YYYY-MM-DD",
    )
    report.add_argument(
        "--until",
        default=None,
        help="Only research entries on or before YYYY-MM-DD",
    )
    report.add_argument(
        "--max",
        type=int,
        default=None,
        dest="max_entries",
        help="Keep only the last N matching research entries",
    )
    report.add_argument(
        "--tag",
        action="append",
        dest="tags",
        help="Tag to persist on the report journal row (repeatable)",
    )
    review = sub.add_parser(
        "review",
        help="Write a daily or weekly review sketch from journal + tasks",
    )
    review.add_argument("--day", default=None, help="Anchor date YYYY-MM-DD (default today UTC)")
    review.add_argument(
        "--period",
        default="daily",
        help="daily (default) or weekly (7 days ending on --day)",
    )
    review.add_argument(
        "--max",
        type=int,
        default=None,
        dest="max_entries",
        help="Keep only the last N journal rows in the window",
    )
    review.add_argument(
        "--tag",
        action="append",
        dest="tags",
        help="Tag to persist on the review journal row (repeatable)",
    )
    review.add_argument(
        "--digest",
        action="store_true",
        help="Write a reviews coverage digest instead of a daily/weekly sketch",
    )
    task = sub.add_parser("task", help="Track personal tasks (add / list / done)")
    task_sub = task.add_subparsers(dest="task_cmd", required=True)
    task_add = task_sub.add_parser("add", help="Create an open task")
    task_add.add_argument("title", nargs="+", help="Task title")
    task_add.add_argument("--notes", default="", help="Optional notes")
    task_add.add_argument(
        "--tag",
        action="append",
        dest="tags",
        help="Tag to persist on the task (repeatable)",
    )
    task_add.add_argument("--due", default=None, help="Due date YYYY-MM-DD")
    task_add.add_argument(
        "--priority",
        default=None,
        help="Priority: low, medium, high, urgent (default medium)",
    )
    task_list = task_sub.add_parser("list", help="List tasks")
    task_list.add_argument(
        "--status",
        default=None,
        help="Filter by status: open, done, cancelled",
    )
    task_list.add_argument(
        "--priority",
        default=None,
        help="Filter by priority: low, medium, high, urgent",
    )
    task_list.add_argument(
        "--tag",
        action="append",
        dest="tags",
        help="Filter by tag (repeatable; match any; leading # optional)",
    )
    task_list.add_argument(
        "--query",
        default=None,
        help="Case-insensitive substring match on title and notes",
    )
    task_list.add_argument(
        "--id",
        default=None,
        dest="task_id_prefix",
        help="Filter by task id prefix (case-insensitive, e.g. T00 or t001)",
    )
    task_list.add_argument(
        "--since",
        default=None,
        help="Only tasks created on or after YYYY-MM-DD",
    )
    task_list.add_argument(
        "--until",
        default=None,
        help="Only tasks created on or before YYYY-MM-DD",
    )
    task_list.add_argument(
        "--overdue",
        action="store_true",
        help="Only open tasks whose due date is before today",
    )
    task_list.add_argument(
        "--due-soon",
        nargs="?",
        const=7,
        default=None,
        dest="due_soon",
        help="Only open tasks due today through N days (default 7)",
    )
    task_list.add_argument(
        "--exact-id",
        action="store_true",
        dest="exact_id",
        help="Require --id to match the full task id (not a prefix)",
    )
    task_list.add_argument(
        "--updated-since",
        default=None,
        help="Only tasks updated on or after YYYY-MM-DD",
    )
    task_list.add_argument(
        "--updated-until",
        default=None,
        help="Only tasks updated on or before YYYY-MM-DD",
    )
    task_list.add_argument(
        "--sort",
        default="due",
        help="Sort by due (default), priority, created, or updated",
    )
    task_done = task_sub.add_parser("done", help="Mark a task done")
    task_done.add_argument("task_id", help="Task id such as T001")
    task_set = task_sub.add_parser("set", help="Set task status / due / priority / notes / tags / title")
    task_set.add_argument("task_id", help="Task id such as T001")
    task_set.add_argument(
        "status",
        nargs="?",
        default=None,
        help="open, done, or cancelled",
    )
    task_set.add_argument("--due", default=None, help="Due date YYYY-MM-DD (empty to clear)")
    task_set.add_argument(
        "--priority",
        default=None,
        help="Priority: low, medium, high, urgent",
    )
    task_set.add_argument(
        "--notes",
        default=None,
        help="Replace notes (empty string clears)",
    )
    task_set.add_argument(
        "--tag",
        action="append",
        dest="tags",
        help="Replace task tags (repeatable; omit to leave unchanged; pass empty to clear)",
    )
    task_set.add_argument(
        "--title",
        default=None,
        help="Replace the task title (must be non-empty)",
    )
    inbox = sub.add_parser("inbox", help="List or capture Gmail/Drive items (sketch + creds probe)")
    inbox_sub = inbox.add_subparsers(dest="inbox_cmd", required=True)
    inbox_list = inbox_sub.add_parser("list", help="List fixture or live-stub inbox items")
    inbox_list.add_argument(
        "--source",
        default=None,
        help="gmail, drive, or omit for all",
    )
    inbox_list.add_argument("--query", default=None, help="Case-insensitive substring filter")
    inbox_list.add_argument("--max", type=int, default=10, dest="max_results")
    inbox_list.add_argument(
        "--offline",
        action="store_true",
        help="Use FixtureInboxAdapter (default when --live is omitted)",
    )
    inbox_list.add_argument(
        "--live",
        action="store_true",
        help="Use LiveInboxAdapter (empty list until a Google client is wired)",
    )
    inbox_cap = inbox_sub.add_parser("capture", help="Persist matching items to the journal")
    inbox_cap.add_argument(
        "--source",
        default=None,
        help="gmail, drive, or omit for all",
    )
    inbox_cap.add_argument("--query", default=None, help="Case-insensitive substring filter")
    inbox_cap.add_argument("--max", type=int, default=10, dest="max_results")
    inbox_cap.add_argument(
        "--offline",
        action="store_true",
        help="Use FixtureInboxAdapter",
    )
    inbox_cap.add_argument(
        "--live",
        action="store_true",
        help="Use LiveInboxAdapter (empty list until a Google client is wired)",
    )
    inbox_cap.add_argument(
        "--tag",
        action="append",
        dest="tags",
        help="Tag to persist on the journal row (repeatable)",
    )
    inbox_sub.add_parser(
        "status",
        help="Show whether a local Google token file is present (never prints secrets)",
    )
    return parser
