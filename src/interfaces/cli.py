"""eternalforge status | next | cycle [--dry-run] | recent | research QUERY | capture | kb QUERY | report"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from core.agent import Agent
from tools.capture import DEFAULT_TOPICS, capture
from tools.kb import build_index, format_index_hits, parse_day, search_kb, write_index
from tools.report import write_report
from tools.research import FixtureAdapter, format_hits, get_adapter, record_hits, search

BACKEND_HELP = (
    "Search backend: wikipedia, duckduckgo, openlibrary, multi, fixture "
    "(aliases: ddg, ol, books, all)"
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
    kb = sub.add_parser("kb", help="Search memory markdown + journal")
    kb.add_argument("query", nargs="+", help="Knowledge-base query")
    kb.add_argument("--max", type=int, default=8, dest="max_results")
    kb.add_argument(
        "--kind",
        default=None,
        help="Filter by document kind (research, capture, markdown, journal, ...)",
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
            print(agent.dump_recent(n=args.max_results, kind=args.kind))
        elif args.cmd == "research":
            query = " ".join(args.query)
            adapter = FixtureAdapter() if args.offline else get_adapter(args.backend)
            hits = search(query, max_results=args.max_results, adapter=adapter)
            if not args.no_journal:
                record_hits(query, hits, root=args.root)
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
            )
            print(
                f"wrote {result.path} "
                f"({result.entry_count} run(s), {result.query_count} query(ies))"
            )
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
