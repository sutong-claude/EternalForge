"""eternalforge status | next | cycle [--dry-run]"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from core.agent import Agent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eternalforge")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="Print phase, progress, next task")
    sub.add_parser("next", help="Print the planned next task")
    cycle = sub.add_parser("cycle", help="Run one plan-act-reflect loop")
    cycle.add_argument("--dry-run", action="store_true")

    args = parser.parse_args(argv)
    agent = Agent(args.root)
    try:
        if args.cmd == "status":
            print(agent.status())
        elif args.cmd == "next":
            print(agent.plan())
        elif args.cmd == "cycle":
            print(agent.run_once(dry_run=args.dry_run))
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
