"""eternalforge status | next | cycle [--dry-run] | recent | research QUERY | capture | kb QUERY | report | task"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from core.agent import Agent
from tools.capture import DEFAULT_TOPICS, capture
from tools.kb import build_index, format_index_hits, parse_day, search_kb, write_index
from tools.report import write_report
from tools.research import FixtureAdapter, format_hits, get_adapter, record_hits, search
from tools.tasks import add_task, format_tasks, list_tasks, update_task

BACKEND_HELP = (
    "Search backend: wikipedia, duckduckgo, openlibrary, hackernews, arxiv, crossref, "
    "semanticscholar, pubmed, multi, fixture "
    "(aliases: ddg, ol, books, hn, algolia, papers, preprint, doi, works, s2, scholar, "
    "ncbi, medline, all)"
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eternalforge")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="cmd", required=True)
    status = sub.add_parser("status", help="Print phase, progress, next task")
    status.add_argument(
        "--kind",
        default=None,
        help="Only include this journal kind in journal_kinds",
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
        "--sort",
        default="due",
        help="Sort by due (default) or priority",
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

    args = parser.parse_args(argv)
    agent = Agent(args.root)
    try:
        if args.cmd == "status":
            print(agent.status(kind=args.kind))
        elif args.cmd == "next":
            print(agent.plan())
        elif args.cmd == "cycle":
            print(agent.run_once(dry_run=args.dry_run))
        elif args.cmd == "recent":
            print(agent.dump_recent(n=args.max_results, kind=args.kind, tag=args.tag))
        elif args.cmd == "research":
            query = " ".join(args.query)
            adapter = FixtureAdapter() if args.offline else get_adapter(args.backend)
            hits = search(query, max_results=args.max_results, adapter=adapter)
            if not args.no_journal:
                record_hits(query, hits, root=args.root, tags=args.tags)
            print(format_hits(hits))
        elif args.cmd == "capture":
            adapter = FixtureAdapter() if args.offline else get_adapter(args.backend)
            topics = args.topics or list(DEFAULT_TOPICS)
            result = capture(
                args.root,
                topics=topics,
                adapter=adapter,
                max_results=args.max_results,
                day=args.day,
                tags=args.tags,
            )
            print(f"wrote {result.path} ({result.hit_count} hits, {len(result.topics)} topics)")
        elif args.cmd == "kb":
            query = " ".join(args.query)
            since = parse_day(args.since)
            until = parse_day(args.until)
            if args.write_index:
                write_index(build_index(root=args.root), args.root)
            hits = search_kb(
                args.root,
                query,
                max_results=args.max_results,
                kind=args.kind,
                since=since,
                until=until,
                source=args.source,
                tag=args.tag,
            )
            print(format_index_hits(hits))
        elif args.cmd == "report":
            since = parse_day(args.since)
            until = parse_day(args.until)
            result = write_report(
                args.root,
                day=args.day,
                since=since,
                until=until,
                max_entries=args.max_entries,
                tags=args.tags,
            )
            print(
                f"wrote {result.path} "
                f"({result.entry_count} run(s), {result.query_count} query(ies))"
            )
        elif args.cmd == "task":
            if args.task_cmd == "add":
                task_obj = add_task(
                    args.root,
                    " ".join(args.title),
                    notes=args.notes,
                    tags=args.tags,
                    due=args.due,
                    priority=args.priority,
                )
                extra = ""
                if task_obj.priority != "medium":
                    extra += f"\tp={task_obj.priority}"
                if task_obj.due:
                    extra += f"\tdue={task_obj.due}"
                print(f"added {task_obj.id}\t{task_obj.status}\t{task_obj.title}{extra}")
            elif args.task_cmd == "list":
                print(
                    format_tasks(
                        list_tasks(
                            args.root,
                            status=args.status,
                            priority=args.priority,
                            tag=args.tags,
                            query=args.query,
                            task_id=args.task_id_prefix,
                            since=args.since,
                            until=args.until,
                            overdue=args.overdue,
                            due_soon=args.due_soon if args.due_soon is not None else False,
                            sort=args.sort,
                        )
                    )
                )
            elif args.task_cmd == "done":
                task_obj = update_task(args.root, args.task_id, status="done")
                print(f"{task_obj.id}\t{task_obj.status}\t{task_obj.title}")
            elif args.task_cmd == "set":
                if (
                    args.status is None
                    and args.due is None
                    and args.priority is None
                    and args.notes is None
                    and args.tags is None
                    and args.title is None
                ):
                    raise ValueError(
                        "task set needs a status, --due, --priority, --notes, --tag, or --title"
                    )
                task_obj = update_task(
                    args.root,
                    args.task_id,
                    status=args.status,
                    due=args.due,
                    priority=args.priority,
                    notes=args.notes,
                    tags=args.tags,
                    title=args.title,
                )
                extra = ""
                if task_obj.priority != "medium":
                    extra += f"\tp={task_obj.priority}"
                if task_obj.due:
                    extra += f"\tdue={task_obj.due}"
                if task_obj.tags:
                    extra += f"\t#{',#'.join(task_obj.tags)}"
                print(f"{task_obj.id}\t{task_obj.status}\t{task_obj.title}{extra}")
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
