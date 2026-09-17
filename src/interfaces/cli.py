"""eternalforge status | next | cycle [--dry-run] | recent | research QUERY | capture | kb QUERY | report | review | task | inbox

Parser lives in interfaces.cli_parser; constants in interfaces.cli_const.
This module is the public facade (build_parser + main).
"""

from __future__ import annotations

import sys

from core.agent import Agent
from interfaces.cli_const import BACKEND_HELP
from interfaces.cli_parser import build_parser
from tools.capture import DEFAULT_TOPICS, capture
from tools.inbox import LiveInboxAdapter, capture_inbox, format_items, get_inbox_adapter, list_inbox
from tools.kb import build_index, format_index_hits, parse_day, search_kb, write_index
from tools.report import write_report
from tools.research import FixtureAdapter, format_hits, get_adapter, record_hits, search
from tools.review import write_digest, write_review
from tools.tasks import add_task, format_tasks, list_tasks, update_task

__all__ = ["BACKEND_HELP", "build_parser", "main"]


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    agent = Agent(args.root)
    try:
        if args.cmd == "status":
            print(agent.status(kind=args.kind, digest=args.digest))
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
        elif args.cmd == "review":
            if args.digest:
                digest = write_digest(
                    args.root,
                    day=args.day,
                    tags=args.tags,
                )
                print(
                    f"wrote {digest.path} "
                    f"(Reviews={digest.review_count}, daily={digest.daily_count}, "
                    f"weekly={digest.weekly_count}, digest={digest.digest_count})"
                )
            else:
                result = write_review(
                    args.root,
                    day=args.day,
                    period=args.period,
                    max_entries=args.max_entries,
                    tags=args.tags,
                )
                print(
                    f"wrote {result.path} "
                    f"({result.journal_count} journal, {result.open_count} open, "
                    f"{result.overdue_count} overdue, {result.done_count} done)"
                )
        elif args.cmd == "inbox":
            if args.inbox_cmd == "status":
                print(LiveInboxAdapter(root=args.root).creds_status().format())
                return 0
            use_live = bool(getattr(args, "live", False)) and not bool(getattr(args, "offline", False))
            adapter = get_inbox_adapter("live" if use_live else "fixture", root=args.root)
            if args.inbox_cmd == "list":
                print(
                    format_items(
                        list_inbox(
                            source=args.source,
                            query=args.query,
                            limit=args.max_results,
                            adapter=adapter,
                        )
                    )
                )
            elif args.inbox_cmd == "capture":
                result = capture_inbox(
                    args.root,
                    source=args.source,
                    query=args.query,
                    limit=args.max_results,
                    adapter=adapter,
                    tags=args.tags,
                )
                print(f"{result.summary}")
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
                            exact_id=args.exact_id,
                            since=args.since,
                            until=args.until,
                            updated_since=args.updated_since,
                            updated_until=args.updated_until,
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
