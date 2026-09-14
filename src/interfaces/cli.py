"""eternalforge status | next | cycle [--dry-run] | research QUERY"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from core.agent import Agent
from tools.research import FixtureAdapter, WikipediaAdapter, format_hits, search


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
            print(format_hits(hits))
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
