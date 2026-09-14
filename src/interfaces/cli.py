"""eternalforge status | next | cycle [--dry-run] | research QUERY | capture"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from core.agent import Agent
from tools.capture import DEFAULT_TOPICS, capture
from tools.research import FixtureAdapter, WikipediaAdapter, format_hits, record_hits, search


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eternalforge")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="Print phase, progress, next task")
    sub.add_parser("next", help="Print the planned next task")
    cycle = sub.add_parser("cycle", help="Run one plan-act-reflect loop")
    cycle.add_argument("--dry-run", action="store_true")
    research = sub.add_parser("research", help="Run a search via an adapter")
    research.add_argument("query", nargs="+", help="Search query")
    research.add_argument("--max", type=int, default=5, dest="max_results")
    research.add_argument(
        "--offline",
        action="store_true",
        help="Use FixtureAdapter instead of Wikipedia",
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
    cap.add_argument(
        "--offline",
        action="store_true",
        help="Use FixtureAdapter instead of Wikipedia",
    )

    args = parser.parse_args(argv)
    agent = Agent(args.root)
    try:
        if args.cmd == "status":
            print(agent.status())
        elif args.cmd == "next":
            print(agent.plan())
        elif args.cmd == "cycle":
            print(agent.run_once(dry_run=args.dry_run))
        elif args.cmd == "research":
            query = " ".join(args.query)
            adapter = FixtureAdapter() if args.offline else WikipediaAdapter()
            hits = search(query, max_results=args.max_results, adapter=adapter)
            if not args.no_journal:
                record_hits(query, hits, root=args.root)
            print(format_hits(hits))
        elif args.cmd == "capture":
            adapter = FixtureAdapter() if args.offline else WikipediaAdapter()
            topics = args.topics or list(DEFAULT_TOPICS)
            result = capture(
                args.root,
                topics=topics,
                adapter=adapter,
                max_results=args.max_results,
                day=args.day,
            )
            print(f"wrote {result.path} ({result.hit_count} hits, {len(result.topics)} topics)")
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
